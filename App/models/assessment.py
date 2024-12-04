import enum
from App.database import db

class AssessmentTypes(enum.Enum):
    FINAL = "final"
    COURSEWORK = "course_work"
    ASSIGNMENT = "assignment"
    QUIZ = "quiz"
    PROJECT = "project"
    PRESENTATION = "presentation"

class Assessment(db.Model):
    __tablename__ = 'assessment'

    # Attributes
    assessmentID = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    assessmentTitle = db.Column(db.String(120),nullable=False)
    assessmentType = db.Column(db.Enum(AssessmentTypes), nullable=False)

    def __init__(self, assessmentTitle, assessmentType):
        self.assessmentTitle = assessmentTitle
        self.assessmentType = assessmentType

    def get_json(self):
        return {
            'assessmentID': self.assessmentID,
            'assessmentTitle': self.assessmentTitle,
            'assessmentType': self.assessmentType.name,
        }

    def __str__(self):
        return (f"assessmentTitle={self.assessmentTitle},"
                f"assessmentType={self.assessmentType.name},")

    def __repr__(self):
        return (f"<Assessment(assessmentTitle='{self.assessmentTitle}', "
                f"assessmentType='{self.assessmentType.name}'>")