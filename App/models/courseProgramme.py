from App.database import db
from App.models import Programme
from App.models import Course

class CourseProgramme(db.Model):
  __tablename__ = 'courseProgramme'

  #Attributes
  courseProgrammeID = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
  programmeID = db.Column(db.Integer, db.ForeignKey('programme.programmeID'), nullable = False)   
  courseCode = db.Column(db.String(8), db.ForeignKey('course.courseCode'), nullable = False)

  #Relationships
  course = db.relationship('Course', backref='programme', lazy='joined')
  programme = db.relationship('Programme', backref='course', lazy='joined')
 
  def __init__(self, programmeID, courseCode):
    self.programmeID = programmeID
    self.courseCode = courseCode
    
  def get_json(self):
    return {
        'courseProgrammeID': self.courseProgrammeID,
        'programmeID': self.programmeID,
        'courseCode': self.courseCode
    } 
  
  def __str__(self):
    return (
        f"CourseProgramme(programmeTitle={self.programme.programmeTitle}, "
        f"courseCode={self.course.courseCode}, "
        f"courseTitle={self.course.courseTitle})"
    )

  def __repr__(self):
      return (
          f"<CourseProgramme(programmeTitle: '{self.programme.programmeTitle}' | "
          f"courseCode: '{self.course.courseCode}' | "
          f"courseTitle: '{self.course.courseTitle}')>"
      )