from datetime import timedelta
from App.models import CourseProgramme, CourseAssessment, CourseOffering

# Clash Rule for Validation of Assesment Schedule by Programm
# -> Checks whether an assessment for a course clashes with another assessment
#    in the same degree programme, on the same day.
def validate_by_degree(courseCode, start_date, end_date):

    related_programmes = CourseProgramme.query.filter_by(courseCode=courseCode).all()
    if not related_programmes:
        return {"status": "error", "message": "No related degree programmes found for the course"}

    programme_ids = [prog.programmeID for prog in related_programmes]
    programme_courses = CourseProgramme.query.filter(CourseProgramme.programmeID.in_(programme_ids)).all()

    for programme in programme_courses:
        if programme.courseCode != courseCode:
            clashes = CourseAssessment.query.filter(
                CourseAssessment.courseCode == programme.courseCode,
                CourseAssessment.startDate <= end_date,
                CourseAssessment.endDate >= start_date
            ).all()

            if clashes:
                return {"status": "error", "message": "Assessment clash found with another course in the same programme"}

    return {"status": "success", "message": "No assessment clashes found in the same programme"}

# Clash Rule for Validation of Assesment Schedule by Percentage Overlap
# -> Checks all courses scheduled on the same day to see if the number of students 
#    taking each of those courses exceeds the threshold, calculated based 
#    on the percentage of overlapping student enrollment.m
def validate_by_student_overlap(courseCode, startDate, dueDate, overlap_threshold):

    overlaping_courses = CourseAssessment.query.filter(
        (CourseAssessment.startDate <= dueDate) &
        (CourseAssessment.dueDate >= startDate)
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
        CourseAssessment.dueDate >= reserved_start_date
    ).all()

    overlapped_assessments = []

    if conflicting_assessments:
        for conflicting_assessment in conflicting_assessments:
            overlapped_assessments.append({
                "courseCode": conflicting_assessment.courseCode,
                "assessmentType": conflicting_assessment.type,
                "startDate": conflicting_assessment.startDate,
                "endDate": conflicting_assessment.dueDate
            })
        return {
            "status": "error", 
            "message": "Assessment clash found due to insufficient preparation time",
            "ConflictingAssessments": overlapped_assessments
        }
    else:
        return {"status": "success", "message": "No assessment clashes found"}