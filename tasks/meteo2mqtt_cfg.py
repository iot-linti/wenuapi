from .common_cfg import *
import random
enable_task = True

data_url = 'http://clima.info.unlp.edu.ar/last?lang=es'
mqtt_sensor_id = 'linti_control'
mqtt_client_id = mqtt_sensor_id + '_{:04x}'.format(random.getrandbits(16))
seconds_between_checks = 60
