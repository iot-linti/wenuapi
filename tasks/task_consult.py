# -*- coding: utf-8 -*-

from .mqtt2influxdb_cfg import *
import paho.mqtt.client as mqtt
import struct 
#https://pypi.python.org/pypi/paho-mqtt/1.1#id17

def run():
    valores = struct.pack("BBB",1,1,1)
    
    #~ client.on_message = to_influxdb(influxclient, logger)
    #~ client.connect(mqtt_server, mqtt_port)
    print(valores)
    #~ client.single("mota1", payload =valores,hostname=mqtt_server, port=mqtt_port)
    
if __name__ == '__main__':
    run()
