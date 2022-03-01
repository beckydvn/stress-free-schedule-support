from nltk.corpus import wordnet
from sfss import db, Course
from sqlalchemy import func
from typing import List

def get_query_results(queries: List[str]):
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
    print(related_words)
    # searches are case insensitive and include faculty names other than Arts and Science
    # (we choose to disclude Arts and Science as the faculty is too broad...)
    # reference: https://stackoverflow.com/questions/32124009/mysql-string-replace-using-sqlalchemy
    for r in related_words:
        course_recs.extend(db.session.query(Course).filter(func.replace(Course.description, "Arts and Science", "").contains(r)).all())

    print(f"{len(course_recs)} recommendations found:")
    for c in course_recs:
        print(f"id: {c.id}\ndescription: {c.description}")

get_query_results(["math"])