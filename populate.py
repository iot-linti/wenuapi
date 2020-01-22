'''Helper script to fill te DB with random data. This script
can be used to check the installation of WenuAPI and the DB
configuration'''
import wenuclient
import random
import string
from wenuapi.models.role import Role

url = 'http://localhost:8080'
client = wenuclient.Client(url)

# Fake mote information
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


# Insert mote fake mote information in the DB
for mote in motes:
    moteobj = client.Mote(**mote)
    moteobj.create()

# Fake level information
levels = [{
    'map': random.choice(string.ascii_letters),
} for i in range(5)]

# Insert fake information about different levels on a building
for level in levels:
    levelobj = client.Level(**level)
    levelobj.create()

# Create an admin group
roleResponse = client.Role(rolename = 'admin').create()
# Create a non-admin group
client.Role(rolename='user').create()

# Create an administrator user
userResponse = client.User(username='admin', password= "1234").create()
client.Roletable(user_id = userResponse.get('_id'),role_id = roleResponse.get('_id')).create()

# Insert a series of commands for the fake motes
client.Action(mote_id=1, command='turn_off', arguments='').create()
client.Action(mote_id=2, command='turn_off', arguments='').create()
client.Action(mote_id=3, command='turn_off', arguments='').create()
client.Action(mote_id=4, command='turn_off', arguments='').create()
