from sfss import db
from sfss.courses_database_conversion import create_database

db.drop_all()
db.create_all()
create_database()
