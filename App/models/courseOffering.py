from App.database import db
from .semester import Semester

class CourseOffering(db.Model):
    __tablename__ = 'course_offering'

    # Attributes
    offeringID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    courseCode = db.Column(db.String(9), db.ForeignKey('course.courseCode'), nullable=False)
    semesterID = db.Column(db.Integer, db.ForeignKey('semester.semesterID'), nullable=False)
    totalStudentsEnrolled = db.Column(db.Integer, default=0)

    # Relationships
    course = db.relationship('Course', backref='course_offerings')
    semester = db.relationship('Semester', backref='semester_offerings')

    def __init__(self, courseCode, semesterName, academicYear, totalStudentsEnrolled=0):
        self.courseCode = courseCode

        # Fetch Correct Semester Using semesterName & academicYear
        semester = Semester.query.filter_by(semesterName=semesterName, academicYear=academicYear).first()
        if not semester:
            raise ValueError(f"No Semester Found With Name '{semesterName}' And Academic Year '{academicYear}'")
        
        self.semesterID = semester.semesterID
        self.totalStudentsEnrolled = totalStudentsEnrolled

    def get_json(self):
        return {
            "offeringID": self.offeringID,
            "courseCode": self.courseCode,
            "semesterID": self.semesterID,
            "semester": self.semester.get_json() if self.semester else None,
            "totalStudentsEnrolled": self.totalStudentsEnrolled,
        }

    def __str__(self):
        return (
            f"Course Offering: {self.course.courseTitle} ({self.courseCode}) - "
            f"{self.semester.semesterName} ({self.semester.academicYear})"
        )

    def __repr__(self):
        return (
            f"CourseOffering(courseCode='{self.courseCode}', semesterID={self.semesterID}, "
            f"totalStudentsEnrolled={self.totalStudentsEnrolled})"
        )