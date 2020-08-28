import serial
import re
import paho.mqtt.client as mqtt
import json
import logging
import sys

# logging configuration

level = logging.DEBUG
log = logging.getLogger(__name__)
log.setLevel(level)

sh = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(module)s | %(message)s')
sh.setFormatter(formatter)
sh.setLevel(level)
log.addHandler(sh)


temp_pat = re.compile(r'^Temperature: (\d+.\d+).*')
hum_pat = re.compile(r'^Humidity: (\d+.\d+).*')


def run(mqtt_host, sensor_name):
    print(mqtt_host)
    client = mqtt.Client()
    client.connect(mqtt_host, 1883, 60)
    log.info('mqtt connected')
    client.loop_start()
    with serial.Serial('/dev/ttyACM0', 9600, timeout=2) as ser:
        while 1:
            line = ser.readline()
            line = line.decode().strip()
            line = line.rstrip()
            log.debug(line)
            m = temp_pat.match(line)
            if m:
                value = float(m.group(1))
                topic = '/sensor/{}/temperature'.format(sensor_name)
                data = {'topic': topic,
                          'sensor': sensor_name,
                          'measurement': 'temperature',
                          'value': value}
                log.info(data)
                client.publish(
                    topic,
                    json.dumps(data)
                )
            else:
                m = hum_pat.match(line)
                if m:
                    value = float(m.group(1))
                    topic = '/sensor/{}/humidity'.format(sensor_name)
                    client.publish(
                        topic,
                        json.dumps({'topic': topic,
                                    'sensor': sensor_name,
                                    'measurement': 'humidity',
                                    'value': value})
                    )
                else:
                    log.error('cannot read temperature or humidity')
    client.disconnect()
    client.loop_stop()


if __name__ == '__main__':
    import sys
    mqtt_host, sensor_name = sys.argv[1:]
    run(mqtt_host, sensor_name)
