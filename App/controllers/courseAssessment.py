from App.controllers.clashDetection import validate_assessment_clash
from App.database import db
from App.services.assessment import *
from App.models import Course, Assessment, CourseAssessment

# Link New Course Assessment To Relevant Code
def add_course_assessment(courseCode, assessmentID, startDate, startTime, endDate, endTime, clashRule=None):
    try:
        course = Course.query.get(courseCode)
        if not course:
            return {"Error": "Course With This CourseCode Does Not Exist"}

        assessment = Assessment.query.get(assessmentID)
        if not assessment:
            return {"Error": "Assessment With This AssessmentID Does Not Exist"}

        date_validation = validate_dates(startDate, endDate)
        if "Error Message" in date_validation:
            return {"Error": date_validation["Error Message"]}

        time_validation = validate_times(startTime, endTime)
        if "Error Message" in time_validation:
            return {"Error": time_validation["Error Message"]}

        existing_association = CourseAssessment.query.filter_by(courseCode=courseCode,
                                                                assessmentID=assessmentID).first()
        if existing_association:
            return {"Error": "Assessment Is Already Associated With This Course"}

        new_course_assessment = CourseAssessment(
            courseCode=courseCode,
            assessmentID=assessmentID,
            startDate=date_validation["startDate"],
            endDate=date_validation["endDate"],
            startTime=time_validation["startTime"],
            endTime=time_validation["endTime"],
            clashRule=clashRule.upper()
        )

        validation_result = validate_assessment_clash(new_course_assessment)
        if validation_result["status"] == "error":
            return validation_result

        db.session.add(new_course_assessment)
        db.session.commit()
        return {"Message": "Course And Assessment Successfully Associated",
                "CourseAssessment": new_course_assessment.get_json()}

    except Exception as e:
        db.session.rollback()
        print(e)
        return {"Error": "An Error Occurred While Associating The Course With The Assessment"}

# Reschedule An Assessment
def reschedule_course_assessment(courseAssessmentID, newStartDate, newStartTime, newEndDate, newEndTime):
    try:
        course_assessment = CourseAssessment.query.get(courseAssessmentID)
        if not course_assessment:
            return {"Error": "CourseAssessment Not Found"}

        date_validation = validate_dates(newStartDate, newEndDate)
        if "Error Message" in date_validation:
            return {"Error": date_validation["Error Message"]}

        time_validation = validate_times(newStartTime, newEndTime)
        if "Error Message" in time_validation:
            return {"Error": time_validation["Error Message"]}

        course_assessment.startDate = date_validation["startDate"]
        course_assessment.endDate = date_validation["endDate"]
        course_assessment.startTime = time_validation["startTime"]
        course_assessment.endTime = time_validation["endTime"]

        validation_result = validate_assessment_clash(course_assessment)
        if validation_result["status"] == "error":
            return validation_result

        db.session.commit()
        return {"Message": "CourseAssessment Successfully Rescheduled",
                "CourseAssessment": course_assessment.get_json()}

    except Exception as e:
        db.session.rollback()
        print(f"Error While Rescheduling Course Assessment: {e}")
        return {"Error": "An Error Occurred While Rescheduling The Course Assessment"}

# List All Assessments For A Specific Course (Throughout Time)
def list_course_assessments(courseCode):
    try:
        course_assessments = CourseAssessment.query.filter_by(courseCode=courseCode).all()
        
        if not course_assessments:
            return {"Message": f"No Assessments Found For Course {courseCode}"}
        return {"CourseAssessments": [assessments.get_json() for assessments in course_assessments]}

    except Exception as e:
        print(f"Error While Listing Course Assessments: {e}")
        return {"Error": "An Error Occurred While Fetching Course Assessments"}

# Get Specific Course Assessment Via AssessmentID
def get_course_assessment(courseAssessmentID):
    try:
        course_assessment = CourseAssessment.query.get(courseAssessmentID)
        
        if not course_assessment:
            return {"Error": "CourseAssessment Not Found"}
        return {"CourseAssessment": course_assessment.get_json()}

    except Exception as e:
        print(f"Error While Fetching Course Assessment: {e}")
        return {"Error": "An Error Occurred While Fetching The Course Assessment"}

# Get Specific courseAssesment
def get_course_assessment_by_code_and_id(courseCode, assessmentID, startDate, startTime, endDate, endTime):
    try:
        course_assessment = CourseAssessment.query.filter_by(courseCode=courseCode, 
                                                             assessmentID=assessmentID,
                                                             startDate=startDate,
                                                             startTime=startTime,
                                                             endDate=endDate,
                                                             endTime=endTime).first()

        if not course_assessment:
            return {"Error": "CourseAssessment Not Found"}
        return course_assessment

    except Exception as e:
        print(f"Error While Fetching Course Assessment: {e}")
        return {"Error": "An Error Occurred While Fetching The Course Assessment"}

# Unlink CourseAssessment From Course | Deletes The Associated Assessment As Well
def delete_course_assessment(courseAssessmentID):
    try:
        course_assessment = CourseAssessment.query.get(courseAssessmentID)

        if not course_assessment:
            return {"Error": "CourseAssessment Not Found"}

        assessment = course_assessment.assessment

        if not assessment.assessment_courses:  # Safe Guard
            db.session.delete(assessment)

        db.session.delete(course_assessment)
        db.session.commit()
        return {"Message": "CourseAssessment And Associated Assessment Deleted"}

    except Exception as e:
        db.session.rollback()
        print(f"Error While Deleting Course Assessment: {e}")
        return {"Error": "An Error Occurred While Deleting The Course Assessment"}

# Get All Scheduled Assessments For A Specific Course Given A Date Range (Too Tired For Error Handling)
def get_scheduled_assessments(courseCode, start_date, end_date):
    try:
        assessments = CourseAssessment.query.filter(
            CourseAssessment.courseCode == courseCode,
            CourseAssessment.startDate >= start_date,
            CourseAssessment.endDate <= end_date
        ).all()

        if not assessments:
            return {"Error": "No Scheduled Assessments Found For Given Criteria."}
        return {"CourseAssessments": [assessment.get_json() for assessment in assessments]}

    except Exception as e:
        print(f"Error While Fetching Scheduled Assessments: {e}")
        return {"Error": "An Error Occurred While Retrieving The Scheduled Assessments."}