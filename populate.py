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
} for i in range(10) for j in range(5)]

levels = [{
    '_id': i,
    'map': random.choice(string.ascii_letters),
} for i in range(5)]

for mote in motes:
    moteobj = server.Mote(**mote)
    moteobj.commit()

for level in levels:
    levelobj = server.Level(**level)
    levelobj.commit()
