from App.database import db
import enum

class Category(enum.Enum):
    EXAM = "Exam"
    ASSIGNMENT = "Assignment"
    QUIZ = "Quiz"
    PROJECT = "Project"
    DEBATE = "Debate"
    PRESENTATION = "Presentation"
    ORALEXAM = "Oral Exam"
    PARTICIPATION = "Participation"

class Assessment(db.Model):
    __tablename__ = 'assessment'

    assessmentID = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    courseCode = db.Column(db.Integer, db.ForeignKey('course.courseCode'),nullable=False)
    assessmentTitle = db.Column(db.String(120),nullable=False)
    assessmentType = db.Column(db.String(120),nullable=False)
    startDate = db.Column(db.Date)
    dueDate = db.Column(db.Date)
    # category = db.Column(db.Enum(Category), nullable=False)

    def __init__(self, assessmentID, courseCode, assessmentTitle, assessmentType, startDate, dueDate):
        self.assessmentID = assessmentID
        self.courseCode = courseCode
        self.assessmentTitle = assessmentTitle
        self.assessmentType = assessmentType
        self.startDate = startDate
        self.dueDate = dueDate

        # self.category = category

    def to_json(self):
        return {
        "assessmentID" : self.assessmentID,
        "courseCode" : self.courseCode,
        "assessmentTitle" : self.assessmentTitle,
        "assessmentType" : self.assessmentType,
        "startDate" : self.startDate,
        "dueDate" : self.dueDate
        # "category" : self.category
        }     
