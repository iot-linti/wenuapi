from influxdb import InfluxDBClient
from .auth import requires_auth
import json


class InfluxDBHandler(object):
    def __init__(self, host, port, username, password, db, app):
        self.host = host
        self.username = username
        self.password = password
        self.influx = InfluxDBClient(host, port, username, password, db)
        app.route('/measurement', methods=['GET'])(self.list)

    @requires_auth
    def list(self):
        result = self.influx.query(
            'SELECT * FROM medicion ORDER BY time DESC LIMIT 50'
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
