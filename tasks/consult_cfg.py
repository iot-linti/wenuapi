from common_cfg import *
import random


mqtt_client_id = 'mqtt2influxdb' + '_{:04x}'.format(random.getrandbits(16))
