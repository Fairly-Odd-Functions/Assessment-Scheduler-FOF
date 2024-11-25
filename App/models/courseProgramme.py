from App.database import db

class CourseProgramme(db.Model):
  __tablename__ = 'courseProgramme'

  courseProgrammeID = db.Column(db.Integer, primary_key=True )
  programmeID = db.Column(db.Integer, db.ForeignKey('programme.programmeID'), nullable = False)   
  courseCode = db.Column(db.String(8), db.ForeignKey('course.courseCode'), nullable = False)
 
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
    return f" programmeID={self.programmeID}, 
              courseCode={self.courseCode})"
  
  def __repr__(self):
    return (f"<programmeID: {self.programmeID} | "
            f"courseCode: {self.courseCode}>")