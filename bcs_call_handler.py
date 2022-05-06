"""
Log into BCS460/BCS462 brewery controller
Make calls
Return dicts
"""

import requests

NUM_PROBES = 8
NUM_OUTPUTS = 18


class BCSCallHandler(object):
    """TODO docstrings"""

    def __init__(self, url, port, username, password):
        self.url = url
        self.port = port
        self.username = username
        self.password = password

    def get(self, path):
        return requests.get(
            f"{self.url}:{self.port}/api/{path}", auth=(self.username, self.password)
        ).json()

    def temps(self):
        temp_data = [self.get(f"temp/{probe}") for probe in range(NUM_PROBES)]
        ordered_names = [probe["name"] for probe in temp_data]
        active_controllers = self.active_output_controllers()

        setpoints = _format_setpoints(
            temp_data
        )  # todo yeah get it from controllers for sure because summing
        swings = _format_swings(ordered_names, active_controllers)

        return dict(
            temps=_format_temperatures(temp_data),
            setpoints=setpoints,
            swings=swings,
            # summing in daemon because InfluxDB is lame and makes me use Flux for join queries
            setpoint_swing_sums=_format_setpoint_swing_sums(setpoints, swings),
        )

    def outputs(self, to_data_type=bool):
        output_data = [self.get(f"output/{out}") for out in range(NUM_OUTPUTS)]
        return _format_outputs(output_data, to_data_type)

    def active_output_controllers(self):
        aoc = []
        for proc, state in self._active_processes_and_states_numbers():
            aoc += [
                output_controllers
                for output_controllers in self.get(
                    "process/{}/state/{}/output_controllers".format(proc, state)
                )
                if output_controllers["mode"] != 0  # 0 is inactive
            ]
        return aoc

    def _active_processes_and_states_numbers(self):
        active_process_nums = [
            process_num
            for process_num, active in enumerate(self.get("process"))
            if active
        ]
        return [
            (proc_num, self.get(f"process/{proc_num}")["current_state"]["state"])
            for proc_num in active_process_nums
        ]


def _format_temperatures(temp_data):
    return {temp["name"]: _move_decimal(temp["temp"]) for temp in temp_data}


def _format_setpoints(temp_data):
    return {
        temp["name"]: _move_decimal(temp["setpoint"])
        for temp in temp_data
        if temp["setpoint"]
    }


def _format_swings(ordered_names, active_controllers):
    return {
        ordered_names[controller["input"]]: _move_decimal(controller["swing"])
        for controller in active_controllers
    }


def _format_setpoint_swing_sums(setpoints, swings):
    sums = {}
    for key in setpoints:
        sums[key] = setpoints[key] + swings[key]
    return sums


def _format_outputs(output_data, to_data_type):
    return {output["name"]: to_data_type(output["on"]) for output in output_data}


def _move_decimal(num):
    return num / 10
