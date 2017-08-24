#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import json
import paho.mqtt.client as mqtt
import requests
import time
import iso8601
import logging
import logging.handlers

logging.basicConfig(
    level=logging.WARNING,
    format='[%(levelname)s] (meteo2mqtt) %(message)s',
)
logger = logging.getLogger('meteo2mqtt')
logger.addHandler(logging.handlers.SysLogHandler(address='/dev/log'))

server = 'localhost'
port = 1883
DELAY = 60

client = mqtt.Client(client_id='linti_control')
client.connect(server, port)
client.loop_start()  # Maneja eventos y reconexiones

previous_check = None

try:
    while True:
        URL = 'http://clima.info.unlp.edu.ar/last?lang=es'
        try:
            logger.debug('Petición al servidor de clima %s', URL)
            req = requests.get(URL)
        except requests.exceptions.HTTPError as e:
            logger.error('Conectandose a %s: %s', URL, e)
        else:
            logger.debug('Decodificación de la respuesta')
            weather = json.loads(req.content)
            req.close()  # Para evitar el CLOSE_WAIT, pero no funciona
            captured_date = iso8601.parse_date(weather['captured_at'])

            if previous_check is not None and captured_date <= previous_check:
                # Si ya mandamos esta información a MQTT salteamos una
                # iteración
                logger.debug('Mensaje con fecha %s ya procesado',  weather['captured_at'])
                time.sleep(DELAY)
                continue

            previous_check = captured_date

            msj = json.dumps({
                'mote_id': 'linti_control',
                'temperature': float(weather['temperature']),
                'current': 0,
                'movement': 0,
            })
            logger.debug('Publicando en servidor MQTT %s:%d', server, port)
            client.publish('linti/ipv6/temp', msj)

        time.sleep(DELAY)
finally:
    # Pase lo que pase, aunque ocurra una excepción frenamos el thread
    # de PAHO MQTT
    client.loop_stop()
