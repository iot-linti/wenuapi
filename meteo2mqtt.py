#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import json
import paho.mqtt.client as mqtt
import requests
import time
import iso8601

server = '163.10.20.206'
port = 1883

client = mqtt.Client(client_id='linti_control')
client.connect(server, port)
client.loop_start()  # Maneja eventos y reconexiones

previous_check = None

try:
    while True:
        URL = 'http://clima.info.unlp.edu.ar/last?lang=es'
        try:
            req = requests.get(URL)
        except requests.exceptions.HTTPError as e:
            print(e.message)
        else:
            weather = json.loads(req.content)
            captured_date = iso8601.parse_date(weather['captured_at'])

            if previous_check is not None and captured_date <= previous_check:
                # Si ya mandamos esta información a MQTT salteamos una
                # iteración
                continue

            previous_check = captured_date

            msj = json.dumps({
                'mote_id': 'linti_control',
                'temperature': float(weather['temperature']),
                'current': 0,
                'movement': 0,
            })
            client.publish('linti/ipv6/temp', msj)

        time.sleep(60)
except Exception as e:
    time.sleep(60)
finally:
    # Pase lo que pase, aunque ocurra una excepción frenamos el thread
    # de PAHO MQTT
    client.loop_stop()
