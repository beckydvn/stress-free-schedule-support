from typing import List
from sfss import db

class Course(db.Model):
    __tablename__ = "Courses"
    id = db.Column(db.String, primary_key=True, nullable=False, unique=True)
    credits = db.Column(db.Float, nullable=False, unique=False)
    course_name = db.Column(db.String, nullable=False, unique=False)
    description = db.Column(db.String, nullable=False, unique=False)
    prerequisites = db.Column(db.PickleType, nullable=True, unique=False)
    corequisites = db.Column(db.PickleType, nullable=True, unique=False)
    exclusions = db.Column(db.PickleType, nullable=True, unique=False)
    one_way_exclusions = db.Column(db.PickleType, nullable=True, unique=False)
    equivalency = db.Column(db.PickleType, nullable=True, unique=False)
    recommendations = db.Column(db.PickleType, nullable=True, unique=False)
    learning_hours = db.Column(db.String, nullable=False, unique=False)

    def __init__(self, id: str, credits: int, course_name: str, description: str, prerequisites: List[str], corequisites: List[str],
                exclusions: List[str], one_way_exclusions: List[str], equivalency: List[str], recommendations: List[str], learning_hours: str) -> None:
        super().__init__(id=id, credits=credits, course_name=course_name, description=description, prerequisites=prerequisites,
         corequisites=corequisites, exclusions=exclusions, one_way_exclusions=one_way_exclusions, equivalency=equivalency, recommendations=recommendations, learning_hours=learning_hours)

    def __repr__(self) -> str:
        output = "\n".join(["\n", self.id, "CREDITS: " + str(self.credits), "COURSE NAME: " + str(self.course_name), "DESCRIPTION: " + self.description])
        if self.prerequisites:
            output += "\nPREREQUISITES: " + " ".join(self.prerequisites)
        if self.corequisites:
            output += "\nCOREQUISITES: " + " ".join(self.corequisites)
        if self.exclusions:
            output += "\nEXCLUSIONS: " + " ".join(self.exclusions)
        if self.one_way_exclusions:
            output += "\nONE-WAY EXCLUSIONS: " + " ".join(self.one_way_exclusions)
        if self.equivalency:
            output += "\EQUIVALENCIES: " + " ".join(self.equivalency)
        if self.recommendations:
            output += "\nRECOMMENDATIONS: " + " ".join(self.recommendations)
        if self.learning_hours:
            output += "\nLEARNING HOURS: " + " ".join(self.learning_hours)
        output += "\n\n"
        return output

def parse_description(line: str):
    print(line)
    # split whenever you come across one of the following keywords
    keywords = ["PREREQUISITE ", "COREQUISITE ", "ONE-WAY EXCLUSION* ", "EXCLUSION ", "EQUIVALENCY ", "RECOMMENDATION ", "LEARNING HOURS "]
    splits = {}
    for outer_k in keywords:
        find = line.split(outer_k)
        # found an instance (shouldn't ever have more than 2 unless there's an error in the data)
        if len(find) == 2:
            before, after = find[0], find[1]
            start_index = len(before)
            # now we need to find where this section (i.e. prereqs) ends.
            # this is to avoid sections nesting inside each other and to achieve a clean split
            end_index = start_index + len(after)
            for inner_k in keywords:
                find = after.split(inner_k)
                if len(find) == 2:
                    potential_end_index = start_index + len(find[0])
                    if potential_end_index < end_index:
                        end_index = potential_end_index
            splits[outer_k.strip(" ")] = line[start_index + len(outer_k) : end_index]
    return splits

def parse_course(line: str):
    course, course_name = [s for s in line.split("\t")]
    id, credits = course.split("/")
    return id, credits, course_name

def create_database():
    new_course = True
    description = ""
    prerequisites = None
    exclusions = None
    recommendations = None

    f = open("sfss/courses.txt", "r")
    text = f.readlines()
    f.close()    
    for i in range(len(text)):
        print(i)
        line = text[i]
        if new_course:
            id, credits, course_name = parse_course(line)
            description = ""
            new_course = False
        elif line.strip(" ") == "\n":
            description = parse_description(description)
            db.session.add(Course(id, credits, course_name, description, prerequisites, corequisites, exclusions, equivalency, recommendations, learning_hours))
            new_course = True
        else:
            description += line
    db.session.commit()
