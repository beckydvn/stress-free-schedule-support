from sfss import db
from sfss.courses_database_conversion import Courses

db.create_all()
db.session.add(Courses("ANAT", 3.0, "test", ["1", "2"], None, None))
db.session.commit()
print(Courses.query.all())

