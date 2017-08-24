# -*- coding: utf-8 -*-
from influxdb import InfluxDBClient
from .mqtt2influxdb_cfg import *
import json
import logging
import logging.handlers
import paho.mqtt.client as mqtt

def to_influxdb(influxclient, logger):
    def handler(client, userdata, msg):
        logger.debug('Message received from %s', userdata)
        logger.debug('Message text: %s', msg.payload)
        try:
            msg = json.loads(msg.payload)
        except ValueError as e:
            logger.error('Error decoding MQTT message: %s', e)
            return

        data_points = [{
            'measurement': influxdb_measurement,
            'tags': {'mota_id': msg['mote_id']},
            'fields': {
                'temperatura': float(msg['temperature']),
                'movimiento': int(msg['movement']) == 1,
                'corriente': int(msg['current']),
            }
        }]
        if 'voltage' in msg:
            data_points[0]['fields']['voltaje'] = int(msg['voltage'])

        influxclient.write_points(data_points)

    return handler


def run():
    logging.basicConfig(
        level=logging.DEBUG,
        format='[%(levelname)s] (mqtt2influxdb) %(message)s',
    )
    logger = logging.getLogger('mqtt2influxdb')
    logger.addHandler(logging.handlers.SysLogHandler(address='/dev/log'))


    influxclient = InfluxDBClient(
        influxdb_host,
        influxdb_port,
        influxdb_user,
        influxdb_password,
        influxdb_dbname,
    )
    client = mqtt.Client(client_id=mqtt_client_id)
    client.on_message = to_influxdb(influxclient, logger)
    client.connect(mqtt_server, mqtt_port)
    client.subscribe(mqtt_topic)
    client.loop_forever(timeout=1.0)

if __name__ == '__main__':
    mqtt2influxdb()
