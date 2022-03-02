from sfss import db, Course
from sqlalchemy import func, or_, and_

def test_art_sci_exclusion():
    db.create_all()
    test1 = Course("DNI", 3, "not a real science course", "Consult Arts and Science.", None, None, None, None, None, None, "blah")
    test2 = Course("YES", 3, "a real science course", "we do science in this class!", None, None, None, None, None, None, "blah")
    db.session.add(test1)
    db.session.add(test2)
    db.session.commit()
    assert db.session.query(Course).filter(func.replace(Course.description, "Arts and Science", "").contains("science")).all() == [test2]
    db.drop_all()

def test_narrow_db_search():
    db.create_all()
    related_words_test = {"math": ["mathematics", "statistics"], "english": ["english"]}
    filter_list = []
    for query in related_words_test:
        # all the entries that contain any value from this query
        test = [func.replace(Course.description, "Arts and Science", "").contains(f"{v}") for v in related_words_test[query]]
        filter_list.append(or_(*test))
    query = db.session.query(Course).filter(and_(*filter_list)).all()
    for q in query:
        assert "mathematics" in q.description.lower() and "statistics" in q.description.lower() and "english" in q.description.lower()
    db.drop_all() 
