from sfss.courses_database_conversion import Course
# from nltk import similar

if __name__ == "__main__":
    queries = ["math", "english"]
    # queries.extend()
    test = Course.query.filter(Course.description.contains(queries[0])).all()
    print(test)