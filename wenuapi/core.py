from .auth import token_auth
from . import settings
from .influx_db_handler import InfluxDBHandler
from .camera_app import init_camera_app
from .models.common import Base
from eve import Eve
from eve_sqlalchemy import SQL
from eve_sqlalchemy.validation import ValidatorSQL
from . import tasks
from . import register

def build_app(disable_auth=False):
    '''Build WSGI APP setting up the DB and EVE'''
    parameters = {
        'validator':ValidatorSQL,
        'data': SQL,
        'settings': settings.SETTINGS,
    }

    # Auth via tokens is enabled by default
    if not disable_auth:
        parameters['auth'] = token_auth.TokenAuth

    # Setup EVE
    app = Eve(**parameters)

    # Eve automatic token creation and role assigment when a user is
    # inserted.
    tasks.set_on_insert_account_token(app)
    register.log_user(app)

    # Setup DB engine
    db = app.data.driver
    Base.metadata.bind = db.engine

    # Bind the model to the engine and create tables if needed
    db.Model = Base
    db.create_all()

    # Add a route to fetch camera frames in order to do a visual
    # inspection of the monitored room
    init_camera_app(app=app)

    # Measurements can be stored either on InfluxDB or in a relational
    # DB, depending on the user configuration.
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
        # Use a relational DB for measurements
        from eve_sqlalchemy.decorators import registerSchema
        from .models.measurement import Measurement
        registerSchema(Measurement.__tablename__)(Measurement)
        settings.SETTINGS['DOMAIN']['measurement'] = Measurement._eve_schema['measurement']

    return app
