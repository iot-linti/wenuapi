import logging

from eve_sqlalchemy.decorators import registerSchema
from .models.action import Action
from .models.alert import Alert
from .models.user import User
from .models.role import Role
from .models.roletable import RoleTable
from .models.level import Level
from .models.camera import Camera, BasicIPCamera
from .models.measurement import Measurement
from .models.mote import Mote
from .models.role import Role
from .models.roletable import RoleTable
from .models.user import User
from eve_sqlalchemy.decorators import registerSchema
from secrets import database_username, database_password
from secrets import influxdb_username, influxdb_password

# Basic configuration
use_influxdb = True
influxdb_host = 'influxdb.linti.unlp.edu.ar'
influxdb_port = '8086'
influxdb_db = 'uso_racional'
# database_uri = 'sqlite://'
database_uri = 'mysql://{}:{}@localhost/wenuapi'.format(
    database_username,
    database_password,
)

# Only used in measurement by the moment
realm = 'eve'

# Register SQL_Alchemy schemas in EVE
registerSchema(User.__tablename__)(User)
registerSchema(Action.__tablename__)(Action)
registerSchema(Level.__tablename__)(Level)
registerSchema(Mote.__tablename__)(Mote)
registerSchema(Role.__tablename__)(Role)
registerSchema(RoleTable.__tablename__)(RoleTable)
registerSchema(Camera.__tablename__)(Camera)
registerSchema(Alert.__tablename__)(Alert)
registerSchema(BasicIPCamera.__tablename__)(BasicIPCamera)

action = Action._eve_schema['action']
user = User._eve_schema['user']
level = Level._eve_schema['level']
mote = Mote._eve_schema['mote']
role = Role._eve_schema['role']
roleTable = RoleTable._eve_schema['roletable']
camera = Camera._eve_schema['camera']
alert = Alert._eve_schema['alert']
basicIPCamera = BasicIPCamera._eve_schema['camera']

# Setup allowed methods and roles for each endpoint
action.update({
    'allowed_roles': ['admin', 'user'],
    'allowed_item_roles': ['admin', 'user'],
    'resource_methods': ['POST', 'GET'],
    'item_methods': ['GET', 'DELETE', 'PUT'],
})

mote.update({
    'allowed_roles': ['admin', 'user'],
    'allowed_item_roles': ['admin', 'user'],
    'resource_methods': ['POST', 'GET'],
    'item_methods': ['GET', 'DELETE', 'PUT'],
})

alert.update({
    'allowed_roles': ['admin', 'user'],
    'allowed_item_roles': ['admin', 'user'],
    'resource_methods': ['POST', 'GET'],
    'item_methods': ['GET', 'DELETE', 'PUT'],
})

#data_relation permite devolver los roles de cada usuario

# Only admin can access user and role information
user.update({
    'allowed_roles': ['admin'],
    'allowed_item_roles': ['admin'],
    'public_methods': ['POST'],
    'resource_methods': ['POST', 'GET', 'DELETE'],
    'item_methods': ['GET', 'DELETE', 'PUT'],
    'data_relation': {
        'resource': 'role',
        'field': '_id',
        'embeddable': True
    }
})

role.update({
    'allowed_roles': ['admin'],
    'allowed_item_roles': ['admin'],
    'resource_methods': ['POST', 'GET'],
    'item_methods': ['GET', 'DELETE', 'PUT'],
})

#Contiene las relaciones entre Users y Roles.
roleTable.update({
    'allowed_roles': ['admin'],
    'allowed_item_roles': ['admin'],
    'resource_methods': ['POST', 'GET'],
    'item_methods': ['GET', 'DELETE'],
})

level.update({
    'allowed_roles': ['admin', 'user'],
    'allowed_item_roles': ['admin', 'user'],
    'resource_methods': ['POST', 'GET'],
    'item_methods': ['GET', 'DELETE'],
})

DOMAIN = {
    'user': user,
    'action': action,
    'level': level,
    'mote': mote,
    'role': role,
    'roletable': roleTable,
    'camera': camera,
    'alert': alert,
    'basicIPCamera': basicIPCamera,
}

SETTINGS = {
    'DOMAIN':DOMAIN,
    'IF_MATCH' : False, # FIXME
    'DEBUG': True,
    'RESOURCE_METHODS': ['GET', 'POST'],
    'ITEM_METHODS': ['GET', 'PATCH', 'PUT', 'DELETE'],
    'SQLALCHEMY_DATABASE_URI': database_uri,
    'XML': False,
    'PAGINATION': True,
    'PAGINATION_LIMIT': 40,
    'SQLALCHEMY_TRACK_MODIFICATIONS': False
}


#Oculta la password y el token de los usuarios al hacer GET de user.
SETTINGS['DOMAIN']['user']['datasource']['projection']['password'] = 0
SETTINGS['DOMAIN']['user']['datasource']['projection']['token'] = 0

# These settings can be overrided by a local_settings.py module if present
try:
    from local_settings import *
except ImportError:
    logging.warning("No local settings found")
