from App.database import db

class Course(db.Model):
  __tablename__ = 'course'

  courseCode = db.Column(db.String(9), primary_key=True)
  offeredSemester = db.Column(db.Integer,db.ForeignKey('semester.semesterID'), nullable=False)
  clashRules = db.relationship('ClashRule',backref='course', lazy=True)
   
  clashRuleID = db.Column(db.Integer,db.ForeignKey('clashrule.clashRuleID'),nullable=False)
  courseTitle = db.Column(db.String(120), nullable=False)
  courseCredits = db.Column(db.Integer)
  courseDescription = db.Column(db.String(1024), nullable=False)
  courseLevel = db.Column(db.Integer, nullable=False)
  

  def __init__(self, courseCode, offeredSemester, courseTitle, courseCredits,  courseDescription, courseLevel):
    self.courseCode = courseCode
    self.offeredSemester = offeredSemester
    self.courseTitle = courseTitle
    self.courseCredits = courseCredits
    self.courseDescription = courseDescription
    self.courseLevel = courseLevel
    
  def to_json(self):
    return {
      "courseCode" : self.courseCode,
      "offeredSemester" : self.offeredSemester,
      "courseTitle" : self.courseTitle,
      "courseCredits": self.courseCredits,
      "courseDescription" : self.courseDescription,
      "courseLevel" : self.courseLevel
     
    }
