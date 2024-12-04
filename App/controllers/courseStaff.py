from App.database import db
from App.models import Course, Staff, CourseStaff, Semester, CourseOffering

# Add Staff To A Course In A Given Semester
def add_course_staff(courseCode, semesterName, academicYear, staffID):
    try:
        staff = Staff.query.filter_by(staffID=staffID).first()
        course = Course.query.filter_by(courseCode=courseCode).first()
        semester = Semester.query.filter_by(semesterName=semesterName, academicYear=academicYear).first()
        course_offering = CourseOffering.query.filter_by(courseCode=course.courseCode, semesterID=semester.semesterID).first()

        if not course:
            return {"Error": "Course Not Found"}
        if not semester:
            return {"Error": "Semester Not Found"}
        if not staff:
            return {"Error": "Staff Not Found"}
        if not course_offering:
            return {"Error": "Course Offering Not Found For The Given Semester"}

        already_assigned_staff = CourseStaff.query.filter_by(courseOfferingID=course_offering.offeringID, staffID=staffID).first()
        if already_assigned_staff:
            return {"Error": "Staff member is already assigned to this course"}

        new_course_staff = CourseStaff(courseOfferingID=course_offering.offeringID, staffID=staffID)
        db.session.add(new_course_staff)
        db.session.commit()
        return {"Message": "Staff successfully assigned to the course", "CourseStaff": new_course_staff.get_json()}

    except Exception as e:
        db.session.rollback()
        print(f"Error While Adding Staff To Course: {e}")
        return {"Error": "An Error Occurred While Assigning Staff To The Course"}

# Remove Staff From A Course In A Given Semester
def remove_course_staff(courseCode, semesterName, academicYear, staffID):
    try:
        staff = Staff.query.filter_by(staffID=staffID).first()
        course = Course.query.filter_by(courseCode=courseCode).first()
        semester = Semester.query.filter_by(semesterName=semesterName, academicYear=academicYear).first()
        course_offering = CourseOffering.query.filter_by(courseCode=course.courseCode, semesterID=semester.semesterID).first()

        if not course:
            return {"Error": "Course Not Found"}
        if not semester:
            return {"Error": "Semester Not Found"}
        if not staff:
            return {"Error": "Staff Not Found"}
        if not course_offering:
            return {"Error": "Course Offering Not Found For The Given Semester"}

        assigned_staff = CourseStaff.query.filter_by(courseOfferingID=course_offering.offeringID, staffID=staffID).first()
        if not assigned_staff:
            return {"Error": "Staff Not Assigned To This Course In The Given Semester"}

        db.session.delete(assigned_staff)
        db.session.commit()
        return {"Message": "Staff Successfully Removed From The Course"}

    except Exception as e:
        db.session.rollback()
        print(f"Error While Removing Staff From Course: {e}")
        return {"Error": "An Error Occurred While Removing Staff From The Course"}

# Get Staff Assigned To A Course In A Given Semester
def get_course_staff(courseCode, semesterName, academicYear):
    try:
        course = Course.query.filter_by(courseCode=courseCode).first()
        semester = Semester.query.filter_by(semesterName=semesterName, academicYear=academicYear).first()
        course_offering = CourseOffering.query.filter_by(courseCode=course.courseCode, semesterID=semester.semesterID).first()

        if not course:
            return {"Error": "Course Not Found"}
        if not semester:
            return {"Error": "Semester Not Found"}
        if not course_offering:
            return {"Error": "Course Offering Not Found For The Given Semester"}

        course_staff = CourseStaff.query.filter_by(courseOfferingID=course_offering.offeringID).all()
        if not course_staff:
            return {"Message": "There Are No Staff Assigned To This Course In The Given Semester"}

        return {
            "CourseStaff": [staff.get_json() for staff in course_staff]
        }

    except Exception as e:
        print(f"Error While Fetching Course Staff: {e}")
        return {"Error": "An Error Occurred While Fetching Course Staff"}