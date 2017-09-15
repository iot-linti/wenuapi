from .auth import token_auth
from . import settings
from .influx_db_handler import InfluxDBHandler
from .camera_app import init_camera_app
from .models.common import Base
from .views.mote import init_mote_app
from eve import Eve
from eve_sqlalchemy import SQL
from eve_sqlalchemy.validation import ValidatorSQL
from . import tasks
from . import register
import os

def build_app(disable_auth=False):
    folder = os.path.dirname(os.path.abspath(__file__))
    parameters = {
        'validator':ValidatorSQL,
        'data': SQL,
        'settings': settings.SETTINGS,
        'template_folder':  folder + "/templates"
    }
    if not disable_auth:
        parameters['auth'] = token_auth.TokenAuth
    
    app = Eve(**parameters)
    tasks.set_on_insert_account_token(app)
    register.log_user(app)

    db = app.data.driver
    Base.metadata.bind = db.engine
    db.Model = Base
    db.create_all()

    init_camera_app(app=app)
    init_mote_app(app=app)

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
        from eve_sqlalchemy.decorators import registerSchema
        from .models.measurement import Measurement
        registerSchema(Measurement.__tablename__)(Measurement)
        settings.SETTINGS['DOMAIN']['measurement'] = Measurement._eve_schema['measurement']

    return app
