from App.database import db
from App.models import Course, Assessment, CourseAssessment

# Link New Course Assessment To Relevant Code
def add_course_assessment(courseCode, assessmentID):
    try:
        course = Course.query.get(courseCode)
        if not course:
            return {"Error": "Course with this courseCode does not exist"}

        assessment = Assessment.query.get(assessmentID)
        if not assessment:
            return {"Error": "Assessment with this assessmentID does not exist"}

        existing_association = CourseAssessment.query.filter_by(courseCode=courseCode, assessmentID=assessmentID).first()
        if existing_association:
            return {"Error": "Assessment is already associated with this course"}

        new_course_assessment = CourseAssessment(
            courseCode=courseCode,
            assessmentID=assessmentID,
            startDate=assessment.startDate,
            dueDate=assessment.dueDate
        )

        db.session.add(new_course_assessment)
        db.session.commit()

        return {"Message": "Course and Assessment successfully associated", "CourseAssessment": new_course_assessment.get_json()}

    except Exception as e:
        db.session.rollback()
        print(f"Error while adding course assessment: {e}")
        return {"Error": "An error occurred while associating the course with the assessment"}

# List All Assessments For A Specific Course (Throughout Time)
def list_course_assessments(courseCode):
    try:
        course_assessments = CourseAssessment.query.filter_by(courseCode=courseCode).all()
        
        if not course_assessments:
            return {"Message": f"No assessments found for course {courseCode}"}
        return {"CourseAssessments": [assessments.get_json() for assessments in course_assessments]}

    except Exception as e:
        print(f"Error while listing course assessments: {e}")
        return {"Error": "An error occurred while fetching course assessments"}

# Get Specific Course Assessment Via AssessmentID
def get_course_assessment(courseAssessmentID):
    try:
        course_assessment = CourseAssessment.query.get(courseAssessmentID)
        
        if not course_assessment:
            return {"Error": "CourseAssessment not found"}
        return {"CourseAssessment": course_assessment.get_json()}

    except Exception as e:
        print(f"Error while fetching course assessment: {e}")
        return {"Error": "An error occurred while fetching the course assessment"}

#Get Specific courseAssesment object via courseCode and assessmentID
def get_course_assessment_by_code_and_id(courseCode, assessmentID):
    try:
        course_assessment = CourseAssessment.query.filter_by(courseCode=courseCode, assessmentID=assessmentID).first()
        
        if not course_assessment:
            return {"Error": "CourseAssessment not found"}
        return course_assessment

    except Exception as e:
        print(f"Error while fetching course assessment: {e}")
        return {"Error": "An error occurred while fetching the course assessment"}

# Unlink CourseAssessment From Course | Deletes The Associated Assessment As Well
def delete_course_assessment(courseAssessmentID):
    try:
        course_assessment = CourseAssessment.query.get(courseAssessmentID)

        if not course_assessment:
            return {"Error": "CourseAssessment not found"}

        assessment = course_assessment.assessment

        if not assessment.assessment_courses:  # Safe Guard
            db.session.delete(assessment)

        db.session.delete(course_assessment)
        db.session.commit()
        return {"Message": "CourseAssessment and associated Assessment deleted"}

    except Exception as e:
        db.session.rollback()
        print(f"Error while deleting course assessment: {e}")
        return {"Error": "An error occurred while deleting the course assessment"}
