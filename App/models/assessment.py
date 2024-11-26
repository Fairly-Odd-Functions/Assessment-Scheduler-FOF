from App.database import db
import enum

class Assessment(db.Model):
    __tablename__ = 'assessment'

    #Attributes
    assessmentID = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    courseCode = db.Column(db.Integer, db.ForeignKey('course.courseCode'),nullable=False)
    assessmentTitle = db.Column(db.String(120),nullable=False)
    assessmentType = db.Column(db.String(120),nullable=False)

    def __init__(self, courseCode, assessmentTitle, assessmentType):
            self.courseCode = courseCode
            self.assessmentTitle = assessmentTitle
            self.assessmentType = assessmentType 

    def get_json(self):
        return {
            'assessmentID': self.assessmentID,
            'courseCode': self.courseCode,
            'assessmentTitle': self.assessmentTitle,
            'assessmentType': self.assessmentType,
        }  
    
    def __str__(self):
        return f"courseCode={self.courseCode}, 
                assessmentTitle={self.assessmentTitle},
                assessmentType={self.assessmentType}"

    def __repr__(self):
        return (f"<Assessment(assessmentTitle='{self.assessmentTitle}', "
                f"courseCode='{self.courseCode}', "
                f"assessmentType='{self.assessmentType}')>")