# -*- coding: utf-8 -*-
from common_cfg import *
from .consult_cfg import *
import paho.mqtt.client as mqtt
import paho.mqtt.publish as mqttpublish
import struct 
#https://pypi.python.org/pypi/paho-mqtt/1.1#id17

def run():
    valores = struct.pack("BBB",1,1,1)
    
    
    #~ client.connect(mqtt_server, mqtt_port)
    print(valores)
    mqttpublish.single("mota1", payload =valores,hostname=mqtt_server, port=mqtt_port)
    
if __name__ == '__main__':
    run()
