from App.database import db

class ClashRule(db.Model):
  __tablename__ = 'clashrule'
  # __abstract__ = True

  clashRuleID = db.Column(db.Integer, primary_key=True)
  userID = db.Column(db.Integer, db.ForeignKey('user.userID'), nullable=False)
  clashRuleTitle = db.Column(db.String(120), nullable=False)
  clashRuleDescription = db.Column(db.String(120),nullable=False)
  allowableDays = db.Column(db.Integer)
  # courses = db.relationship('Course',backref='clashrule',lazy=True)
  

  def __init__(self, clashRuleTitle, clashRuleDescription):
    self.clashRuleTitle = clashRuleTitle
    self.clashRuleDescription = clashRuleDescription
    

  def to_json(self):
    return {
      "clashRuleTitle" : self.clashRuleTitle,
      "clashRuleDescription" : self.clashRuleDescription
      
    }

  # def addCourse(courseCode, courseTitle, description, level, semester, aNum):
  #   newCourse = Course(courseCode, courseTitle, description, level, semester, aNum)
  #   db.session.add(newCourse)  #add to db
  #   db.session.commit()
  #   return newCourse
  # def is_clash(courses):
  
  def addNewRule(clashRuleTitle, clashRuleDescription):
    newRule = ClashRule(clashRuleTitle, clashRuleDescription)
    db.session.add(newRule)
    db.session.commit()
    return newRule
