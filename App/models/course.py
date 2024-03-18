from App.database import db

class Course(db.Model):
  __tablename__ = 'course'

  courseCode = db.Column(db.String(9), primary_key=True)
  courseTitle = db.Column(db.String(120), nullable=False)
  description = db.Column(db.String(1024), nullable=False)
  level = db.Column(db.Integer, nullable=False)
  semester = db.Column(db.Integer, nullable=False)
  aNum = db.Column(db.Integer, nullable=False, default=0)
  # preReqs = db.Column(db.ForeignKey('course.courseCode'))
  #Relationship between a course and programmes to define which programmes a course belongs to
  # p_ID = db.Column(db.Integer, db.ForeignKey('programme.p_ID'), nullable = False)
  #creates reverse relationship from Course back to Assessment to access assessments for a specific course
  # assessmentsAssigned = db.relationship('assessment', backref=db.backref('assessment', lazy='joined'))
  # staffAssigned = db.Column(db.ForeignKey('staff.u_ID'))

  def __init__(self, courseCode, courseTitle, description, level, semester, aNum):
    self.courseCode = courseCode
    self.courseTitle = courseTitle
    self.description = description
    self.level = level
    self.semester = semester
    self.aNum = aNum

  # #Add new Course
  # def addCourse(courseCode, courseTitle, description, level, semester, aNum):
  #   newCourse = Course(courseCode, courseTitle, description, level, semester, aNum)
  #   db.session.add(newCourse)  #add to db
  #   db.session.commit()
  #   return newCourse