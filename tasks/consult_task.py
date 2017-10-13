# -*- coding: utf-8 -*-
from common_cfg import *
from .consult_cfg import *
import wenuclient 
import paho.mqtt.client as mqtt
import paho.mqtt.publish as mqttpublish
import struct 
import time
#https://pypi.python.org/pypi/paho-mqtt/1.1#id17

def run():
    valores = struct.pack("BBB",1,1,1)
    server = "http://163.10.10.118/wenuapi"
    user = ***REMOVED***
    password = ***REMOVED***
    session = wenuclient.get_session(
                            '/'.join((server, 'login')),
                            user,
                            password,
                        )
    client = wenuclient.Client(server, session)
    lista = client.Action.where(viewed = False)
    for each in lista:
        print("hay entrada")
        for cada in range(3):
            mqttpublish.single("motaID/accion", payload =valores,hostname=mqtt_server, port=mqtt_port)
            time.sleep(0.2)
        each.viewed = True
        each.save()
    
if __name__ == '__main__':
    run()
