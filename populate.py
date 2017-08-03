import wenuclient
import random
import string
from wenuapi.models.role import Role

server = wenuclient.Client('http://localhost:8080')

motes = [{
    'level_id': i,
    'mote_id': 'aula_' + random.choice(string.ascii_letters),
    'resolution': '({},{})'.format(
        random.randrange(0, 2600),
        random.randrange(0, 2600)
    ),
    'x': random.randrange(0, 2600),
    'y': random.randrange(0, 2600),
} for i in range(1, 11) for j in range(5)]


for mote in motes:
    moteobj = server.Mote(**mote)
    moteobj.create()

levels = [{
    'map': random.choice(string.ascii_letters),
} for i in range(5)]

for level in levels:
    levelobj = server.Level(**level)
    levelobj.create()

roleResponse = server.Role(rolename = 'admin').create()
server.Role(rolename='user').create()
userResponse = server.User(username='admin', password= "1234").create()

server.Roletable(user_id = userResponse.get('_id'),role_id = roleResponse.get('_id')).create()

server.Action(mote_id=1, command='turn_off', arguments='').create()
server.Action(mote_id=2, command='turn_off', arguments='').create()
server.Action(mote_id=3, command='turn_off', arguments='').create()
server.Action(mote_id=4, command='turn_off', arguments='').create()
