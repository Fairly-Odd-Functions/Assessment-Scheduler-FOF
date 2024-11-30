from datetime import datetime, timedelta
from App.controllers.course import get_degree_programme
from App.controllers.courseProgramme import get_course_programme
from App.controllers.programme import get_programme_by_id
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
        clash_validation_result = validate_by_student_overlap(course_code, start_date, end_date, overlap_threshold=50)
        if clash_validation_result["status"] == "error":
            return clash_validation_result

    elif clash_rule == "ASSESSMENT_TYPE":
        pass
        # clash_validation_result = validate_by_assessment_type(course_code, start_date, start_time, end_date, end_time)
        # if clash_validation_result["status"] == "error":
        #     return clash_validation_result

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
            programme_id = course_programme['programmeID']
            other_courseProgramme = get_programme_by_id(programme_id)
            other_courseProgrammeTitle = other_courseProgramme.programmeTitle if other_courseProgramme else "Unknown Programme"

            course_assessments = CourseAssessment.query.filter_by(courseCode=other_courseCode).all()
            for course_assessment in course_assessments:
                other_start_date = course_assessment.startDate
                other_end_date = course_assessment.endDate
                other_start_time = course_assessment.startTime
                other_end_time = course_assessment.endTime
                other_assessmentTitle = course_assessment.assessment.assessmentTitle
                other_assessmentType = course_assessment.assessment.assessmentType

                if courseCode == other_courseCode:
                    continue

                current_start_datetime = datetime.combine(start_date, start_time)
                current_end_datetime = datetime.combine(end_date, end_time)

                other_start_datetime = datetime.combine(other_start_date, other_start_time)
                other_end_datetime = datetime.combine(other_end_date, other_end_time)

                if (current_start_datetime < other_end_datetime and current_end_datetime > other_start_datetime):
                    error_message = (
                            f"\nDegree Clash Detected!\n"
                            f"{'='*50}\n"
                            f"Clashing Course(s):\n"
                            f"  - CourseCode: {other_courseCode}\n"
                            f"  - Degree Programme: {other_courseProgrammeTitle}\n"
                            f"  - AssessmentTitle: {other_assessmentTitle}\n"
                            f"  - AssessmentType: {other_assessmentType}\n"
                            f"  - Start Time: {other_start_datetime.strftime('%Y-%m-%d %H:%M')}\n"
                            f"  - End Time: {other_end_datetime.strftime('%Y-%m-%d %H:%M')}\n"
                            f"{'='*50}"
                    )
                    return {"status": "error", "message": error_message}
        return {
            "status": "success",
            "message": "No Assessment Clashes Found In The Same Programme."
        }
    except Exception as e:
        print(f"Error: {e}")
        return {"status": "error", "message": "Failed To Validate Courses."}

# Clash Rule for Validation of Assesment Schedule by Percentage Overlap
# -> Checks all courses scheduled on the same day to see if the number of students 
#    taking each of those courses exceeds the threshold, calculated based 
#    on the percentage of overlapping student enrollment
def validate_by_student_overlap(courseCode, startDate, endDate, overlap_threshold):
    overlap_courses = CourseAssessment.query.filter(
        (CourseAssessment.startDate <= endDate) &
        (CourseAssessment.endDate >= startDate)
    ).all()
    # print(f"Found {len(overlap_courses)} Overlapping Courses")

    course_offering = CourseOffering.query.filter_by(courseCode=courseCode).first()
    if not course_offering:
        return {"status": "error", "message": "CourseOffering Not Found For The Provided Course Code"}

    total_students = course_offering.totalStudentsEnrolled

    for overlap_course in overlap_courses:
        overlap_offering = CourseOffering.query.filter_by(courseCode=overlap_course.courseCode).first()
        if not overlap_offering:
            continue

        overlap_students = overlap_offering.totalStudentsEnrolled
        overlap_percentage = (overlap_students / total_students) * 100
        if overlap_percentage > overlap_threshold:
            # print(f"DEBUG: Overlap Percentage {overlap_percentage:.2f}% Exceeds Threshold {overlap_threshold}%")

            error_message = (
                f"\nAssessment Clash Found Due To Overlapping Student Enrollment\n"
                f"{'='*50}\n"
                f"Overlapping Course(s):\n"
                f"- Course 1: {courseCode} (Total Students: {total_students})\n"
                f"- Course 2: {overlap_offering.courseCode} "
                f"(Total Students: {overlap_students}, Overlap: {overlap_percentage:.2f}%)\n"
                f"{'='*50}"
            )
            return {"status": "error", "message": error_message}
    return {"status": "success", "message": "No Assessment Clashes Found Due To Overlapping Student Enrollment"}

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