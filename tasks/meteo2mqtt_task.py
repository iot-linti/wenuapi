#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from .meteo2mqtt_cfg import *
import iso8601
import json
import logging
import logging.handlers
import paho.mqtt.client as mqtt
import requests
import time

def run():
    logging.basicConfig(
        level=logging.WARNING,
        format='[%(levelname)s] (meteo2mqtt) %(message)s',
    )
    logger = logging.getLogger('meteo2mqtt')
    logger.addHandler(logging.handlers.SysLogHandler(address='/dev/log'))

    client = mqtt.Client(client_id=mqtt_client_id)
    client.connect(mqtt_server, mqtt_port)
    client.loop_start()  # Maneja eventos y reconexiones

    previous_check = None

    URL = data_url
    try:
        while True:
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
                    time.sleep(seconds_between_checks)
                    continue

                previous_check = captured_date

                msj = json.dumps({
                    'mote_id': mqtt_sensor_id,
                    'temperature': float(weather['temperature']),
                    'current': 0,
                    'movement': 0,
                })
                logger.debug('Publicando en servidor MQTT %s:%d', mqtt_server, mqtt_port)
                client.publish(mqtt_topic, msj)

            time.sleep(seconds_between_checks)
    finally:
        # Pase lo que pase, aunque ocurra una excepción frenamos el thread
        # de PAHO MQTT
        client.loop_stop()
