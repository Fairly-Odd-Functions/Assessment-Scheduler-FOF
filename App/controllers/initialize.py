from App.models import *
from flask import jsonify
from App.database import db
from App.controllers import *
from datetime import datetime, date

def initialize():
    try:
        db.drop_all()
        db.create_all()

        # Create Default Admin User
        bob = Admin(firstName="Bob", lastName="Bobberson", password="bobpass", email="bob.bobberson@mail.com")

        # Create Default Staff User
        rick = Staff(firstName="Rick", lastName="Rickson", password="rickpass", email="rick.rickson@mail.com")

        db.session.add(bob)
        db.session.add(rick)
        db.session.commit()

        # Create Defulat Programme
        programme_title = "BSc Computer Science (Special)"
        programme_description = ("This Is A Porgramme.")
        programme = Programme(
            programmeTitle=programme_title,
            programmeDescription=programme_description
        )
        db.session.add(programme)
        db.session.commit()

        # Create Default Semester
        semester_name = "Semester 1"
        academic_year = "2024/2025"
        start_date = date(2024, 8, 25)
        end_date = date(2024, 12, 20)

        semester = Semester(
            semesterName=semester_name,
            academicYear=academic_year,
            startDate=start_date,
            endDate=end_date
        )
        db.session.add(semester)
        db.session.commit()

        # Create Default Course
        course_code = "COMP3613"
        course_title = "Software Engineering II"
        course_credits = 3
        course_level = 3
        course_description = ("This Is A Course")

        course = Course (
            courseCode=course_code,
            courseTitle=course_title,
            courseCredits=course_credits,
            courseDescription=course_description,
            courseLevel=course_level
        )
        db.session.add(course)
        db.session.commit()

        # Create Default Assessment
        assessment_title = "Software Engineering II- CourseWork Exam"
        assessment_type = "COURSEWORK"

        assessment = Assessment(
            assessmentTitle=assessment_title,
            assessmentType=assessment_type)
        db.session.add(assessment)
        db.session.commit()

        # Adding Course To Programme
        programmecourse = CourseProgramme(programmeID=programme.programmeID, courseCode=course.courseCode)
        db.session.add(programmecourse)
        db.session.commit()
        
        # Add Course To Semester
        courseoffering = CourseOffering(courseCode=course.courseCode, semesterID=semester.semesterID, totalStudentsEnrolled=125)
        db.session.add(courseoffering)
        db.session.commit()

        # Add Assessment To Course
        courseassessment = CourseAssessment(
            assessmentID=assessment.assessmentID,
            courseCode=course.courseCode,
            startDate=datetime.strptime("2024-11-04", "%Y-%m-%d"),
            startTime=datetime.strptime("9:00", "%H:%M").time(),
            endDate=datetime.strptime("2024-11-04", "%Y-%m-%d"),
            endTime=datetime.strptime("10:00", "%H:%M").time(),
            clashRule=ClashRules.DEGREE)
        db.session.add(courseassessment)
        db.session.commit()

    except Exception as e:
        print(f"Error: {e}")
        return jsonify(error="An Error Occurred While Initializing Database"), 500