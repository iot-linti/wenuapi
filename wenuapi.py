from eve import Eve
from eve_sqlalchemy import SQL
from influx_db_handler import InfluxDBHandler
from models.common import Base
import settings
import auth

app = Eve(data=SQL, settings=settings.SETTINGS, auth=auth.WenuBasicAuth)
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

Base.metadata.drop_all(db.engine)
Base.metadata.create_all(db.engine)


app.run(debug=True)
