import imp
from sfss import db, Course
from sqlalchemy import func

db.drop_all()
db.create_all()
test1 = Course("DNI", 3, "not a real science course", "Consult Arts and Science.", None, None, None, None, None, None, "blah")
test2 = Course("YES", 3, "a real science course", "we do science in this class!", None, None, None, None, None, None, "blah")
db.session.add(test1)
db.session.add(test2)
db.session.commit()
test_raw = db.session.query(Course).filter(func.replace(Course.description, "Arts and Science", "").contains("science")).all()
db.drop_all()
