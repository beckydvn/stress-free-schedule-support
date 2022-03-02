from nltk.corpus import wordnet
from sfss import db, Course
from sqlalchemy import func, and_, or_
from typing import List

def choose_semantic_meaning(query):
    possible_synsets = wordnet.synsets(query)
    if len(possible_synsets) > 1:
        output_str = "Do you mean:\n"
        for count, val in enumerate(possible_synsets):
            output_str += f"{count + 1}: {val.name()}\t{val.definition()}\n"
        print(output_str)
        chosen = int(input("Pick which semantic meaning of your query you wish to search:\t"))
        return possible_synsets[chosen - 1]
    return possible_synsets[0]

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
    # TODO: (possibly) return a dict with the course selected mapped to the highlighted word(s) that
    # prompted the result. send these words to HTML through the controller to highlight/italicize/whatever.

    course_recs = {}
    related_words = {}
    for query in queries:
        related_words[query] = set()
        related_words[query].add(query)
        # we want to consider all synsets, lemmas, hyponyms, hypernyms.
        syn = choose_semantic_meaning(query)
        related_words[query].update([l.name() for l in syn.lemmas()])
        # syn.hyponyms() and syn.hypernyms() return synsets as well
        related_words[query].update(*[w.lemma_names() for w in syn.hyponyms()])
        related_words[query].update(*[w.lemma_names() for w in syn.hypernyms()])
        related_words[query] = {val.replace("_", " ") for val in related_words[query]}

    """ 
    searches are case insensitive and include faculty names other than Arts and Science
    (we choose to disclude Arts and Science as the faculty is too broad...)
    also, we force that the whole word is contained by using spaces (to avoid matching unrelated words
    that happen to have a smaller related word nested in its spelling...)
    reference: https://stackoverflow.com/questions/32124009/mysql-string-replace-using-sqlalchemy
    """
    
    filter_list = []
    # for a search to be viable, it must contain at least one word from each query category
    for query in related_words:
        # all the entries that contain any value from this query
        test = [func.replace(Course.description, "Arts and Science", "").contains(f" {v} ") for v in related_words[query]]
        filter_list.append(or_(*test))
    course_recs = db.session.query(Course).filter(and_(*filter_list)).all()

    print(f"{len(course_recs)} recommendations found:\n")
    for c in course_recs:
       print(c.description)

    return course_recs
