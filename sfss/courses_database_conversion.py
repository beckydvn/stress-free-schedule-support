from typing import List
from sfss import db

class Courses(db.Model):
    __tablename__ = "Courses"
    id = db.Column(db.String, primary_key=True, nullable=False, unique=True)
    credits = db.Column(db.Float, nullable=False, unique=False)
    description = db.Column(db.String, nullable=False, unique=False)
    prerequisites = db.Column(db.PickleType, nullable=True, unique=False)
    exclusions = db.Column(db.PickleType, nullable=True, unique=False)
    recommendations = db.Column(db.PickleType, nullable=True, unique=False)

    def __init__(self, id: str, credits: int, description: str, prerequisites: List[str], 
                exclusions: List[str], recommendations: List[str]) -> None:
        super().__init__(id=id, credits=credits, description=description, prerequisites=
        prerequisites, exclusions = exclusions, recommendations=recommendations)

    def __repr__(self) -> str:
        output = "\n".join(["\n", self.id, "CREDITS: " + str(self.credits), "DESCRIPTION: " + self.description])
        if self.prerequisites:
            output += "\nPREREQUISITES: " + " ".join(self.prerequisites)
        if self.exclusions:
            output += "\nEXCLUSIONS: " + " ".join(self.exclusions)
        if self.recommendations:
            output += "\nRECOMMENDATIONS: " + " ".join(self.recommendations)
        output += "\n\n"
        return output

def create_database():
    new_course = False
    f = open("sfss/courses.txt", "r")
    text = f.readlines()
    f.close()

    for i in range(len(text)):
        if text[i] == "\n":
            new_course = True
