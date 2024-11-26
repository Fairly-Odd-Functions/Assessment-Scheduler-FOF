from App.database import db

from App.models import CourseProgramme
from App.models import CourseAssessment
from App.models import CourseOffering

from datetime import timedelta

# Clash Rule for Validation of Assesment Schedule by Programm
# -> Checks whether an assessment for a course clashes with another assessment
#    in the same degree programme, on the same day.
def validate_by_degree(courseCode, assessment, start_date, end_date):

    # Retrieving all programmes associated with the given course
    related_programmes = CourseProgramme.query.filter_by(courseCode=courseCode).all()
    
    if not related_programmes:
        return {"Error": "No related degree programmes found for the course"}
    
    # Collecting all the courses in the same programme
    programme_courses = []
    for programme in related_programmes:
        programme_courses.extend(CourseProgramme.query.filter_by(programmeID=programme.programmeID).all())
    
    # Checking for clashes with other assessments in the same programme
    for programme in programme_courses:
        if programme.courseCode != courseCode:
            clashes = CourseAssessment.query.filter_by(courseCode=programme.courseCode, 
                                                       startDate=start_date, 
                                                       endDate=end_date).all()
            if clashes:
                return {"Error": "Assessment clash found with another course in the same programme"}
    
    return {"Success": "No assessment clashes found in the same programme"}


# Clash Rule for Validation of Assesment Schedule by Percentage Overlap
# -> Checks all courses scheduled on the same day to see if the number of students 
#    taking each of those courses exceeds the threshold, calculated based 
#    on the percentage of overlapping student enrollment.m
def validate_by_student_overlap(courseCode, assessment, startDate, dueDate, overlap_threshold):
    
    # Getting all courses which overlap schedule
    overlaping_courses = CourseAssessment.query.filter(
        (CourseAssessment.startDate >= startDate) & (CourseAssessment.startDate <= dueDate) |
        (CourseAssessment.dueDate >= startDate) & (CourseAssessment.dueDate <= dueDate)).all()

    # Obtaining the total number of students in the course to be scheduled
    total_students = CourseOffering.query.filter_by(courseCode=courseCode).first().totalStudentsEnrolled

    # Iterating over the overlapping courses
    for overlap_course in overlaping_courses:
        # Get the number of students in the overlapping course
        overlap_students = CourseOffering.query.filter_by(courseCode=overlap_course.courseCode).first().totalStudentsEnrolled
        
        # Calculate the overlap percentage
        overlap_percentage = (overlap_students / total_students) * 100
        
        # Check if the overlap percentage exceeds the threshold
        if overlap_percentage > overlap_threshold:
            return {"Error": "Assessment clash found due to overlapping student enrollment"}
    
    return {"Success": "No assessment clashes found due to overlapping student enrollment"}


# Clash Rule for Validation of Assement Schdule by Assesment Type
# -> Checks if an assessment follows the required preparation time before it starts, 
#    based on its assesment type.
def validate_by_assessment_type(assessment, startDate, preparation_days):

    # Checking if the assessment requires preparation days
    if assessment.type in ["Exam", "Quiz", "Final"]:
        # Calculate the start of the reserved preparation period
        reserved_start_date = startDate - timedelta(days=preparation_days)

    # Obtaining conflicting assessments within the reserved period
    conflicting_assessments = CourseAssessment.query.filter(
            CourseAssessment.startDate <= startDate,
            CourseAssessment.dueDate >= reserved_start_date).all()
    
    # Checking if there are any conflicting assessments
    if conflicting_assessments:
        return {"Error": "Assessment clash found due to insufficient preparation time"}
    else:   
        return {"Success": "No assessment clashes found"}