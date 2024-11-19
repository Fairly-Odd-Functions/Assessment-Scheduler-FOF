from App.database import db

class Course(db.Model):
  __tablename__ = 'course'

  courseCode = db.Column(db.String(9), primary_key=True)
  offeredSemester = db.Column(db.Integer,db.ForeignKey('semester.semesterID'), nullable=False)
  clashRules = db.relationship('ClashRule',backref='course', lazy=True)
  # , cascade="all, delete-orphan" 
  
  clashRuleID = db.Column(db.Integer,db.ForeignKey('clashrule.clashRuleID'),nullable=False)
  courseTitle = db.Column(db.String(120), nullable=False)
  courseCredits = db.Column(db.Integer)
  courseDescription = db.Column(db.String(1024), nullable=False)
  courseLevel = db.Column(db.Integer, nullable=False)
  # semester = db.Column(db.Integer, nullable=False)
  # aNum = db.Column(db.Integer, nullable=False, default=0)
  # creates reverse relationship from Course back to Assessment to access assessments for a specific course
  # assessmentsAssigned = db.relationship('assessment', backref=db.backref('assessment', lazy='joined'))


  # ^^^^^^^^^^^^^^^^
  # COMMENT(RYNNIA):      (1) I see that you added 'clashRuleID' attribute, however it may not be needed as
  #                           you already created a relationship attribute 'clashRules'
  #
  

  def __init__(self, courseCode, offeredSemester, courseTitle, courseCredits,  courseDescription, courseLevel):
    self.courseCode = courseCode
    self.offeredSemester = offeredSemester
    self.courseTitle = courseTitle
    self.courseCredits = courseCredits
    self.courseDescription = courseDescription
    self.courseLevel = courseLevel
    # self.semester = semester
    # self.aNum = aNum

  # ^^^^^^^^^^^^^^^^
  # COMMENT(RYNNIA):      (1) I think there should be a  definition of the relationship attribute 'clashRules' here
  #


  def to_json(self):
    return {
      "courseCode" : self.courseCode,
      "offeredSemester" : self.offeredSemester,
      "courseTitle" : self.courseTitle,
      "courseCredits": self.courseCredits,
      "courseDescription" : self.courseDescription,
      "courseLevel" : self.courseLevel
     
    }

  # #Add new Course
  # def addCourse(courseCode, courseTitle, description, level, semester, aNum):
  #   newCourse = Course(courseCode, courseTitle, description, level, semester, aNum)
  #   db.session.add(newCourse)  #add to db
  #   db.session.commit()
  #   return newCourse