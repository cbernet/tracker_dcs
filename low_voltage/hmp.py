import paho.mqtt.client as mqtt
from dataclasses import dataclass
import time
import json
import visa
from typing import Union


@dataclass
class Channel(object):
    number: int
    on: bool = False
    vreq: float = 0.


class HMP(object):

    def __init__(self, name: str, n_channels: int = 1):
        self.channels = [Channel(i) for i in range(n_channels)]
        self.name = name
        rm = visa.ResourceManager("/usr/lib64/librsvisa.so@ni")
        HMP4040 = rm.open_resource('TCPIP::192.168.1.203::10002::SOCKET')
        HMP4040.read_termination = '\n'
        HMP4040.write_termination = '\n'
        HMP4040.write("*IDN?")
        idn = HMP4040.read()
        print("IDN:", idn)
        HMP4040.set_visa_attribute(visa.constants.VI_ATTR_TERMCHAR_EN,True)
        attr = HMP4040.get_visa_attribute(visa.constants.VI_ATTR_TERMCHAR_EN)
        print("Attrib. TERMCHAR_EN:", attr)
        HMP4040.set_visa_attribute(visa.constants.VI_ATTR_SUPPRESS_END_EN,False)
        attr = HMP4040.get_visa_attribute(visa.constants.VI_ATTR_SUPPRESS_END_EN)
        print("Attrib. SUPPRESS_END_EN:", attr)
        print()
        HMP4040.write("INST:NSEL 1")
        HMP4040.write("INST:NSEL?")
        Channel_hmp = HMP4040.read()
        print("Channel  :  ",  Channel_hmp)
        channel.number = Channel_hmp
        if Channel_hmp > 0 :
            channel.on = True 
        HMP4040.write("MEAS:VOLT?")
        V1 = HMP4040.read()
        print("V1 : ",V1)
        channel.vreq = V1
        

    def command(self, topic: str, message: Union[bytes, float, int]) -> None:
        device, cmd, command, channel = topic.split('/')[1:]
        if cmd != 'cmd':
            raise ValueError('command messages should be of the form /device/cmd/#')
        commands = ['switch', 'setv']
        if device != self.name:
            raise ValueError('wrong hv! ', device, self.name)
        channel = int(channel)
        if command == 'switch':
            message = message.decode('utf-8')
            if message == 'on':
                self.channels[channel].on = True
            elif message == 'off':
                self.channels[channel].on = False
            else:
                msg = 'can only switch on or off'
                raise ValueError(msg)
        elif command == 'setv':
            self.channels[channel].vreq = float(message)
        else:
            raise ValueError('only possible commands are', commands)

    def status(self):
        """TODO: Write unittest"""
        status_channels = []
        for channel in self.channels:
            status_channels.append({
                'number': channel.number,
                'on': int(channel.on), # issue with bools in telegraf/influxdb
                'vreq': channel.vreq,
            })
        return status_channels


def on_connect(client, userdata, flags, rc):
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(f'/{client.device.name}/cmd/#')


def on_message(client, userdata, msg):
    print('recv', msg.topic, msg.payload)
    client.device.command(msg.topic, msg.payload)


def run(device, mqtt_host):
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.device = device
    client.connect(mqtt_host, 1883, 60)
    client.loop_start()
    while 1:
        client.publish(
            '/{}/status'.format(device.name),
            json.dumps(device.status())
        )
        time.sleep(1)
    time.sleep(1)
    client.disconnect()
    client.loop_stop()


if __name__ == '__main__':
    import sys
    device_name, mqtt_host = sys.argv[1:]
    device = HMP(device_name)
    run(device, mqtt_host)
