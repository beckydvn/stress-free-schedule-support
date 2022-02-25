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
    equivalency = db.Column(db.PickleType, nullable=True, unique=False)
    recommendations = db.Column(db.PickleType, nullable=True, unique=False)
    learning_hours = db.Column(db.String, nullable=False, unique=False)

    def __init__(self, id: str, credits: int, course_name: str, description: str, prerequisites: List[str], corequisites: List[str],
                exclusions: List[str], equivalency: List[str], recommendations: List[str], learning_hours: str) -> None:
        super().__init__(id=id, credits=credits, course_name=course_name, description=description, prerequisites=
        prerequisites, corequisites=corequisites exclusions=exclusions, equivalency=equivalency, recommendations=recommendations, learning_hours=learning_hours)

    def __repr__(self) -> str:
        output = "\n".join(["\n", self.id, "CREDITS: " + str(self.credits), "COURSE NAME: " + str(self.course_name), "DESCRIPTION: " + self.description])
        if self.prerequisites:
            output += "\nPREREQUISITES: " + " ".join(self.prerequisites)
        if self.corequisites:
            output += "\nCOREQUISITES: " + " ".join(self.prerequisites)
        if self.exclusions:
            output += "\nEXCLUSIONS: " + " ".join(self.exclusions)
        if self.equivalency:
            output += "\EQUIVALENCY: " + " ".join(self.equivalency)
        if self.recommendations:
            output += "\nRECOMMENDATIONS: " + " ".join(self.recommendations)
        if self.learning_hours:
            output += "\nLEARNING HOURS: " + " ".join(self.learning_hours)
        output += "\n\n"
        return output

def parse_course(line: str):
    course, course_name = [s for s in line.split("\t")]
    id, credits = course.split("/")
    return id, credits, course_name

def create_database():
    new_course = True
    description = ""
    prerequisite = None
    exclusion = None
    recommendation = None

    f = open("sfss/courses.txt", "r")
    text = f.readlines()
    f.close()    
    for i in range(len(text)):
        print(i)
        line = text[i]
        if new_course:
            id, credits, course_name = parse_course(line)
            if id == "ANAT 312":
                print()
            description = ""
            new_course = False
        elif line.strip(" ") == "\n":
            description = description.strip("\n")
            db.session.add(Course(id, credits, course_name, description, prerequisite, exclusion, recommendation))
            new_course = True
        elif "PREREQUISITE" in line:
            prerequisite = line
        elif "EXCLUSION" in line:
            exclusion = line
        elif "RECOMMENDATION" in line:
            recommendation = line
        else:
            description += line + "\n"
    db.session.commit()
