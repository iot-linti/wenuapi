from eve_sqlalchemy.decorators import registerSchema
from models.action import Action
from models.user import User
from models.role import Role
from models.roletable import RoleTable
from models.level import Level
from models.measurement import Measurement
from models.mote import Mote
from secrets import database_username, database_password
from secrets import influxdb_username, influxdb_password


use_influxdb = True
influxdb_host = 'influxdb.linti.unlp.edu.ar'
influxdb_port = '8086'
influxdb_db = 'uso_racional'
#database_uri = 'sqlite://'
#database_uri = 'mysql://{}:{}@localhost/wenuapi2'.format(
database_uri = 'mysql://{}:{}@localhost/wenuapi'.format(
    database_username,
    database_password,
)

# Only used in measurement by the moment
realm = 'eve'

registerSchema(User.__tablename__)(User)
registerSchema(Action.__tablename__)(Action)
registerSchema(Level.__tablename__)(Level)
registerSchema(Mote.__tablename__)(Mote)
registerSchema(Role.__tablename__)(Role)
registerSchema(RoleTable.__tablename__)(RoleTable)

action = Action._eve_schema['action']
user =  User._eve_schema['user']
level = Level._eve_schema['level']
mote =  Mote._eve_schema['mote']
role = Role._eve_schema['role']
roleTable = RoleTable._eve_schema['roletable']

action.update({
    #'allowed_read_roles' : ['admino'],
    #'allowed_item_read_roles' : ['admi'],
    'allowed_roles': ['admin', 'user'],
    'allowed_item_roles': ['admin','user'],
    'resource_methods' : ['POST','GET'],
    'item_methods' : ['GET','DELETE','PUT'],
    })

user.update({
    'allowed_roles': ['admin'],
    'allowed_item_roles': ['admin'],
    'public_methods': ['POST'],
    'resource_methods' : ['POST','GET','DELETE'],
    'item_methods': ['GET','DELETE','PUT'],
    'data_relation' : {'resource': 'role',
                      'field': '_id',
                      'embeddable': True}
    })

role.update({
    'allowed_roles': ['admin'],
    'allowed_item_roles': ['admin'],
    'resource_methods': ['POST','GET'],
    'item_methods': ['GET','DELETE','PUT'],
    })

roleTable.update({
    'allowed_roles': ['admin'],
    'allowed_item_roles': ['admin'],
    'resource_methods': ['POST','GET'],
    'item_methods' : ['GET','DELETE'],
    })

level.update({
    'allowed_roles': ['admin', 'user'],
    'allowed_item_roles': ['admin','user'],
    'resource_methods' : ['POST','GET'],
    'item_methods' : ['GET','DELETE'],
    })

DOMAIN = {
    'user' : user,
    'action': action,
    'level': level,
    'mote': mote,
    'role': role,
    'roletable': roleTable,
    }

SETTINGS = {
    'DOMAIN':DOMAIN,
    'IF_MATCH' : False,
    'DEBUG': True,
    #'PUBLIC_METHODS': ['GET', 'POST'],
    #'PUBLIC_ITEM_METHODS': ['GET', 'PATCH'],
    'RESOURCE_METHODS': ['GET', 'POST'],
    'ITEM_METHODS' : ['GET', 'PATCH', 'PUT', 'DELETE'],
    'SQLALCHEMY_DATABASE_URI': database_uri,
    'XML': False,
    'PAGINATION' : True,
    'PAGINATION_LIMIT' : 40,
    #'SERVER_NAME' : 'Wenuapi2',
    }

SETTINGS['DOMAIN']['user']['datasource']['projection']['password'] = 0
SETTINGS['DOMAIN']['user']['datasource']['projection']['token'] = 0
#SETTINGS['DOMAIN']['user']['authentication'] = auth.MyBasicAuth
#SETTINGS['DOMAIN']['role']['authentication'] = auth.MyBasicAuth
#SETTINGS['DOMAIN']['roletable']['authentication'] = auth.MyBasicAuth
