from flask import jsonify
from App.database import db
from App.models import Admin, Staff

def initialize():
    try:
        db.drop_all()
        db.create_all()

        # Create Default Admin User
        bob = Admin(firstName="Bob", lastName="Bobberson", password="bobpass", email="bob.bobberson@mail.com")

        # Create Default Staff User
        rick = Staff(firstName="Rick", lastName="Rickson", password="rickpass", email="rick.rickson@mail.com")

        # TESING CODE : List Semester Courses 
        # from datetime import date  
        # semester = Semester(semesterName="Semester 1", academicYear="2024/2025", startDate=date(2024, 10, 12), endDate=date(2025, 10, 12))
        # course = Course(courseCode="JAY1212", courseTitle="Introduction To Jalene", courseCredits="9000", courseDescription="Whompy Whomp", courseLevel="Expert")
        # db.session.add(semester)
        # db.session.add(course)
        # course_offering = CourseOffering(semesterName="Semester 1", courseCode="JAY1212", academicYear="2024/2025", totalStudentsEnrolled=100)
        # db.session.add(course_offering)

        db.session.add(rick)
        db.session.add(bob)
        db.session.commit()
        print(rick)
        print(bob)

    except Exception as e:
        print(f"Error: {e}")
        return jsonify(error="An Error Occurred While Initializing Database"), 500