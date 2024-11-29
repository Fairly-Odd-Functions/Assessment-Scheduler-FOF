from App.database import db
from App.models import Course, Programme, CourseProgramme

# Get All Courses Associated With A Specific Programme
def get_course_programme(programmeID):
    try:
        programme = Programme.query.filter_by(programmeID=programmeID).first()
        if not programme:
            return {"Error": "Programme Not Found"}

        course_programmes = CourseProgramme.query.filter_by(programmeID=programmeID).all()
        if not course_programmes:
            return {"Message": "No courses found for this programme"}

        return {
            "CourseProgrammes": [course_programme.get_json() for course_programme in course_programmes]
        }
    except Exception as e:
        print(f"Error while fetching course-programme association: {e}")
        return {"Error": "An error occurred while fetching course-programme associations"}

# Add Course To A Programme
def add_course_to_programme(courseCode, programmeID):
    try:
        course = Course.query.filter_by(courseCode=courseCode).first()
        if not course:
            return {"Error": "Course Not Found"}

        programme = Programme.query.filter_by(programmeID=programmeID).first()
        if not programme:
            return {"Error": "Programme Not Found"}

        existing_association = CourseProgramme.query.filter_by(courseCode=courseCode, programmeID=programmeID).first()
        if existing_association:
            return {"Message": "This course is already part of the programme"}

        new_course_programme = CourseProgramme(courseCode=courseCode, programmeID=programmeID)
        db.session.add(new_course_programme)
        db.session.commit()

        return {"Message": "Course successfully added to the programme", "CourseProgramme": new_course_programme.get_json()}
    except Exception as e:
        db.session.rollback()
        print(f"Error while adding course to programme: {e}")
        return {"Error": "An error occurred while adding course to the programme"}

# Remove Course From a Programme
def remove_course_from_programme(courseCode, programmeID):
    try:
        course = Course.query.filter_by(courseCode=courseCode).first()
        if not course:
            return {"Error": "Course Not Found"}

        programme = Programme.query.filter_by(programmeID=programmeID).first()
        if not programme:
            return {"Error": "Programme Not Found"}

        course_programme = CourseProgramme.query.filter_by(courseCode=courseCode, programmeID=programmeID).first()
        if not course_programme:
            return {"Error": "Course is not part of this programme"}

        db.session.delete(course_programme)
        db.session.commit()

        return {"Message": "Course successfully removed from the programme"}
    except Exception as e:
        db.session.rollback()
        print(f"Error while removing course from programme: {e}")
        return {"Error": "An error occurred while removing course from the programme"}
