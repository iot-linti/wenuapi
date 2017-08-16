import json
from wenuclient import Client,get_session,register_user
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
    parameters = {
        "page" : 1,
        "sort" : "-time",
        "max_results" : 40,
    }

    parametersString = '&'.join('{}={}'.format(key, value) for key, value in parameters.items())

    measurements = server.Measurement.where(parametersString,**arg)
    print "-------- "
    for measure in measurements:
        print 'Mote id: {}'.format(measure.mote_id)
        print 'Temperature: {}'.format(measure.temperature)
        print 'Date: {}'.format(measure._created)
        print "--------"
