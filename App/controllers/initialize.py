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
        db.session.add(rick)
        db.session.add(bob)
        db.session.commit()


        # TESTING CODE: Create A Course, Add Assessment To Course
        from datetime import date
        from App.models import Course, Semester,Assessment,courseAssessment
        course = Course(courseCode="COMP911", courseTitle="Intro to Mental Health", courseCredits="0", courseDescription="Help Me", courseLevel="1")        
        semester = Semester(semesterName="Semester 1", academicYear="2024/2025", startDate=date(2024, 10, 12), endDate=date(2025, 10, 12))
        assessment = Assessment(assessmentTitle="CourseWork#1", assessmentType="Midterm", startDate=date(2024, 10, 12), dueDate=date(2024, 10, 12))
        
        db.session.add(assessment)
        db.session.add(course)
        db.session.add(semester)
        db.session.commit()

    except Exception as e:
        print(f"Error: {e}")
        return jsonify(error="An Error Occurred While Initializing Database"), 500