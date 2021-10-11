import unittest
import datetime

from influxdb_client import InfluxDBClient, Point, rest
from influxdb_client.client.write_api import SYNCHRONOUS

bucket = "my-bucket"
org = 'cms-tedd'
# TODO : from config file
client = InfluxDBClient(url="http://localhost:8086",
                        token="bWt05eYbDNNi1inKouIfs8R-EyAgL8VMhWfRBgw3ScgNiV1iXIwGyV4DajMLu-jhZNHnAJc7qfu4yeG3sf1o0g==",
                        org=org)
query_api = client.query_api()
write_api = client.write_api(write_options=SYNCHRONOUS)
delete_api = client.delete_api()
measurement = 'unittest_measurement'


class TestInflux(unittest.TestCase):

    def setUp(self) -> None:
        start = "1970-01-01T00:00:00Z"
        stop = datetime.datetime.now()
        try:
            delete_api.delete(
                start, stop,
                f'_measurement="{measurement}"',
                bucket=bucket, org=org
            )
        except rest.ApiException as err:
            pass

    def test_fill(self):
        """test that one can write a point"""
        temperature = 25
        p = Point(measurement).tag("location", "Prague").field(
            "temperature", temperature
        )
        res = write_api.write(bucket=bucket, record=p)

        q = f"""
from(bucket: "{bucket}")
|> range(start: -1s, stop: now())
|> filter(fn: (r) => r._measurement == "{measurement}")
"""
        tables = query_api.query(q)
        self.assertEqual(len(tables), 1)
        table = tables[0]
        self.assertEqual(len(table.records), 1)
        record = table.records[0]
        self.assertEqual(record['_value'], temperature)


if __name__ == "__main__":
    unittest.main()