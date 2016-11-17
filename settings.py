from eve_sqlalchemy.decorators import registerSchema
from models.action import Action
from models.common import User
from models.level import Level
from models.measurement import Measurement
from models.mote import Mote
from secrets import influxdb_username, influxdb_password

use_influxdb = True
influxdb_host = 'influxdb.linti.unlp.edu.ar'
influxdb_port = '8086'
influxdb_db = 'uso_racional'

registerSchema(User.__tablename__)(User)
registerSchema(Action.__tablename__)(Action)
registerSchema(Level.__tablename__)(Level)
if not use_influxdb:
    registerSchema(Measurement.__tablename__)(Measurement)
registerSchema(Mote.__tablename__)(Mote)

SETTINGS = {
    'DOMAIN': {
        'user': User._eve_schema['user'],
        'action': Action._eve_schema['action'],
        'level': Level._eve_schema['level'],
        'mote': Mote._eve_schema['mote'],
    },
    'RESOURCE_METHODS': ['GET', 'POST'],
}

if not use_influxdb:
    SETTINGS['DOMAIN']['measurement'] = Measurement._eve_schema['measurement']
