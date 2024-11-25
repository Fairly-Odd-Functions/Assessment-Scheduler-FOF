from App.database import db

class CourseAssessment(db.Model):
    __tablename__ = 'courseAssessment'

    id = db.Column(db.Integer, primary_key= True, autoincrement=True)
    courseCode = db.Column(db.String(9), db.ForeignKey('course.courseCode'), nullable = False)
    assessmentID = db.Column(db.Integer, db.ForeignKey('assessment.assessmentID'), nullable = False)
    startDate = db.Column(db.Date, nullable = True)
    endDate = db.Column(db.Date, nullable = True)
    startTime = db.Column(db.Time, nullable = True)
    endTime = db.Column(db.Time, nullable = True)
    clashDetected = db.Column(db.Boolean, default = False)


    def __init__(self, courseCode, a_ID, startDate, endDate, startTime, endTime, clashDetected):
        self.courseCode = courseCode
        self.a_ID = a_ID
        self.startDate = startDate
        self.endDate = endDate
        self.startTime = startTime
        self.endTime = endTime
        self.clashDetected = clashDetected

    def to_json(self):
        return {
            "assessmentNo": self.id,
            "courseCode" : self.courseCode,
            "a_ID" : self.a_ID,
            "startDate" : self.startDate,
            "endDate" : self.endDate,
            "startTime" : self.startTime,
            "endTime" : self.endTime,
            "clashDetected" : self.clashDetected
        }

    #Add new assessment to course
    def addCourseAsg(self, courseCode, a_ID, startDate, endDate, startTime, endTime, clashDetected):
        newAsg = CourseAssessment(courseCode, a_ID, startDate, endDate, startTime, endTime, clashDetected)
        db.session.add(newAsg)  #add to db
        db.session.commit()
        return newAsg