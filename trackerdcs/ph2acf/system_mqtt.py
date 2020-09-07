import paho.mqtt.client as mqtt

import logging
import sys

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

    def __init__(self, device_name):
        self.device_name = device_name

    def add_command(self, cmd_name, cmd):
        """add a new command"""
        log.info(f'registering command {cmd_name} : {cmd}')

    def command(self, cmd_name, cmd):
        cmd = cmd.decode()
        log.info(f'executing: {cmd_name}, {cmd}')

    def topic(self):
        """returns device topic"""
        return f'/{self.device_name}/cmd'


def on_connect(client, userdata, flags, rc):
    topic = client.device.topic()
    log.info(f'subscribing to {topic}')
    client.subscribe(topic)


def on_message(client, userdata, msg):
    log.info(f'received: {msg.topic} : {msg.payload}')
    client.device.command(msg.topic, msg.payload)
    if log.level == logging.DEBUG:
        client.publish('/test', 'ok')


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