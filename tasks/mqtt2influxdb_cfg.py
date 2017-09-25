from common_cfg import *
from wenuapi.secrets import influxdb_username, influxdb_password
import random

influxdb_dbname = 'uso_racional'
influxdb_host = 'influxdb.linti.unlp.edu.ar'
influxdb_port = 8086
influxdb_measurement = 'medicion'
mqtt_client_id = 'mqtt2influxdb' + '_{:04x}'.format(random.getrandbits(16))
