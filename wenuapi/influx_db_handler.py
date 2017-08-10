from influxdb import InfluxDBClient
from .auth.token_auth import requires_auth
from flask import request
import json
from collections import OrderedDict
import string
import re

translator = {
            'mote_id': 'mota_id',
            'current': 'corriente',
            'movement': 'movimiento',
            'temperature': 'temperatura',
            'voltage': 'voltaje',
            'time': 'time',
        }

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
    if not string.replace('.','',1).isdigit():
        string = "'" + string +"'"
    array.append(string)
    return array

def flask_to_influxdb_query(args, translator=translator):
    query = ""
    query_args = []
    where = args.get('where')
    order=offset=None
    limit = 40

    if args.get('sort') is not None:
        order = args.get('sort')
        if order[0] == '-':
            order_type = "DESC"
            order = order[1:]
        else:
            order_type = "ASC"
    if args.get('max_results') is not None:
        limit = int(args.get('max_results'))
    if args.get('page') is not None:
        offset = (int(args.get('page')) - 1) * limit

    if where is not None:
        where_args = json.loads(where, object_pairs_hook=OrderedDict)
        where_condition = []
        for key, val in where_args.items():
            if key in translator:
                valDic = reParser(val)
                where_condition.append("{} {} {}".format(translator[key],valDic[0],valDic[1]))
        if where_condition:
            query_args.extend(('WHERE', ' AND '.join(where_condition)))
            query = ' '.join(query_args)

    if order:
        query = "{} ORDER BY {} {}".format(query, order,order_type)
    if limit:
        query = "{} LIMIT {}".format(query,limit)
    if offset:
        query = "{} OFFSET {}".format(query,offset)

    return query

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
        #print query_filter
        query = "SELECT * FROM medicion {} ".format(query_filter)
        #query = "SELECT * FROM medicion WHERE mota_id = 'linti_cocina' ORDER BY mota_id DESC LIMIT 50"
        print query
        measurements = make_query(query,self.influx)
        return json.dumps({'_items': measurements})
