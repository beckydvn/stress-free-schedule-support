import itertools
from nltk.corpus import wordnet
from sfss import db, Course
from sqlalchemy import func, and_, or_
from typing import List
import json
import ast

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

def faculty_translator(input):
    translator = {
        "anatomy": "ANAT",
        "anishinaabe": "ANSH",
        "arabic": "ARAB",
        "art": "ARTF",
        "fine arts": "ARTF",
        "art history": "ARTF",
        "astronomy": "ASTR",
        "biochemistry": "BCHM",
        "biology": "BIOL",
        "cancer": "CANC",
        "chemistry": "CHEM",
        "chinese": "CHIN",
        "computer": "CISC",
        "computing": "CISC",
        "computer science": "CISC",
        "classical literature": "CLST",
        "cognitive science": "COGS",
        "cognitive": "COGS",
        "creative writing": "CWRI",
        "developmoent": "DEVS",
        "drama": "DRAM",
        "economics": "ECON",
        "employment relations": "EMPR",
        "english": "ENGL",
        "entrepreneur": "ENIN",
        "environment sciences": "ENSC",
        "epidemiology" : "EPID",
        "film": "FILM",
        "french": "FREN",
        "geology": "GEOL",
        "gender": "GNDS",
        "geography": "GPHY",
        "greek": "GREK",
        "german": "GRMN",
        "hebrew": "HEBR",
        "history": "HIST",
        "health": "HLTH",
        "humanities": "IDIS",
        "indigenous" : "INDG",
        "global": "INTS",
        "italian": "ITLN",
        "japanese": "JAPN",
        "kinesiology": "KNPE",
        "language": "LANG",
        "latin": "LATN",
        "linguistics": "LING",
        "life sciences": "LISC",
        "cultures": "LLCU",
        "media and performance": "MAPP",
        "math": "MATH",
        "microbiology": "MICR",
        "mohawk": "MOHK",
        "music": "MUSC",
        "musical theater": "MUTH",
        "neurosciencee": "NSCI",
        "pathology": "PATH",
        "pharmacology": "PHAR",
        "physiology": "PHGY",
        "philosophy": "PHIL",
        "physics": "PHYS",
        "politics": "POLS",
        "political science": "POLS",
        "psychology": "PSYC",
        "religion": "RELS",
        "sociology": "SOCY",
        "spanish": "SPAN",
        "statistics": "STAT",
        "writing": "WRIT",

    }
    input = input.lower()
    if input in translator.keys():
        return translator[input.lower()]
    return None

def get_query_results(queries: List[str]):
    """
    references: 
    https://www.guru99.com/wordnet-nltk.html
    https://www.nltk.org/howto/wordnet.html
    https://stackoverflow.com/questions/32124009/mysql-string-replace-using-sqlalchemy
    https://stackoverflow.com/questions/66591809/filter-a-sqlalchemy-query-by-field-that-contains-a-substring-from-a-list
    and of course, the NLTK textbook!

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

    related_words = {}
    for query in queries:
        related_words[query] = {query}
        # print(query)
        # print(wordnet.synsets(query))
        synsets = (wordnet.synsets(query))
        for syn in synsets:
            related_words[query].add(query)
            # we want to consider all synsets, lemmas, hyponyms, hypernyms.
            #syn = choose_semantic_meaning(query)
            related_words[query].update([l.name() for l in syn.lemmas()])
            # syn.hyponyms() and syn.hypernyms() return synsets as well
            related_words[query].update(*[w.lemma_names() for w in syn.hyponyms()])
            related_words[query].update(*[w.lemma_names() for w in syn.hypernyms()])
            related_words[query] = {val.replace("_", " ") for val in related_words[query]}

    """ 
    searches are case insensitive and include faculty names other than Arts and Science
    (we choose to disclude Arts and Science as the faculty is too broad...)
    """

    filter_list = []
    # if we have multiple search terms, prioritize courses that fit the broader range of categories
    if len(related_words) > 1:
        # add results that include all search keywords in the description
        print([i for i in itertools.combinations(related_words, 2)])
        filter_list.extend(db.session.query(Course).filter(and_(*[func.replace(Course.description, "Arts and Science", "").contains(query) for query in related_words])).all())
        # add results that include pairs of keywords in the description
        for combo in itertools.combinations(related_words, 2):
            filter_list.extend(db.session.query(Course).filter(and_(*[func.replace(Course.description, "Arts and Science", "").contains(c) for c in combo])).all())
    # add results where the keywords are in the COURSE CODE
    for query in related_words:
        translation = faculty_translator(query)
        if translation:
            filter_list.extend(db.session.query(Course).filter(Course.id.contains(translation)).all())
    
    # add results where the keywords are in the NAME
    for query in related_words:
        filter_list.extend(db.session.query(Course).filter(Course.course_name.contains(query)).all())
    # then add results that contain the direct keywords individually in their description
    for query in related_words:
        filter_list.extend(db.session.query(Course).filter(func.replace(Course.description, "Arts and Science", "").contains(query)).all())

    # finally, add any that have related words in their description
    for query in related_words:
        for v in related_words[query]:
            filter_list.extend(db.session.query(Course).filter(func.replace(Course.description, "Arts and Science", "").contains(v)).all())
    return json.dumps(ast.literal_eval(str({d.id : d.toJSON() for d in filter_list})))


if __name__ == "__main__":
    course_recs = get_query_results(["math", "english"], False)
    print(f"{len(course_recs)} recommendations found:\n")
    for c in course_recs:
        print(c.toJSON())
       #print(str(c), "\n")
    course_recs = get_query_results(["math", "english"], True)
    print(f"{len(course_recs)} recommendations found:\n")
    for c in course_recs:
        print(c.toJSON())
       #print(str(c), "\n")
