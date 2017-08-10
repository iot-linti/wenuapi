import wenuclient
import random
import string
from wenuapi.models.role import Role

url = 'http://localhost:8080'
client = wenuclient.Client(url)

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
    moteobj = client.Mote(**mote)
    moteobj.create()

levels = [{
    'map': random.choice(string.ascii_letters),
} for i in range(5)]

for level in levels:
    levelobj = client.Level(**level)
    levelobj.create()

roleResponse = client.Role(rolename = 'admin').create()
client.Role(rolename='user').create()
userResponse = client.User(username='admin', password= "1234").create()

client.Roletable(user_id = userResponse.get('_id'),role_id = roleResponse.get('_id')).create()

client.Action(mote_id=1, command='turn_off', arguments='').create()
client.Action(mote_id=2, command='turn_off', arguments='').create()
client.Action(mote_id=3, command='turn_off', arguments='').create()
client.Action(mote_id=4, command='turn_off', arguments='').create()
