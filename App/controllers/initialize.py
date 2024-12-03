from flask import jsonify
from App.database import db
from App.models import *
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

                # Create Defulat Programme
        programme_title = "BSc Computer Science (Special)"
        programme_description = ("This Is A Porgramme.")
        programme = Programme(
            programmeTitle=programme_title,
            programmeDescription=programme_description
        )

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

        # Create Default Course 1
        course_code1 = "COMP3613"
        course_title1 = "Software Engineering II"
        course_credits1 = 3
        course_level1 = 3
        course_description1 = ("This Is A Course")

        course1 = Course (
            courseCode=course_code1,
            courseTitle=course_title1,
            courseCredits=course_credits1,
            courseDescription=course_description1,
            courseLevel=course_level1
        )

        # Create Default Course 2
        course_code2 = "COMP3603"
        course_title2 = "Human-Computer Interaction"
        course_credits2 = 3
        course_credits2 = 3
        course_level2 = 3
        course_description2 = ("This Is A Course")

        course2 = Course (
            courseCode=course_code2,
            courseTitle=course_title2,
            courseCredits=course_credits2,
            courseDescription=course_description2,
            courseLevel=course_level2
        )

        # Create Default Assessment 1
        assessment1_title = "Human-Computer Interaction - CourseWork Exam"
        assessment1_type = "COURSEWORK"

        assessment1 = Assessment(
            assessmentTitle=assessment1_title,
            assessmentType=assessment1_type)

        # Create Default Assessment 2
        assessment2_title = "Theory Of Computing - Quiz #1"
        assessment2_type = "QUIZ"

        assessment2 = Assessment(
            assessmentTitle=assessment2_title,
            assessmentType=assessment2_type)
        
        # Create Default Assessment 3
        assessment3_title = "Software Engineering II - Project"
        assessment3_type = "PROJECT"

        assessment3 = Assessment(
            assessmentTitle=assessment3_title,
            assessmentType=assessment3_type)

        db.session.add(programme)
        db.session.add(semester)
        db.session.add(course1)
        db.session.add(course2)
        db.session.add(assessment1)
        db.session.add(assessment2)
        db.session.add(assessment3)
        db.session.commit()

        # Adding Course To Programme
        programmecourse1 = CourseProgramme(programmeID=programme.programmeID, courseCode=course1.courseCode)
        programmecourse2 = CourseProgramme(programmeID=programme.programmeID, courseCode=course2.courseCode)

        # Add Course To Semester
        courseoffering1 = CourseOffering(courseCode=course1.courseCode, semesterID=semester.semesterID, totalStudentsEnrolled=150)
        courseoffering2 = CourseOffering(courseCode=course2.courseCode, semesterID=semester.semesterID, totalStudentsEnrolled=200)

        # Add Assessment To Course - CourseWork
        courseassessment1 = CourseAssessment(
            assessmentID=assessment1.assessmentID,
            courseCode=course1.courseCode,
            startDate=datetime.strptime("2024-11-04", "%Y-%m-%d"),
            startTime=datetime.strptime("9:00", "%H:%M").time(),
            endDate=datetime.strptime("2024-11-04", "%Y-%m-%d"),
            endTime=datetime.strptime("10:00", "%H:%M").time(),
            clashRule=ClashRules.DEGREE)

        db.session.add(programmecourse1)
        db.session.add(programmecourse2)
        db.session.add(courseoffering1)
        db.session.add(courseoffering2)
        db.session.add(courseassessment1)
        db.session.commit()

    except Exception as e:
        print(f"Error: {e}")
        return jsonify(error="An Error Occurred While Initializing Database"), 500