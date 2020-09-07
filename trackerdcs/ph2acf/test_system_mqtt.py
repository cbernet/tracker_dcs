import unittest
from multiprocessing import Process
import paho.mqtt.client as mqtt
import time
from trackerdcs.ph2acf.system_mqtt import SystemMQTT, run


class TestSystemMQTT(unittest.TestCase):

    def setUp(self) -> None:
        self.device_name = 'test'
        self.system = SystemMQTT(self.device_name)
        self.mqtt_host = 'localhost'
        self.client = mqtt.Client()
        self.client.connect(self.mqtt_host, 1883, 60)

    def tearDown(self) -> None:
        self.client.disconnect()

    def test_1(self):
        self.assertTrue(True)

    def test_run(self):
        p = Process(target=run, args=[self.system, self.mqtt_host])
        p.start()
        # when for mqtt connection
        time.sleep(0.5)
        self.assertTrue(True)
        self.client.publish(self.system.topic(), 'ls')
        time.sleep(1)
        p.terminate()


if __name__ == '__main__':
    unittest.main()
