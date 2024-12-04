from App.database import db
from App.models import Course
from App.models.courseProgramme import CourseProgramme
from App.models.programme import Programme

def add_course(courseCode, courseTitle, courseCredits, courseDescription, courseLevel):
    try:
        existing_course = Course.query.get(courseCode)
        if existing_course: 
            return {"Error": "Course With This courseCode Already Exists"}

        new_course = Course(
            courseCode=courseCode,
            courseTitle=courseTitle,
            courseCredits=courseCredits,
            courseDescription=courseDescription,
            courseLevel=courseLevel
        )

        db.session.add(new_course)
        db.session.commit()
        return {"Message": "New Course Added", "Course": new_course.get_json()}

    except Exception as e:
        db.session.rollback()
        print(f"Error while adding course: {e}")
        return {"Error": "An error occurred while adding the course"}

def list_courses():
    courses = Course.query.all()
    return [course.get_json() for course in courses] 

def get_course_by_code(courseCode):
    course = Course.query.filter_by(courseCode=courseCode).first()
    if not course:
        return {"Error": "Course Not Found"}
    return course.get_json()

def get_course(courseCode):
    course = Course.query.filter_by(courseCode=courseCode).first()
    if not course:
        return {"Error": "Course Not Found"}
    return course

def edit_course(courseCode, new_courseTitle=None, new_courseCredits=None, new_courseDescription=None, new_courseLevel=None):
    try:
        course = Course.query.filter_by(courseCode=courseCode).first()
        if not course:
            return {"Error": "Course not found"}

        if new_courseTitle:
            course.courseTitle = new_courseTitle
        if new_courseCredits:
            course.courseCredits = new_courseCredits
        if new_courseDescription:
            course.courseDescription = new_courseDescription
        if new_courseLevel:
            course.courseLevel = new_courseLevel

        db.session.commit()
        return {"Message": "Course Updated", "Course": course.get_json()}
    
    except Exception as e:
        db.session.rollback()
        print(f"Error while updating course: {e}")
        return {"Error": "An error occurred while updating the course"}

def get_degree_programme(courseCode):
    try:
        course = Course.query.get(courseCode)
        if not course:
            raise ValueError(f"No course found with courseCode: {courseCode}")

        course_programme = CourseProgramme.query.filter_by(courseCode=courseCode).first()
        if not course_programme:
            raise ValueError(f"Course {courseCode} is not associated with any program.")

        return course_programme

    except Exception as e:
        print(f"Error while fetching degree program for course {courseCode}: {e}")
        return None 
