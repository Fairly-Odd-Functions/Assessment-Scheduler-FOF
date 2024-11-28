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

        # #TESTING CODE: Add Staff Course
        # from datetime import date
        # from App.models import Course, Semester
        # course = Course(courseCode="COMP911", courseTitle="Intro to Mental Health", courseCredits="0", courseDescription="Help Me", courseLevel="1")        
        # semester = Semester(semesterName="Semester 1", academicYear="2024/2025", startDate=date(2024, 10, 12), endDate=date(2025, 10, 12))
        # db.session.add(course)
        # db.session.add(semester)
        # db.session.commit()

        # TESING CODE : List Semester Courses 
        # from datetime import date
        # from App.models import Semester, Course, CourseOffering
        # semester = Semester(semesterName="Semester 1", academicYear="2024/2025", startDate=date(2024, 10, 12), endDate=date(2025, 10, 12))
        # course = Course(courseCode="JAY1212", courseTitle="Introduction To Jalene", courseCredits="9000", courseDescription="Whompy Whomp", courseLevel="Expert")
        # db.session.add(semester)
        # db.session.add(course)
        # course_offering = CourseOffering(semesterName="Semester 1", courseCode="JAY1212", academicYear="2024/2025", totalStudentsEnrolled=100)
        # db.session.add(course_offering)

        # TESING CODE : List Programme Courses
        # from App.models import Programme, Course, CourseProgramme
        # programme = Programme(programmeTitle="B.Sc. Jalene Armstrong", programmeDescription="Whomp Whomp Whompy Whomp")
        # course = Course(courseCode="JAY1212", courseTitle="Introduction To Jalene Armstrong", courseCredits="9000", courseDescription="Whompy Whomp", courseLevel="Expert")
        # db.session.add(programme)
        # db.session.add(course)
        # programme_course = CourseProgramme(programmeID=1, courseCode=course.courseCode,)
        # db.session.add(programme_course)

        db.session.add(rick)
        db.session.add(bob)
        db.session.commit()

    except Exception as e:
        print(f"Error: {e}")
        return jsonify(error="An Error Occurred While Initializing Database"), 500