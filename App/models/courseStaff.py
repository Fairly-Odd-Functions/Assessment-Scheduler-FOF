from App.database import db
from .staff import Staff

class CourseStaff(db.Model):
    __tablename__ = 'courseStaff'

    # Attributes
    courseStaffID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    courseCode = db.Column(db.String(9), db.ForeignKey('course.courseCode'), nullable=False)
    staffID = db.Column(db.Integer, db.ForeignKey('staff.staffID'), nullable=False)

    # Relationships
    course = db.relationship('Course', backref='course_staff')
    staff = db.relationship('Staff', backref='assigned_courses')

    def __init__(self, courseCode, staffEmail):
        self.courseCode = courseCode

        # Fetching StaffID Using Email
        staff = Staff.query.filter_by(email=staffEmail).first()
        if staff is None:
            raise ValueError(f"No Staff Found With email: {staffEmail}")
        self.staffID = staff.staffID

    def get_json(self):
        return {
            "courseCode": self.courseCode,
            "staffID": self.staffID,
            "staffEmail": self.staff.email
        }

    def __str__(self):
        return f"CourseStaff(courseCode='{self.courseCode}', staffEmail='{self.staff.email}')"

    def __repr__(self):
        return (
            f"CourseStaff(courseStaffID={self.courseStaffID}, courseCode='{self.courseCode}', "
            f"staffID={self.staffID}, staffEmail='{self.staff.email}')"
        )