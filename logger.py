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


def log():
    temp_data = bcs.temps()
    output_data = bcs.outputs(to_data_type=int)
    points = [
        {'measurement': 'temperatures', 'fields': temp_data['temps'], 'tags': {}},
        {'measurement': 'setpoints', 'fields': temp_data['setpoints'], 'tags': {}},
        {'measurement': 'outputs', 'fields': output_data, 'tags': {}},
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
