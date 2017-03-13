from influxdb import InfluxDBClient
from .auth import requires_auth
from flask import request
import json
from collections import OrderedDict


def flask_to_influxdb_query(args):
    # FIXME: only supports simple where statements
    query_args = []
    where = args.get('where')
    if where is not None:
        where_args = json.loads(where, object_pairs_hook=OrderedDict)
        where_condition = []
        for key, val in where_args.items():
            where_condition.append('{} = {}'.format(key, val))
        if where_condition:
            query_args.extend(('WHERE', ' AND '.join(where_condition)))

    return ' '.join(query_args)


class InfluxDBHandler(object):
    def __init__(self, host, port, username, password, db, app):
        self.host = host
        self.username = username
        self.password = password
        self.influx = InfluxDBClient(host, port, username, password, db)
        app.route('/measurement', methods=['GET'])(self.list)

    @requires_auth
    def list(self):
        query_filter = flask_to_influxdb_query(request.args)
        result = self.influx.query(
            'SELECT * FROM medicion {} ORDER BY time DESC LIMIT 50'.format(
                query_filter,
            )
        )
        measurements = []
        for data_point in result.get_points():
            measurements.append({
                'mote_id': data_point['mota_id'],
                'current': data_point['corriente'],
                'movement': data_point['movimiento'],
                'temperature': data_point['temperatura'],
                'voltage': data_point['voltaje'],
                '_created': data_point['time'],
                '_updated': data_point['time'],
            })
        return json.dumps({'_items': measurements})
