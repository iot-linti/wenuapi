import json
from wenuapi2.wenuclient import Client,get_session,register_user
import requests

url = 'http://localhost:8080'
username = 'admin'
password = 1234
#register_user('{}/user'.format(url),username,password)

try:
    s = get_session('{}/login'.format(url),username,password)
    server = Client('{}'.format(url),s)


except AssertionError:
    print 'ASSERT'
except requests.HTTPError:
    print 'EXCEPTION'
else:
    #server.Measurement.list()
    arg = {
        "mote_id" : "linti_cocina",
        "temperature" : ">24.19",
    }
    parametersString = 'page=2\
&sort=-time\
&max_results=10'


    measurements = server.Measurement.where(parametersString,**arg)
    print "-------- "
    for measure in measurements:
        print 'Mote id: {}'.format(measure.__getattr__('mote_id'))
        print 'Temperature: {}'.format(measure.__getattr__('temperature'))
        print 'Date: {}'.format(measure.__getattr__('_created'))
        print "--------"

