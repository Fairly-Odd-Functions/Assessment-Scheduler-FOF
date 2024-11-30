import calendar
from prettytable import PrettyTable
from datetime import datetime, time, date
from App.controllers.course import get_degree_programme
from App.controllers.courseProgramme import get_course_programme
from App.models.courseAssessment import CourseAssessment

def validate_dates(startDate, endDate):
    errors = []

    if isinstance(startDate, datetime):
        startDate = startDate.date()
    elif not isinstance(startDate, date):
        errors.append("Invalid Start Date. It Must Be A Datetime Object or Date Object.")

    if isinstance(endDate, datetime):
        endDate = endDate.date()
    elif not isinstance(endDate, date):
        errors.append("Invalid End Date. It Must Be A Datetime Object or Date Object.")

    if startDate > endDate:
        errors.append("Start Date Must Be Before End Date.")

    if errors:
        return {"Error Message": errors}
    return {"startDate": startDate, "endDate": endDate}

def validate_times(startTime, endTime):
    errors = []

    if isinstance(startTime, datetime):
        startTime = startTime.time()
    elif not isinstance(startTime, time):
        errors.append("Invalid Start Time. It Must Be A Time Object or Datetime Object.")

    if isinstance(endTime, datetime):
        endTime = endTime.time()
    elif not isinstance(endTime, time):
        errors.append("Invalid End Time. It Must Be A Time Object or Datetime Object.")

    if startTime >= endTime:
        errors.append("Start Time Must Be Before End Time.")

    if errors:
        return {"Error Message": errors}
    return {"startTime": startTime, "endTime": endTime}

def generate_calendar(year, month, course_code):
    cal = calendar.Calendar(firstweekday=calendar.SUNDAY)
    month_days = cal.monthdayscalendar(year, month)

    table = PrettyTable()
    table.field_names = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

    # STEP 1: Get The Programme Of The Given Course
    programme = get_degree_programme(course_code)
    if not programme:
        return "Program not found for this course."

    # STEP 2: Get All Courses In The Same Programme
    all_courses_in_programme = get_course_programme(programme.programmeID)
    
    if "Error" in all_courses_in_programme:
        return all_courses_in_programme

    # STEP 3: Collect All The Assessments For The Courses In The Programme
    assessments_by_date = {}
    for course_programme in all_courses_in_programme["CourseProgrammes"]:
        other_course_code = course_programme['courseCode']

        course_assessments = CourseAssessment.query.filter_by(courseCode=other_course_code).all()
        for course_assessment in course_assessments:
            assessment_date = course_assessment.startDate.date() if isinstance(course_assessment.startDate, datetime) else course_assessment.startDate
            print(f"DEBUG: Assessment for {other_course_code} on {assessment_date}")  # DEBUGGING

            assessments_by_date.setdefault(assessment_date, []).append(course_assessment)

    # STEP 4: Fill The Calendar With Days And Mark Unavailable Dates With "X"
    for week in month_days:
        row = []
        for day in week:
            if day == 0:
                row.append(" ")
            else:
                day_str = str(day).zfill(2)
                day_date = datetime(year, month, day).date()
                if day_date in assessments_by_date:
                    row.append("[X]")
                else:
                    row.append(day_str)
        table.add_row(row)
    return table