from App.database import db
from .course import Course
from .staff import Staff

class CourseStaff(db.Model):
  __tablename__ = 'courseStaff'

  courseStaffID = db.Column(db.Integer, primary_key= True, autoincrement=True)
  courseCode = db.Column(db.String(120), db.ForeignKey('course.courseCode'), nullable=False)
  userID = db.Column(db.Integer, db.ForeignKey('user.userID'), nullable=False)

def __init__(self, courseCode, userID):
  self.courseCode = courseCode
  self.userID = userID

def to_json(self):
  return{
    "courseCode":self.courseCode,
    "userID":self.userID
  }

#Add new CourseStaff
def addCourseStaff(self):
  db.session.add(self)
  db.session.commit()
