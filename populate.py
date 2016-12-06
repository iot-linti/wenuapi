import wenuclient
import random
import string

server = wenuclient.Server('http://localhost:5000')

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


server.Action(mote_id=1, command='turn_off', arguments='').create()
server.Action(mote_id=2, command='turn_off', arguments='').create()
server.Action(mote_id=3, command='turn_off', arguments='').create()
server.Action(mote_id=4, command='turn_off', arguments='').create()
