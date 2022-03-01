from multiprocessing import Value
from typing import List
from sfss import db


class Course(db.Model):
    __tablename__ = "Courses"
    id = db.Column(db.String, primary_key=True, nullable=False, unique=True)
    credits = db.Column(db.Float, nullable=False, unique=False)
    course_name = db.Column(db.String, nullable=False, unique=False)
    description = db.Column(db.String, nullable=False, unique=False)
    prerequisites = db.Column(db.String, nullable=True, unique=False)
    corequisites = db.Column(db.String, nullable=True, unique=False)
    exclusions = db.Column(db.String, nullable=True, unique=False)
    one_way_exclusions = db.Column(db.String, nullable=True, unique=False)
    equivalency = db.Column(db.String, nullable=True, unique=False)
    recommendations = db.Column(db.String, nullable=True, unique=False)
    learning_hours = db.Column(db.String, nullable=False, unique=False)

    def __init__(self, id: str, credits: int, course_name: str, description: str, prerequisites: str, corequisites: str,
                exclusions: str, one_way_exclusions: str, equivalency: str, recommendations: str, learning_hours: str) -> None:
        super().__init__(id=id, credits=credits, course_name=course_name, description=description, prerequisites=prerequisites,
         corequisites=corequisites, exclusions=exclusions, one_way_exclusions=one_way_exclusions, equivalency=equivalency, recommendations=recommendations, learning_hours=learning_hours)

    def __repr__(self) -> str:
        output = "\n".join(["\n", self.id, "CREDITS: " + str(self.credits), "COURSE NAME: " + str(self.course_name)])
        if self.prerequisites:
            output += "PREREQUISITES: " + self.prerequisites
        if self.corequisites:
            output += "COREQUISITES: " + self.corequisites
        if self.exclusions:
            output += "EXCLUSIONS: " + self.exclusions
        if self.one_way_exclusions:
            output += "ONE-WAY EXCLUSIONS: " + self.one_way_exclusions
        if self.equivalency:
            output += "EQUIVALENCIES: " + self.equivalency
        if self.recommendations:
            output += "RECOMMENDATIONS: " + self.recommendations
        if self.learning_hours:
            output += "LEARNING HOURS: " + self.learning_hours
        output += "\n"
        return output

def parse_description(line: str):
    # split whenever you come across one of the following keywords
    # need to differenciate the "exclusion" types when splitting
    line = line.replace("ONE-WAY EXCLUSION ", "ONE-WAY EXCLUSION* ")
    keywords = ["LEARNING HOURS ", "RECOMMENDATION ", "PREREQUISITE ", "COREQUISITE ", "EXCLUSION ", "ONE-WAY EXCLUSION* ",  "EQUIVALENCY "]
    split_counts = 0
    splits = {}
    for i in range(len(keywords)):
        outer_k = keywords[i]
        find = line.split(outer_k)
        # found an instance (shouldn't ever have more than 2 unless there's an error in the data)
        if len(find) == 2:
            before, after = find[0], find[1]
            # if this is the first split, set the description to just the description
            # TODO: FIX
            if split_counts == 0:
                splits["DESCRIPTION"] = before
            split_counts += 1
            start_index = len(before) + len(outer_k)
            # now we need to find where this section (i.e. prereqs) ends.
            # this is to avoid sections nesting inside each other and to achieve a clean split
            end_index = len(after)
            for inner_k in keywords:
                find = after.split(inner_k)
                if len(find) == 2:
                    potential_end_index = len(find[0])
                    if potential_end_index < end_index:
                        end_index = potential_end_index
            splits[outer_k.strip(" ")] = line[start_index : start_index + end_index]
    return splits

def parse_course(line: str):
    course, course_name = [s for s in line.split("\t")]
    id, credits = course.split("/")
    return id, credits, course_name

def create_database():
    new_course = True
    description = ""
    prerequisites = None
    corequisites = None
    one_way_exclusions = None
    exclusions = None
    equivalency = None
    recommendations = None
    learning_hours = None

    f = open("sfss/courses.txt", "r")
    text = f.readlines()
    f.close()    
    for i in range(len(text)):
        line = text[i]
        if new_course:
            id, credits, course_name = parse_course(line)
            description = ""
            new_course = False
        elif line.strip(" ") == "\n":
            description_dict = parse_description(description)
            for key, value in description_dict.items():
                if key == "DESCRIPTION":
                    description = value
                if key == "PREREQUISITE":
                    prerequisites = value
                elif key == "COREQUISITE":
                    corequisites = value
                elif key == "ONE WAY EXCLUSION*":
                    one_way_exclusions = value
                elif key == "EXCLUSION":
                    exclusions = value
                elif key == "EQUIVALENCY":
                    equivalency = value
                elif key == "RECOMMENDATION":
                    recommendations = value
                elif key == "LEARNING HOURS":
                    learning_hours = value
            db.session.add(Course(id, credits, course_name, description, prerequisites, corequisites, exclusions, one_way_exclusions, equivalency, recommendations, learning_hours))
            new_course = True
        else:
            description += line
    db.session.commit()
