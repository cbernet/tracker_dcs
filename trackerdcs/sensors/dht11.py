import serial
import re
import paho.mqtt.client as mqtt
import json

temp_pat = re.compile('^Temperature: (\d+.\d+).*')
hum_pat = re.compile('^Humidity: (\d+.\d+).*')


def run(mqtt_host, sensor_name):
    client = mqtt.Client()
    client.connect(mqtt_host, 1883, 60)
    client.loop_start()
    with serial.Serial('/dev/cu.usbmodem141121', 9600, timeout=2) as ser:
        while 1:
            line = ser.readline()
            line = line.decode().strip()
            m = temp_pat.match(line)
            if m:
                value = float(m.group(1))
                # print('temp', value)
                topic = '/sensor/{}/temperature'.format(sensor_name)
                client.publish(
                    topic,
                    json.dumps({'topic': topic,
                                'sensor': sensor_name,
                                'measurement': 'temperature',
                                'value': value})
                )
            else:
                m = hum_pat.match(line)
                if m:
                    value = float(m.group(1))
                    # print('hum', value)
                    topic = '/sensor/{}/humidity'.format(sensor_name)
                    client.publish(
                        topic,
                        json.dumps({'topic': topic,
                                    'sensor': sensor_name,
                                    'measurement': 'humidity',
                                    'value': value})
                    )
    client.disconnect()
    client.loop_stop()


if __name__ == '__main__':
    import sys
    mqtt_host, sensor_name = sys.argv[1:]
    run(mqtt_host, sensor_name)