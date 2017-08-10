from sqlalchemy_utils.types import Password
from unittest import TestCase
from . import testdb
from ..wenuapi.models.common import Base
from ..wenuapi.influx_db_handler import flask_to_influxdb_query

class TestInfluxDBAdapter(TestCase):
    def setUp(self):
        engine, self.session = testdb()
        Base.metadata.create_all(engine)

        self.username = 'regular'
        self.password = '1234'
        self.translator = {
            'a': 'a',
            'b': 'b',
            'g': 'g',
            'z': 'z',
        }

        # self.user = User(username=self.username, password=self.password)
        # self.session.add(self.user)
        # self.session.commit()

    def test_translate_simple_where(self):
        self.assertEqual(
            flask_to_influxdb_query({'where': '{"a": "b"}', 'max_results': 40}, translator=self.translator),
            "WHERE a = 'b' LIMIT 40",
        )

    def test_translate_where_with_several_conditions(self):
        self.assertEqual(
            flask_to_influxdb_query({'where': '{"a": "b", "g": "i", "z": "x"}', 'max_results': 40}, translator=self.translator),
            "WHERE a = 'b' AND g = 'i' AND z = 'x' LIMIT 40",
        )

    def test_translate_where_with_string_values(self):
        self.assertEqual(
            flask_to_influxdb_query({'where': '{"a": "b"}', 'max_results':40}, translator=self.translator),
            "WHERE a = 'b' LIMIT 40",
        )
