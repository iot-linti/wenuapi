from influxdb import InfluxDBClient
from .auth.token_auth import requires_auth
from flask import request
import json
from collections import OrderedDict
import string
import re

def make_query(query,client):
    result = client.query(query);
    #print result
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
    return measurements

def reParser(string):
    array = ['=']
    operators = ['<','>','<>','<=','>=']
    objects = re.findall(r"[><=]", string)
    if(objects):
        operator = ''.join(objects)
        result = operator in operators
        if result:
            value = string.partition(operator)
            string = value[2]
            array[0] = operator
    array.append(string)
    return array

def flask_to_influxdb_query(args):
    # FIXME: only supports simple where statements
    query_args = []
    where = args.get('where')
    if where is not None:
        where_args = json.loads(where, object_pairs_hook=OrderedDict)
        print where_args
        where_condition = []
        for key, val in where_args.items():
            valDic = reParser(val)
            print valDic
            where_condition.append(" {} {} {}".format(key,valDic[0],valDic[1]))
        if where_condition:
            query_args.extend(('WHERE', ' AND '.join(where_condition)))

    return ' '.join(query_args)


class InfluxDBHandler(object):
    def __init__(self, host, port, username, password, db, app):
        self.host = host
        self.username = username
        self.password = password
        self.influx = InfluxDBClient(host, port, username, password, db)
        app.route('/measurement/<mota_id>', methods=['GET'])(self.query)
        app.route('/measurement', methods=['GET'])(self.list)

    @requires_auth
    def list(self):
        query_filter = flask_to_influxdb_query(request.args)
        print query_filter
        query = "SELECT * FROM medicion {} ORDER BY time DESC LIMIT 50".format(query_filter)
        #query = "SELECT * FROM medicion WHERE mota_id = 'linti_cocina' ORDER BY time DESC LIMIT 50"
        print query
        measurements = make_query(query,self.influx)
        return json.dumps({'_items': measurements})

    @requires_auth
    def query(self,mota_id):
        query_filter = flask_to_influxdb_query(request.args)
        if not query_filter:
            query_filter = "WHERE mota_id ='%s'" % mota_id
        else:
            query_name = " AND mota_id ='%s'" % mota_id
            query_filter = query_filter + query_name
        query = "SELECT * FROM medicion {} ORDER BY time DESC LIMIT 50".format(query_filter)
        measurements = make_query(query,self.influx)
        return json.dumps({'_items': measurements})


