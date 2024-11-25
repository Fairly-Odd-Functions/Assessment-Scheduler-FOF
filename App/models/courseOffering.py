from App.database import db

class CourseOffering(db.Model):
    __tablename__ = 'course_offering'

    # Attributes
    offeringID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    courseCode = db.Column(db.String(9), db.ForeignKey('course.courseCode'), nullable=False)
    semesterID = db.Column(db.Integer, db.ForeignKey('semester.semesterID'), nullable=False)
    academicYear = db.Column(db.String(9), nullable=False)
    totalStudentsEnrolled = db.Column(db.Integer, default=0)

    # Relationships
    course = db.relationship('Course', backref='course_offerings')
    semester = db.relationship('Semester', backref='semester_offerings')

    def __init__(self, courseCode, semesterID, academicYear, totalStudentsEnrolled=0):
        self.courseCode = courseCode
        self.semesterID = semesterID
        self.academicYear = academicYear
        self.totalStudentsEnrolled = totalStudentsEnrolled

    def get_json(self):
        return {
            "offeringID": self.offeringID,
            "courseCode": self.courseCode,
            "semesterID": self.semesterID,
            "academicYear": self.academicYear,
            "totalStudentsEnrolled": self.totalStudentsEnrolled,
        }

    def __str__(self):
        return f"{self.course.courseTitle} ({self.courseCode}) - {self.academicYear}, Semester {self.semesterID}"

    def __repr__(self):
        return (
            f"CourseOffering(courseCode='{self.courseCode}', academicYear='{self.academicYear}', "
            f"semesterID={self.semesterID}, totalStudentsEnrolled={self.totalStudentsEnrolled})"
        )