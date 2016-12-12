from eve_sqlalchemy.decorators import registerSchema
from models.action import Action
from models.user import User
from models.level import Level
from models.measurement import Measurement
from models.mote import Mote
from secrets import database_username, database_password
from secrets import influxdb_username, influxdb_password

use_influxdb = True
influxdb_host = 'influxdb.linti.unlp.edu.ar'
influxdb_port = '8086'
influxdb_db = 'uso_racional'
database_uri = 'mysql://{}:{}@localhost/wenu'.format(
    database_username,
    database_password,
)

registerSchema(User.__tablename__)(User)
registerSchema(Action.__tablename__)(Action)
registerSchema(Level.__tablename__)(Level)
registerSchema(Mote.__tablename__)(Mote)

SETTINGS = {
    'DOMAIN': {
        'action': Action._eve_schema['action'],
        'level': Level._eve_schema['level'],
        'mote': Mote._eve_schema['mote'],
    },
    'RESOURCE_METHODS': ['GET', 'POST'],
    'ITEM_METHODS': ['GET', 'PUT'],
    'SQLALCHEMY_DATABASE_URI': database_uri,
}

