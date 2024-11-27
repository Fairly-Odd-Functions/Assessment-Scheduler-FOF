from App.database import db
from App.models import Semester, CourseOffering
from App.services.semester import *

def add_semester(semesterName, academicYear, startDate, endDate):
    try:
        errors = validate_dates(academicYear, startDate, endDate)
        if errors:
            return {"Error Message": errors}

        if not semesterName or not academicYear or not startDate or not endDate:
            return {"Error Message": "All Fields Are Required"}

        existingSemester = Semester.query.filter_by(semesterName=semesterName, academicYear=academicYear).first()
        if existingSemester:
            return {"Error Message": f"Semester: {semesterName} For {academicYear} Already Exists"}

        existingSemesterDate = Semester.query.filter_by(academicYear=academicYear, startDate=startDate, endDate=endDate).first()
        if existingSemesterDate:
            return {"Error Message": f"Semester Date: {startDate} - {endDate} Already Exists For {existingSemesterDate.semesterName} - {existingSemesterDate.academicYear}"}

        new_semester = Semester(semesterName=semesterName, academicYear=academicYear, startDate=startDate, endDate=endDate)
        db.session.add(new_semester)
        db.session.commit()
        return {"New Semester Added": {"semesterID": new_semester.semesterID, "semesterName": new_semester.semesterName}}

    except Exception as e:
        print(f"Error While Adding Semester: {e}")
        db.session.rollback()
        return None

def update_semester(semesterName, academicYear, new_semesterName=None, new_academicYear=None, startDate=None, endDate=None):
    try:
        errors = validate_dates(academicYear, startDate, endDate)
        if errors:
            return {"Error Message": errors}

        semester = Semester.query.filter_by(semesterName=semesterName, academicYear=academicYear).first()
        if not semester:
            return {"Error Message": f"Semester {semesterName} For {academicYear} Not Found"}

        if new_semesterName:
            semester.semesterName = new_semesterName
        if new_academicYear:
            semester.academicYear = new_academicYear
        if startDate:
            semester.startDate = startDate
        if endDate:
            semester.endDate = endDate

        db.session.commit()

        return {"Semester Updated": semester}

    except Exception as e:
        print(f"Error While Updating Semester: {e}")
        db.session.rollback()
        return None

def get_semester(semesterName, academicYear):
    try:
        errors = validate_academic_year(academicYear)
        if errors:
            return {"Error Message": errors}

        semester = Semester.query.filter_by(semesterName=semesterName, academicYear=academicYear).first()
        if semester:
            return semester
        else:
            return {"Error Message": f"Semester {semesterName} For {academicYear} Not Found"}

    except Exception as e:
        print(f"Error While Fetching Semester: {e}")
        return None

def list_semesters():
    try:
        semesters = Semester.query.order_by(Semester.semesterName, Semester.academicYear, Semester.startDate).all()
        if not semesters:
            return {"Error Message": "No Semesters Found."}
        return semesters

    except Exception as e:
        print(f"Error While Fetching Semesters: {e}")
        return {"Error Message": "An Error Occurred While Fetching Semesters."}

def list_semesters_json():
    try:
        semesters = Semester.query.order_by(Semester.semesterName, Semester.academicYear, Semester.startDate).all()
        if not semesters:
            return {"Error Message": "No Semesters Found."}

        semester_list = [semester.get_json() for semester in semesters]
        return {"Semesters": semester_list}

    except Exception as e:
        print(f"Error While Fetching Semesters: {e}")
        return {"Error Message": "An Error Occurred While Fetching Semesters."}

def get_semesters_by_academic_year(academicYear):
    try:
        semesters = Semester.query.filter_by(academicYear=academicYear).all()
        if not semesters:
            return {"Semesters for Academic Year": []}

        semesters_json = [semester.get_json() for semester in semesters]
        return {"Semesters for Academic Year": semesters_json}

    except Exception as e:
        print(f"Error while fetching semesters: {e}")
        return None

def list_courses_for_semester(semesterName, academicYear):
    try:
        semester = Semester.query.filter_by(semesterName=semesterName, academicYear=academicYear).first()
        if not semester:
            return {"Error Message": f"Semester {semesterName} for {academicYear} not found"}

        course_offerings = CourseOffering.query.filter_by(semesterID=semester.semesterID).all()
        if not course_offerings:
            return {"Error Message": f"No courses found for {semesterName} {academicYear}"}

        courses = [offering.get_json() for offering in course_offerings]
        return {"Courses for Semester": courses}

    except Exception as e:
        print(f"Error while fetching courses: {e}")
        return None