from App.database import db
from App.models import Semester, CourseOffering
from App.services.semester import validate_dates

def add_semester(semesterName, academicYear, startDate, endDate):
    try:
        errors = validate_dates(academicYear, startDate, endDate)
        if errors:
            return {"Error Message": errors}

        if not semesterName or not academicYear or not startDate or not endDate:
            return {"Error Message": "All fields are required"}

        existingSemester = Semester.query.filter_by(semesterName=semesterName, academicYear=academicYear).first()
        if existingSemester:
            return {"Error Message": f"Semester {semesterName} for {academicYear} already exists"}

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
        semester = Semester.query.filter_by(semesterName=semesterName, academicYear=academicYear).first()
        if not semester:
            return {"Error Message": f"Semester {semesterName} for {academicYear} not found"}

        if new_semesterName:
            semester.semesterName = new_semesterName
        if new_academicYear:
            semester.academicYear = new_academicYear
        if startDate:
            semester.startDate = startDate
        if endDate:
            semester.endDate = endDate

        db.session.commit()

        return {"Semester Updated": semester.get_json()}

    except Exception as e:
        print(f"Error while updating semester: {e}")
        db.session.rollback()
        return None

def get_semester(semesterName, academicYear):
    try:
        semester = Semester.query.filter_by(semesterName=semesterName, academicYear=academicYear).first()
        if semester:
            return semester.get_json()
        else:
            return {"Error Message": f"Semester {semesterName} for {academicYear} not found"}

    except Exception as e:
        print(f"Error while fetching semester: {e}")
        return None

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