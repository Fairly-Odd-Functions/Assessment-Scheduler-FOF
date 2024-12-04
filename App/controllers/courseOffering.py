from App.database import db
from App.models import Course, Semester, CourseOffering

# Link Course To Semester
def add_course_offering(courseCode, semesterID, totalStudentsEnrolled=0):
    try:
        course = Course.query.filter_by(courseCode=courseCode).first()
        if not course:
            return {"Error": "Course Not Found"}

        semester = Semester.query.get(semesterID)
        if not semester:
            return {"Error": "Semester Not Found"}

        existing_offering = CourseOffering.query.filter_by(courseCode=courseCode, semesterID=semester.semesterID).first()
        if existing_offering:
            return {"Message": "This course is already offered in this semester"}

        new_offering = CourseOffering(courseCode=courseCode, semesterID=semesterID, totalStudentsEnrolled=totalStudentsEnrolled)
        db.session.add(new_offering)
        db.session.commit()

        return {"Message": "Course offering added successfully", "CourseOffering": new_offering.get_json()}
    
    except Exception as e:
        db.session.rollback()
        print(f"Error while adding course offering: {e}")
        return {"Error": "An error occurred while adding the course offering"}

# Remove Course Offering Link If Course Is No Longer Offered
def remove_course_offering(courseCode, semesterID):
    try:
        course = Course.query.filter_by(courseCode=courseCode).first()
        if not course:
            return {"Error": "Course Not Found"}

        semester = Semester.query.get(semesterID)
        if not semester:
            return {"Error": "Semester Not Found"}

        offering = CourseOffering.query.filter_by(courseCode=courseCode, semesterID=semesterID).first()
        if not offering:
            return {"Error": "Course offering not found for this semester"}

        db.session.delete(offering)
        db.session.commit()

        return {"Message": "Course Offering Removed Successfully"}
    
    except Exception as e:
        db.session.rollback()
        print(f"Error while removing course offering: {e}")
        return {"Error": "An error occurred while removing the course offering"}

# Get A Specific Course Offering Based On Academic Year & Semester
def get_course_offering(courseCode, semesterID):
    try:
        course = Course.query.filter_by(courseCode=courseCode).first()
        if not course:
            return {"Error": "Course Not Found"}
        semester = Semester.query.get(semesterID)
        if not semester:
            return {"Error": "Semester Not Found"}

        course_offering = CourseOffering.query.filter_by(courseCode=courseCode, semesterID=semesterID).first()
        if not course_offering:
            return {"Message": f"Course Offering Not Found For {courseCode} In Academic Year {semester.academicYear}"}
        return course_offering

    except Exception as e:
        print(f"Error while fetching course offering: {e}")
        return {"Error": "An error occurred while fetching course offering"}

# Get All Course Offerings Based On Academic Year
def get_course_offerings(courseCode, academicYear):
    try:
        course = Course.query.filter_by(courseCode=courseCode).first()
        if not course:
            return {"Error": "Course Not Found"}

        course_offerings = CourseOffering.query.join(Semester).filter_by(courseCode=courseCode, academicYear=academicYear).all()

        if not course_offerings:
            return {"Message": f"No Course Offerings Found For {courseCode} In Academic Year {academicYear}"}

        return {
            "CourseOfferings": [offering.get_json() for offering in course_offerings]
        }
    except Exception as e:
        print(f"Error while fetching course offerings: {e}")
        return {"Error": "An error occurred while fetching course offerings"}