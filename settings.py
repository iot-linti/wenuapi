from models.common import User
from models.action import Action
from models.level import Level
from models.measurement import Measurement
from models.mote import Mote
from eve_sqlalchemy.decorators import registerSchema

registerSchema(User.__tablename__)(User)
registerSchema(Action.__tablename__)(Action)
registerSchema(Level.__tablename__)(Level)
registerSchema(Measurement.__tablename__)(Measurement)
registerSchema(Mote.__tablename__)(Mote)

SETTINGS = {
    'DOMAIN': {
        'user': User._eve_schema['user'],
        'action': Action._eve_schema['action'],
        'level': Level._eve_schema['level'],
        'measurement': Measurement._eve_schema['measurement'],
        'mote': Mote._eve_schema['mote'],
    },
    'RESOURCE_METHODS': ['GET', 'POST'],
}
