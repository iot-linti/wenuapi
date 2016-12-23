from . import auth
from . import settings
from .influx_db_handler import InfluxDBHandler
from .models.common import Base
from eve import Eve
from eve_sqlalchemy import SQL

def build_app(disable_auth=False):
    parameters = {
        'data': SQL,
        'settings': settings.SETTINGS,
    }
    if not disable_auth:
        parameters['auth'] = auth.WenuBasicAuth

    app = Eve(**parameters)
    db = app.data.driver
    Base.metadata.bind = db.engine
    db.Model = Base

    if settings.use_influxdb:
        # Register influx for /measurements
        influx_handler = InfluxDBHandler(
            settings.influxdb_host,
            settings.influxdb_port,
            settings.influxdb_username,
            settings.influxdb_password,
            settings.influxdb_db,
            app,
        )
    else:
        registerSchema(Measurement.__tablename__)(Measurement)
        settings.SETTINGS['DOMAIN']['measurement'] = Measurement._eve_schema['measurement']

    return app
