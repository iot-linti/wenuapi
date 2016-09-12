#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import json
import paho.mqtt.client as mqtt
import requests
import time
import iso8601

server = '163.10.20.206'
port = 1883
DELAY = 60

while True:
    try:
        client = mqtt.Client(client_id='linti_control')
        client.connect(server, port)
        client.loop_start()  # Maneja eventos y reconexiones

        previous_check = None

        while True:
            URL = 'http://clima.info.unlp.edu.ar/last?lang=es'
            req = requests.get(URL)
            weather = json.loads(req.content)
            captured_date = iso8601.parse_date(weather['captured_at'])

            if previous_check is not None and captured_date <= previous_check:
                # Si ya mandamos esta información a MQTT salteamos una
                # iteración
                time.sleep(DELAY)
                continue

            previous_check = captured_date

            msj = json.dumps({
                'mote_id': 'linti_control',
                'temperature': float(weather['temperature']),
                'current': 0,
                'movement': 0,
            })
            client.publish('linti/ipv6/temp', msj)

    except Exception as e:
        print(str(e))
    finally:
        time.sleep(DELAY)

# Detener el thread de PAHO MQTT
client.loop_stop()
