from influxdb import InfluxDBClient
import requests

import time

client = None
dbname = None
measurement = None


def db_exists():
    """returns True if the database exists"""
    dbs = client.get_list_database()
    for db in dbs:
        if db['name'] == dbname:
            return True
    return False


def wait_for_server(host, port, nretries=8):
    """wait for the server to come online for waiting_time, nretries times."""
    url = 'http://{}:{}'.format(host, port)
    waiting_time = 1
    for i in range(nretries):
        try:
            requests.get(url)
            return 0
        except requests.exceptions.ConnectionError:
            print('waiting for', url)
            time.sleep(waiting_time)
            waiting_time *= 2
    raise ValueError('influxdb server not available', url)


def connect_db(host, port, reset=False):
    """connect to the database, and create it if it does not exist"""
    global client
    # print('connecting to database: {}:{}'.format(host,port))
    client = InfluxDBClient(host, port, retries=5, timeout=1)
    wait_for_server(host, port)
    create = False
    if not db_exists():
        create = True
        client.create_database(dbname)
    client.switch_database(dbname)
    if not create and reset:
        client.delete_series(measurement=measurement)
    return 0


def get_entries():
    """returns all entries in the database."""
    results = client.query('select * from {}'.format(measurement))
    # we decide not to use the x tag
    return list(results.get_points(measurement, None))
