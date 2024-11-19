from App.database import db

class Programme(db.Model):
  __tablename__ = 'programme'

  programmeID = db.Column(db.Integer, primary_key = True, nullable=False, autoincrement=True)
  programmeTitle = db.Column(db.String(100), nullable = False)
  programmeDescription = db.Column(db.String(200), nullable = False)
  #creates reverse relationship from Programme back to Course to access courses offered in a programme
  # programmeCourses = db.relationship('CourseProgramme', backref='courses', lazy='joined' )

  def __init__(self, programmeTitle, programmeDescription):
    self.programmeTitle = programmeTitle
    self.programmeDescription = programmeDescription

  def to_json(self):
    return {
    "programmeID" : self.programmeID,
    "programmeTitle" : self.programmeTitle,
    "programmeDescription" : self.programmeDescription
    } 