from datetime import datetime, timedelta
from App.controllers.course import get_degree_programme
from App.controllers.courseProgramme import get_course_programme
from App.models import CourseProgramme, CourseAssessment, CourseOffering

def validate_assessment_clash(new_course_assessment):
    clash_rule = new_course_assessment.clashRule
    course_code = new_course_assessment.courseCode
    start_date = new_course_assessment.startDate
    start_time = new_course_assessment.startTime
    end_date = new_course_assessment.endDate
    end_time = new_course_assessment.endTime

    if clash_rule == "DEGREE":
        clash_validation_result = validate_by_degree(course_code, start_date, start_time, end_date, end_time)
        if clash_validation_result["status"] == "error":
            return clash_validation_result
    elif clash_rule == "STUDENT_OVERLAP":
        pass

    elif clash_rule == "ASSESSMENT_TYPE":
        pass
    return {"status": "success", "message": "No clashes detected"}

# Clash Rule for Validation of Assesment Schedule by Programm
# -> Checks whether an assessment for a course clashes with another assessment
#    in the same degree programme, on the same day.
def validate_by_degree(courseCode, start_date, start_time, end_date, end_time):
    try:
        programme = get_degree_programme(courseCode)
        all_courses_in_programme = get_course_programme(programme.programmeID)

        if "Error" in all_courses_in_programme:
            return all_courses_in_programme

        for course_programme in all_courses_in_programme["CourseProgrammes"]:
            other_courseCode = course_programme['courseCode']

            course_assessments = CourseAssessment.query.filter_by(courseCode=other_courseCode).all()
            for course_assessment in course_assessments:
                other_start_date = course_assessment.startDate
                other_end_date = course_assessment.endDate
                other_start_time = course_assessment.startTime
                other_end_time = course_assessment.endTime

                if courseCode == other_courseCode:
                    continue

                current_start_datetime = datetime.combine(start_date, start_time)
                current_end_datetime = datetime.combine(end_date, end_time)

                other_start_datetime = datetime.combine(other_start_date, other_start_time)
                other_end_datetime = datetime.combine(other_end_date, other_end_time)

                if (current_start_datetime < other_end_datetime and current_end_datetime > other_start_datetime):
                    return {
                        "status": "error",
                        "message": f"Assessment clash found with {other_courseCode} in the same programme."
                    }
        return {
            "status": "success",
            "message": "No assessment clashes found in the same programme."
        }
    except Exception as e:
        print(f"Error: {e}")
        return {"status": "error", "message": "Failed to validate courses."}

# Clash Rule for Validation of Assesment Schedule by Percentage Overlap
# -> Checks all courses scheduled on the same day to see if the number of students 
#    taking each of those courses exceeds the threshold, calculated based 
#    on the percentage of overlapping student enrollment.m
def validate_by_student_overlap(courseCode, startDate, endDate, overlap_threshold):

    overlaping_courses = CourseAssessment.query.filter(
        (CourseAssessment.startDate <= endDate) &
        (CourseAssessment.endDate >= startDate)
    ).all()

    course_offering = CourseOffering.query.filter_by(courseCode=courseCode).first()
    if not course_offering:
        return {"status": "error", "message": "Course offering not found for the provided course code"}

    total_students = course_offering.totalStudentsEnrolled

    for overlap_course in overlaping_courses:
        overlap_offering = CourseOffering.query.filter_by(courseCode=overlap_course.courseCode).first()

        if not overlap_offering:
            continue

        overlap_students = overlap_offering.totalStudentsEnrolled
        overlap_percentage = (overlap_students / total_students) * 100

        if overlap_percentage > overlap_threshold:
            return {"status": "error", "message": "Assessment clash found due to overlapping student enrollment"}

    return {"status": "success", "message": "No assessment clashes found due to overlapping student enrollment"}

# Clash Rule for Validation of Assement Schdule by Assesment Type
# -> Checks if an assessment follows the required preparation time before it starts, 
#    based on its assesment type.
def validate_by_assessment_type(assessment, startDate, preparation_days):

    if assessment.type not in ["Exam", "Quiz", "Final"]:
        return {"status": "error", "message": f"Unknown assessment type: {assessment.type}"}

    reserved_start_date = startDate - timedelta(days=preparation_days)

    conflicting_assessments = CourseAssessment.query.filter(
        CourseAssessment.startDate <= startDate,
        CourseAssessment.endDate >= reserved_start_date
    ).all()

    overlapped_assessments = []

    if conflicting_assessments:
        for conflicting_assessment in conflicting_assessments:
            overlapped_assessments.append({
                "courseCode": conflicting_assessment.courseCode,
                "assessmentType": conflicting_assessment.type,
                "startDate": conflicting_assessment.startDate,
                "endDate": conflicting_assessment.endDate
            })
        return {
            "status": "error", 
            "message": "Assessment clash found due to insufficient preparation time",
            "ConflictingAssessments": overlapped_assessments
        }
    else:
        return {"status": "success", "message": "No assessment clashes found"}