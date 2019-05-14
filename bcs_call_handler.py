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
            f'{self.url}:{self.port}/api/{path}',
            auth=(self.username, self.password)
        ).json()

    def temps(self):
        temp_data = [
            self.get(f'temp/{probe}')
            for probe in range(NUM_PROBES)
        ]
        return dict(
            setpoints=_format_setpoints(temp_data),
            temps=_format_temperatures(temp_data),
        )

    def outputs(self, to_data_type=bool):
        output_data = [
            self.get(f'output/{out}')
            for out in range(NUM_OUTPUTS)
        ]
        return _format_outputs(
            output_data,
            to_data_type
        )


def _format_temperatures(temp_data):
    return {
        temp['name']: _move_decimal(temp['temp'])
        for temp in temp_data
    }


def _format_setpoints(temp_data):
    return {
        temp['name']: _move_decimal(temp['setpoint'])
        for temp in temp_data if temp['setpoint']
    }


def _format_outputs(output_data, to_data_type):
    return {
        output['name']: to_data_type(output['on'])
        for output in output_data
    }


def _move_decimal(num):
    return num / 10
