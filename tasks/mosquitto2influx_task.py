# -*- coding: utf-8 -*-
import json
import paho.mqtt.client as mqtt
import logging
import logging.handlers
from influxdb import InfluxDBClient

server = '163.10.10.118'
port = 1883
DELAY = 60

influx_user = ***REMOVED***
influx_password = '***REMOVED***'
influx_dbname = 'uso_racional'
influx_host = 'influxdb.linti.unlp.edu.ar'
influx_port = 8086
influx_measurement = 'medicion'

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
            'measurement': influx_measurement,
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
        influx_host,
        influx_port,
        influx_user,
        influx_password,
        influx_dbname,
    )
    client = mqtt.Client(client_id='mqtt2influxdb')
    client.on_message = to_influxdb(influxclient, logger)
    client.connect(server, port)
    client.subscribe('linti/ipv6/temp')
    client.loop_forever(timeout=1.0)

if __name__ == '__main__':
    mqtt2influxdb()
