#!/usr/bin/env python3

from time import sleep

from influxdb import client as influxdb
from bcs_call_handler import BCSCallHandler

from constants import (
    BCS_URL,
    BCS_PORT,
    BCS_USERNAME,
    BCS_PASSWORD,
    DB_IP,
    DB_PORT,
    DB_USERNAME,
    DB_PASSWORD,
    DB_DATABASE,
)


bcs = BCSCallHandler(
    url=BCS_URL,
    port=BCS_PORT,
    username=BCS_USERNAME,
    password=BCS_PASSWORD
)

db = influxdb.InfluxDBClient(
    DB_IP,
    DB_PORT,
    DB_USERNAME,
    DB_PASSWORD,
    DB_DATABASE
)


def format_point(measurement_name, fields, tags=None):
    return {"measurement": measurement_name, "fields": fields, "tags": tags if tags else {}}


def log():
    temp_data = bcs.temps()
    output_data = bcs.outputs(to_data_type=int)
    points = [
        format_point('temperatures', temp_data['temps']),
        format_point('setpoints', temp_data['setpoints']),
        format_point('swings', temp_data['swings']),
        # summing in daemon because InfluxDB is lame and makes me use Flux for join queries
        format_point('setpoint_swing_sums', temp_data['setpoint_swing_sums']),
        format_point('outputs', output_data)
    ]
    db.write_points(points)
    return points


if __name__ == '__main__':
    while True:
        try:
            print(log())
        except Exception as e:  # do not let daemon crash
            exception_type = type(e).__name__
            print(exception_type)
            try:
                db.write_points([{
                    'measurement': 'errors',
                    'fields': {'exceptionType': exception_type},
                    'tags': {}
                }])
            except Exception as e:  # do not let daemon crash
                exception_type = type(e).__name__
                print(exception_type)
        sleep(10)
