from functools import wraps
import json
import requests


def validate_and_jsonify(func):
    @wraps(func)
    def closure(self, route, *args, **kwargs):
        http_request = func(self, route, *args, **kwargs)
        assert http_request.status_code == 200 or http_request.status_code == 201
        return json.loads(http_request.text)

    return closure


class Entity(object):
    def __init__(self, **kwargs):
        self.fields = kwargs

    def __getattr__(self, attr):
        return self.fields[attr]

    @classmethod
    def spawn_subclass(cls, title, link, server):
        entity = type(str(title), (cls,), {
            'server': server,
            'link': link,
        })
        return entity

    @classmethod
    def list(cls):
        return [cls(**entry) for entry in cls.server.get(cls.link)['_items']]

    @classmethod
    def get_by_id(cls, _id):
        return cls(**cls.server.get('{}/{}'.format(cls.link, _id)))

    def __str__(self):
        return str(self.fields)

    def commit(self):
        response = self.server.post(self.link, json=self.fields)
        self.fields.update(response)
        return response


class Server(object):
    def __init__(self, url, session=None):
        if session is None:
            self.session = requests.Session()
        else:
            self.session = session

        self.url = url
        self.entities = self._spawn_entities()

    def _validate(self, response):
        assert response.status_code == 200

    def _spawn_entities(self):
        http_response = self.session.get(self.url)
        self._validate(http_response)
        response = json.loads(http_response.text)
        titles = []

        for child in response['_links']['child']:
            title = child['title'].title().replace('_', '')
            titles.append(title)
            setattr(self, title, Entity.spawn_subclass(
                title=title,
                link=child['href'],
                server=self,
            ))

        return titles

    @validate_and_jsonify
    def get(self, route):
        return self.session.get('/'.join((self.url, route)))

    @validate_and_jsonify
    def put(self, route):
        return self.session.put('/'.join((self.url, route)))

    @validate_and_jsonify
    def post(self, route, json):
        return self.session.post('/'.join((self.url, route)), json=json)

    @validate_and_jsonify
    def delete(self, route):
        return self.session.delete('/'.join((self.url, route)))


if __name__ == '__main__':
    s = Server('http://localhost:5000')
    print(s.entities)
    print(s.Mote)
    print(s.Mote.list())
