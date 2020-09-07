import paho.mqtt.client as mqtt

import logging
import sys
import subprocess
import json

level = logging.DEBUG
log = logging.getLogger(__name__)
log.setLevel(level)

formatter = logging.Formatter(
    '%(asctime)s %(levelname)s %(module)s | %(message)s')

sh = logging.StreamHandler(sys.stdout)
sh.setFormatter(formatter)
log.addHandler(sh)

fh = logging.FileHandler('log')
fh.setFormatter(formatter)
log.addHandler(fh)


class SystemMQTT(object):
    """Connected MQTT device for executing system commands"""

    def __init__(self, device_name):
        self.device_name = device_name

    # def add_command(self, cmd_name, cmd):
    #     """add a new command"""
    #     log.info(f'registering command {cmd_name} : {cmd}')

    def command(self, cmd_name, cmd):
        """execute system command as a subprocess"""
        cmd = cmd.decode()
        log.info(f'executing: {cmd_name}, {cmd}')
        # for security : need ad hoc protection
        if not cmd.startswith('ls'):
            return
        res = subprocess.run(cmd, capture_output=True)
        log.info(f'return code: {res.returncode}')
        stdout = res.stdout.decode().split('\n')
        return {'return_code': res.returncode, 'stdout': stdout}

    def topic(self):
        """returns device topic"""
        return f'/{self.device_name}/cmd'

    def topic_out(self):
        """returns device output topic"""
        return f'/{self.device_name}/out'


def on_connect(client, userdata, flags, rc):
    """Automatically subscribe to topic upon connection (mqtt callback)"""
    topic = client.device.topic()
    log.info(f'subscribing to {topic}')
    client.subscribe(topic)


def on_message(client, userdata, msg):
    """execute command (mqtt callback)"""
    log.info(f'received: {msg.topic} : {msg.payload}')
    output = client.device.command(msg.topic, msg.payload)
    topic = client.device.topic_out()
    log.info(f'returning {topic} {output}')
    client.publish(topic, json.dumps(output))


def run(device, mqtt_host):
    """Run forever, listening to commands"""
    log.info('run')
    client = mqtt.Client()
    client.device = device
    client.on_connect = on_connect
    client.on_message = on_message
    log.info('connecting')
    client.connect(mqtt_host, 1883, 60)
    log.info('mqtt connected. Starting loop...')
    client.loop_forever()



if __name__ == '__main__':
    import sys
    device_name, mqtt_host = sys.argv[1:]
    device = SystemMQTT(device_name)
    run(device, mqtt_host)