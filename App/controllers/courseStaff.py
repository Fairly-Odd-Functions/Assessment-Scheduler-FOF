from App.database import db
from App.models import Course, Staff, CourseStaff, Semester

# Add Staff To A Course In A Given Semester
def add_course_staff(courseCode, semesterName, academicYear, staffID):
    try:
        course = Course.query.filter_by(courseCode=courseCode).first()
        if not course:
            return {"Error": "Course Not Found"}

        semester = Semester.query.filter_by(semesterName=semesterName, academicYear=academicYear).first()
        if not semester:
            return {"Error": "Semester Not Found"}

        staff = Staff.query.filter_by(staffID=staffID).first()
        if not staff:
            return {"Error": "Staff Not Found"}

        existing_assignment = CourseStaff.query.filter_by(courseCode=courseCode, staffID=staffID).first()
        if existing_assignment:
            return {"Message": "This staff member is already assigned to this course in the given semester"}

        new_course_staff = CourseStaff(courseCode=courseCode, staffID=staffID)
        db.session.add(new_course_staff)
        db.session.commit()

        return {"Message": "Staff successfully assigned to the course", "CourseStaff": new_course_staff.get_json()}
    except Exception as e:
        db.session.rollback()
        print(f"Error while adding staff to course: {e}")
        return {"Error": "An error occurred while assigning staff to the course"}

# Remove Staff From A Course In A Given Semester
def remove_course_staff(courseCode, semesterName, academicYear, staffID):
    try:
        course = Course.query.filter_by(courseCode=courseCode).first()
        if not course:
            return {"Error": "Course Not Found"}

        semester = Semester.query.filter_by(semesterName=semesterName, academicYear=academicYear).first()
        if not semester:
            return {"Error": "Semester Not Found"}

        staff = Staff.query.filter_by(staffID=staffID).first()
        if not staff:
            return {"Error": "Staff Not Found"}

        course_staff = CourseStaff.query.filter_by(courseCode=courseCode, semesterID=semester.semesterID, staffID=staffID).first()
        if not course_staff:
            return {"Error": "Staff not assigned to this course in the given semester"}

        db.session.delete(course_staff)
        db.session.commit()

        return {"Message": "Staff successfully removed from the course"}
    except Exception as e:
        db.session.rollback()
        print(f"Error while removing staff from course: {e}")
        return {"Error": "An error occurred while removing staff from the course"}

# Get Staff Assigned To A Course In A Given Semester
def get_course_staff(courseCode, semesterName, academicYear):
    try:
        # Fetch the course
        course = Course.query.filter_by(courseCode=courseCode).first()
        if not course:
            return {"Error": "Course Not Found"}

        # Ensure the semester exists
        semester = Semester.query.filter_by(semesterName=semesterName, academicYear=academicYear).first()
        if not semester:
            return {"Error": "Semester Not Found"}

        # Fetch staff assigned to this course in the given semester
        course_staff = CourseStaff.query.filter_by(courseCode=courseCode).join(Semester).filter(Semester.semesterID == semester.semesterID).all()
        if not course_staff:
            return {"Message": "No staff assigned to this course in the given semester"}

        return {
            "CourseStaff": [staff.get_json() for staff in course_staff]
        }
    except Exception as e:
        print(f"Error while fetching course staff: {e}")
        return {"Error": "An error occurred while fetching course staff"}