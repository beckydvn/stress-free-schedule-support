from sfss.courses_database_conversion import Course
import nltk
from nltk.corpus import wordnet
from sqlalchemy import case, select
from sqlalchemy.sql.expression import true
from sfss import db

if __name__ == "__main__":
    """
    # references: 
    # https://www.guru99.com/wordnet-nltk.html
    # the NLTK textbook
    # https://www.nltk.org/howto/wordnet.html

    synset: set of words that share a common meaning.
    we want to retrieve all synsets that relate to the query; i.e. if the query is "friend"
    the synsets friend, ally, acquaintance, and supporter are returned as "friend"
    has many possible meanings.

    lemmas: within the synsets are "lemmas" that identify a specific sense of a word.
    i.e. supporter can be interpreted as a "champion," "admirer," "booster," etc.
    the lemma is also what you would see in a dictionary.

    hyponyms: the more general category the word fits into.

    hypernyms: the more specific version of the word.

    parts of speech: adjective, verb, noun, etc.
    """
    queries = ["math"]#, "english"]
    related_words = set()
    course_recs = []

    for query in queries:
        related_words.add(query)
        # we want to use all synsets, lemmas, hyponymms, hypernyms, and parts of speech
        # as search considerations.
        for syn in wordnet.synsets(query):
            related_words.update([l.name() for l in syn.lemmas()])
            # syn.hyponyms() and syn.hypernyms() return synsets as well
            related_words.update(*[w.lemma_names() for w in syn.hyponyms()])
            related_words.update(*[w.lemma_names() for w in syn.hypernyms()])
    related_words = [r.replace("_", " ") for r in related_words]
    remove_fac = False
    if "art" or "science" in related_words:
        remove_fac = True
    print(related_words)
    for r in related_words:
        #raw = Course.query.filter(Course.description.contains(r)).all()
        from sqlalchemy import func
        raw = db.session.query(Course).filter_by(func.lower(Course.description)==func.lower("GANYE")).first()
        course_recs.extend(raw)
        # if r == "art" or r == "science":
        #     for entry in raw:
        #         print(r, r in entry.description.replace("Arts and Science", ""))
        #         if r in entry.description.replace("Arts and Science", ""):
        #             course_recs.append(entry)
        # else:
        #     course_recs.extend(raw)

            #course_recs.extend(Course.query.filter((r in str(Course.description).replace("Arts and Science", "")) == True).all()) 
            #test = Course.description
            #course_recs.extend(db.session.query(Course).filter(r in str(Course.description) == True).all())
            # raw = select(Course).\
            #     where(
            #         case(
            #             Course.description.contains
            #         )
            #     )
            # Course.description.like("Arts and Science", "").contains(r)).all()

        #if remove_fac:
            #for i in range(len(raw)):

        #else:
        #   course_recs.extend(Course.query.filter(Course.description.contains(r)).all()) 
    print(f"{len(course_recs)} recommendations found:")
    for c in course_recs:
        print(f"id: {c.id}\ndescription: {c.description}")