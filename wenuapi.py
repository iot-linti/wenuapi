from eve import Eve
from eve_sqlalchemy import SQL
from influx_db_handler import InfluxDBHandler
from models.common import Base
import settings

app = Eve(data=SQL, settings=settings.SETTINGS)
db = app.data.driver
Base.metadata.bind = db.engine
db.Model = Base
Base.metadata.create_all(db.engine)

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

app.run(debug=True)
