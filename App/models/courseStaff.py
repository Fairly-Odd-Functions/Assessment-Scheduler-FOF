from App.database import db

class CourseStaff(db.Model):
    __tablename__ = 'courseStaff'

    # Attributes
    courseStaffID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    courseOfferingID = db.Column(db.Integer, db.ForeignKey('course_offering.offeringID'), nullable=False)
    staffID = db.Column(db.Integer, db.ForeignKey('staff.staffID'), nullable=False)

    # Relationships
    course_offering = db.relationship('CourseOffering', backref='course_staff')
    staff = db.relationship('Staff', backref='assigned_courses')

    def __init__(self, courseOfferingID, staffID):
        self.courseOfferingID = courseOfferingID
        self.staffID = staffID

    def get_json(self):
        return {
            "courseStaffID": self.courseStaffID,
            "courseOffering": {
                "courseCode": self.course_offering.courseCode if self.course_offering else None,
                "courseName": self.course_offering.course.courseName if self.course_offering and self.course_offering.course else None,
                "semester": self.course_offering.semester.semesterName if self.course_offering and self.course_offering.semester else None,
                "academicYear": self.course_offering.semester.academicYear if self.course_offering and self.course_offering.semester else None,
                "startDate": self.course_offering.semester.startDate if self.course_offering and self.course_offering.semester else None,
                "endDate": self.course_offering.semester.endDate if self.course_offering and self.course_offering.semester else None,
            },
            "staff": {
                "staffID": self.staffID,
                "staffName": f"{self.staff.firstName} {self.staff.lastName}" if self.staff else None,
                "staffEmail": self.staff.email if self.staff else None,
            },
        }

    def __str__(self):
        course_details = (
            f"courseCode='{self.course_offering.courseCode}', "
            f"courseName='{self.course_offering.course.courseName if self.course_offering and self.course_offering.course else 'No course name'}', "
            f"semester='{self.course_offering.semester.semesterName if self.course_offering and self.course_offering.semester else 'No semester'}', "
            f"academicYear='{self.course_offering.semester.academicYear if self.course_offering and self.course_offering.semester else 'No year'}'"
        )
        staff_details = (
            f"staffID='{self.staffID}', "
            f"staffName='{self.staff.firstName} {self.staff.lastName}' if self.staff else 'No name', "
            f"staffEmail='{self.staff.email if self.staff else 'No email'}'"
        )
        return f"CourseStaff({course_details}, {staff_details})"

    def __repr__(self):
        return (
            f"CourseStaff(courseStaffID={self.courseStaffID}, "
            f"courseCode='{self.course_offering.courseCode if self.course_offering else 'No course code'}', "
            f"courseName='{self.course_offering.course.courseName if self.course_offering and self.course_offering.course else 'No course name'}', "
            f"semester='{self.course_offering.semester.semesterName if self.course_offering and self.course_offering.semester else 'No semester'}', "
            f"academicYear='{self.course_offering.semester.academicYear if self.course_offering and self.course_offering.semester else 'No year'}', "
            f"staffID={self.staffID}, "
            f"staffName='{self.staff.firstName} {self.staff.lastName}' if self.staff else 'No name', "
            f"staffEmail='{self.staff.email if self.staff else 'No email'}')"
        )