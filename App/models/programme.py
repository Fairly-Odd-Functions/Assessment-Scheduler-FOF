from App.database import db

class Programme(db.Model):
  __tablename__ = 'programme'

  programmeID = db.Column(db.Integer, primary_key = True, nullable=False, autoincrement=True)
  programmeTitle = db.Column(db.String(100), nullable = False)
  programmeDescription = db.Column(db.String(200), nullable = False)

  # Relationship with the CourseProgramme model
  programmeCourses = db.relationship('courseProgramme', backref='programme', lazy=True)
 
  def __init__(self, programmeTitle, programmeDescription):
    self.programmeTitle = programmeTitle
    self.programmeDescription = programmeDescription

  def get_json(self):
      return {
          'programmeID': self.programmeID,
          'programmeTitle': self.programmeTitle,
          'programmeDescription': self.programmeDescription,
          'programmeCourses': [course.get_json() for course in self.programmeCourses]
      }
  
  def __str__(self):
    return f"programmeID={self.programmeID}, 
             programmeTitle={self.programmeTitle}, 
             programmeDescription={self.programmeDescription},
             programmeCourses={', '.join([course.courseCode for course in self.programmeCourses])})"

  def __repr__(self):
      return (f"<Programme: {self.programmeTitle} | "
              f"Description: {self.programmeDescription} | "
              f"Courses: {', '.join([course.courseCode for course in self.programmeCourses])}>")