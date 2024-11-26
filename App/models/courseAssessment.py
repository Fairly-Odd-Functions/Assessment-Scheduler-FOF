from App.database import db

class CourseAssessment(db.Model):
    __tablename__ = 'courseAssessment'

    # Attributes
    courseAssessmentID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    assessmentID = db.Column(db.Integer, db.ForeignKey('assessment.assessmentID'), nullable=False)
    courseCode = db.Column(db.String(9), db.ForeignKey('course.courseCode'), nullable=False)
    startDate = db.Column(db.Date, nullable=True)
    dueDate = db.Column(db.Date, nullable=True)

    # Relationships
    course = db.relationship('Course', backref='course_assessments')
    assessment = db.relationship('Assessment', backref='assessment_courses')

    def __init__(self, courseCode, assessmentID, startDate, dueDate):
        self.courseCode = courseCode
        self.assessmentID = assessmentID
        self.startDate = startDate
        self.dueDate = dueDate

    def get_json(self):
        return {
            "courseAssessmentID": self.courseAssessmentID,
            "courseCode": self.courseCode,
            "assessmentID": self.assessmentID,
            "startDate": self.startDate,
            "dueDate": self.dueDate,
        }

    def __str__(self):
        return f"CourseAssessment(ID={self.courseAssessmentID}, Course={self.courseCode}, Assessment={self.assessmentID})"

    def __repr__(self):
        return (
            f"CourseAssessment(courseAssessmentID={self.courseAssessmentID}, "
            f"courseCode={self.courseCode}, assessmentID={self.assessmentID}, "
            f"startDate={self.startDate}, dueDate={self.dueDate})"
        )