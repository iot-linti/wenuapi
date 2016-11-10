from eve import Eve
from eve_sqlalchemy import SQL
import settings
from models.common import Base

app = Eve(data=SQL, settings=settings.SETTINGS)
db = app.data.driver
Base.metadata.bind = db.engine
db.Model = Base
Base.metadata.create_all(db.engine)

app.run(debug=True)
