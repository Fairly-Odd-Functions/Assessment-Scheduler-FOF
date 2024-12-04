import click, sys, csv, pytest
from flask import Flask
from App.models import *
from App.controllers import *
from datetime import datetime
from App.main import create_app, parse_users, parse_courses, parse_assessments, parse_programmes, parse_semesters
from App.database import db, create_db, get_migrate
from flask.cli import with_appcontext, AppGroup
from App.models import *
from App.controllers import *

# This commands file allow you to create convenient CLI commands for testing controllers!!
app = create_app()
migrate = get_migrate(app)

# This Command Creates And Initializes The Database
@app.cli.command("init", help="Creates And Initializes The Database")
def init():
    initialize()
    print('Database Initialized!')

"""
CSV Commands 
Written by Jalene Armstrong (Jalene A) - Task 07.4. CLI Commands Polishing
"""

csv_cli = AppGroup('csv', help='Commands To Easily Populate Models With Data')

@csv_cli.command('users', help="Populate The User Model With Data")
def user_csv():
    result = parse_users()
    print(result)

@csv_cli.command('courses', help="Populate The Course Model With Data")
def course_csv():
    result = parse_courses()
    print(result)

@csv_cli.command('assessments', help="Populate The Assessment Model With Data")
def assessment_csv():
    result = parse_assessments()
    print(result)

@csv_cli.command('programmes', help="Populate The Programme Model With Data")
def programme_csv():
    result = parse_programmes()
    print(result)

@csv_cli.command('semesters', help="Populate The Semester Model With Data")
def semester_csv():
    result = parse_semesters()
    print(result)

app.cli.add_command(csv_cli)

'''
|   Staff Group Commands
|   Written by RynniaRyan (Rynnia.R) - Task 07.1.1. Staff Group Commands Implementation
'''
staff_cli = AppGroup('staff', help='Staff object commands')

# COMMAND #1 - CREATE STAFF [Written by JaleneA]
@staff_cli.command('create', help="Registers A Staff Account To The System")
@click.option("--firstname", "-f", prompt="Enter Staff First Name", required=True, help="Staff First Name")
@click.option("--lastname", "-l", prompt="Enter Staff Last Name", required=True, help="Staff Last Name")
@click.option("--email", "-e", prompt="Enter Staff Email", required=True, help="Staff Email Address")
@click.option("--password", "-p", prompt="Enter Staff Default Password", hide_input=True, confirmation_prompt=True, help="Staff Password")
def register_staff_command(firstname, lastname, email, password):
    existing_staff = Staff.query.filter_by(email=email).first()
    if existing_staff:
        print(f"ERROR: A Staff Account With Email '{email}' Already Exists.")
        return

    new_staff = register_staff(firstname, lastname, email, password)
    if new_staff:
        print(f"SUCCESS: Staff '{firstname} {lastname}' Registered Successfully!")
    else:
        print(f"ERROR: Failed To Register Staff '{firstname} {lastname}'.")

# COMMAND #2 - UPDATE STAFF
@staff_cli.command('update', help='Update a staff member')
@click.option('--staffemail', prompt='Enter Staff Email to Edit', required=True)
def update_staff_profile(staffemail):
    staff_member = Staff.query.filter_by(email=staffemail).first()
    if not staff_member:
        print("\nStaff member not found!\n")
        return

    firstname = input('\nEdit First Name (press Enter to keep the current value): ') or None
    lastname = input('Edit Last Name (press Enter to keep the current value): ') or None
    email = input('Edit Email (press Enter to keep the current value): ') or None
    password = input('Edit password (press Enter to keep the current value): ') or None

    updatedStaff = update_staff(staffemail, firstName=firstname, lastName=lastname, password=password, email=email)

    if updatedStaff:
        print(f"\nStaff Member '{updatedStaff.firstName} {updatedStaff.lastName}' Updated! \n")
    else:
        print(updatedStaff['error'])

# COMMAND #3 - DELETE STAFF
@staff_cli.command('delete', help='Delete a staff member')
@click.option('--staffemail', prompt='Enter Staff email', required=True)
def delete_staff_profile(staffemail):
    result = delete_staff(staffemail)
    print("\n" + result)

# COMMAND #4 - LIST ALL STAFF
@staff_cli.command('list-all', help='List all staff members')
def list_staff():
    staffMembers = get_all_staff()
    if staffMembers:
        for staff in staffMembers:
            print(staff)
    else:
        print("No Staff Members Found")

# COMMAND #5 - SEARCH STAFF PROFILE
@staff_cli.command('search', help='Search for a staff member')
@click.option('--staffemail', prompt='Enter Staff Email', required=True)
def search_staff_profile(staffemail):
    staff = get_staff_by_email(staffemail)
    if staff:
        print(f"{staff}")
    else:
        print("\nStaff member not found!\n")

# COMMAND #6 - ASSIGN STAFF TO A COURSE
@staff_cli.command('add-course', help='Assign a staff member to a course')
@click.option('--staffemail', prompt='Enter Staff Email', required=True)
@click.option('--coursecode', prompt='Enter Course Code', required=True)
@click.option('--semestername', prompt='Enter Semester Name', required=True)
@click.option('--academicyear', prompt='Enter Academic Year', required=True)
def assign_staff_to_course(staffemail, coursecode, semestername, academicyear):
    staff = get_staff_by_email(staffemail)

    if staff:
        result = add_course_staff(coursecode, semestername, academicyear, staff.staffID)
        print(f"{result}")
    else:
        print("Staff not found")

# COMMAND #7 - REMOVE STAFF FROM A COURSE
@staff_cli.command('remove-course', help='Remove a staff member from a course')
@click.option('--staffemail', prompt='Enter Staff Email', required=True)
@click.option('--coursecode', prompt='Enter Course Code', required=True)
@click.option('--semestername', prompt='Enter Semester Name', required=True)
@click.option('--academicyear', prompt='Enter Academic Year', required=True)
def remove_staff_from_course(staffemail, coursecode, semestername, academicyear):
    staff = get_staff_by_email(staffemail)

    if staff:
        result = remove_course_staff(coursecode, semestername, academicyear, staff.staffID)
        print(f"{result}")
    else:
        print("Staff not found")

# COMMAND #8 - VIEW STAFF ASSIGNED COURSE/S
@staff_cli.command('list-courses', help='View staff with their assigned course/s')
@click.option('--staffemail', prompt='Enter Staff Email', required=True)
def view_staff_courses(staffemail):
    staff = get_staff_by_email(staffemail)

    if staff:
        result = get_staff_courses(staffemail)

        if result:
            print(f"{result}")
        else:
           print(f"\nThere are Currently No Courses Found For '{staff.firstName} {staff.lastName}'\n")
    else:
        print("Staff not found")

app.cli.add_command(staff_cli)


'''
|   Course Group Commands
|   Written by RynniaRyan (Rynnia.R) - Task 07.1.2. Course Group Commands Implementation
'''
course_cli = AppGroup('course', help='Course object commands')

# Command #1 : CREATE COURSE
@course_cli.command('create', help='Create A Course')
@click.option('--coursecode', '-c', prompt='Enter Course Code', required=True)
@click.option('--coursetitle', '-t', prompt='Enter Course Title', required=True)
@click.option('--coursecredits', '-r', prompt='Enter Course Credits', required=True)
@click.option('--coursedescription', '-d', prompt='Enter Course Description', required=True)
@click.option('--courselevel', '-l', prompt='Enter Course Level', required=True)
def create_course(coursecode, coursetitle, coursecredits, coursedescription, courselevel):
    result = add_course(coursecode, coursetitle, coursecredits, coursedescription, courselevel)
    if result:
        print(f"{result}")
    else:
        print(f"\nError: An error occurred while adding course {coursecode}\n")

# COMMAND #2 : UPDATE COURSE
@course_cli.command('update', help='Edit A Course')
@click.option('--coursecode', '-c', prompt='Enter Course Code To Edit', required=True)
def update_course(coursecode):
    response = get_course_by_code(coursecode)

    if 'Error' in response:
        print(f"{response}")
        return
    else:
        print(f"\nEnter New Course Details For {coursecode}. . .")

        coursetitle = input('\nEdit Course Title (press Enter to keep the current value): ') or None
        coursecredits = input('Edit Course Credits (press Enter to keep the current value): ') or None
        coursedescription = input('Edit Course Description (press Enter to keep the current value): ') or None
        courselevel = input('Edit Course Level (press Enter to keep the current value): ') or None

        result = edit_course(coursecode, coursetitle, coursecredits, coursedescription, courselevel)

        if result:
            print(f"{result}")
        else:
            print(f"\nError: An error occurred while updating course {coursecode}\n")

# COMMAND #3 : SEARCH COURSE
@course_cli.command('search', help='Search For A Course')
@click.option('--coursecode', '-c', prompt='Enter Course Code', required=True)
def search_course(coursecode):
    course= get_course_by_code(coursecode)

    if course:
        print(f"{course}")
    else:
        print("\nError: An error occurred while searching for the course\n")

# COMMAND #4 : VIEW ALL COURSES
@course_cli.command('list-all', help='View All Courses')
def get_all_courses():
    courses = list_courses()

    if courses:
        print(f"{courses}")
    else:
        print("\nError: An error occurred while obtaining all courses\n")

# COMMAND #5 : ADD ASSESSMENT TO A COURSE
@course_cli.command('add-assessment', help='Add Assessment To A Course')
@click.option('--coursecode', '-c', prompt='Enter Course Code', required=True)
@click.option('--year', '-y', prompt="Enter Year", type=int, help="Year For The Calendar", required=True)
@click.option('--month', '-m', prompt="Enter Month", type=int, help="Month For The Calendar", required=True)
def add_assessment_to_course(coursecode, year, month):

    # STEP 1: Generate & Display The Schedule Calendar With Any Unavailable Dates Marked | service/assessment.py
    print(f"\n{'Assessment Calendar':^50}")
    print(f"{'-'*50}")
    calendar_table = generate_calendar(year, month, coursecode)
    print(calendar_table)

    # STEP 2: Prompt For Scheduling Details
    assessmentcode = click.prompt("\nEnter Assessment ID:")
    start_day = click.prompt("Enter Start Day", type=int)
    start_time = click.prompt("Enter Start Time (HH:MM)", type=click.DateTime(formats=["%H:%M"]))

    start_date = datetime(year, month, start_day).date()

    end_day = click.prompt("Enter End Day", type=int)
    end_time = click.prompt("Enter End Time (HH:MM)", type=click.DateTime(formats=["%H:%M"]))

    end_date = datetime(year, month, end_day).date()

    print("\nAvailable Clash Rules:")
    for idx, rule in enumerate(ClashRules):
        print(f"{idx + 1}. {rule.name} - {rule.value}")

   # STEP 3: Prompt For Clash Rule To Apply
    while True:
        try:
            clash_rule_input = click.prompt("\nSelect A Clash Rule (Enter Number)", type=int)
            if 1 <= clash_rule_input <= len(ClashRules):
                selected_rule_name = list(ClashRules)[clash_rule_input - 1].name
                selected_rule = selected_rule_name
                break
            else:
                print("Invalid Selection! You Must Choose A Valid ClashRule From The List.")
        except ValueError:
            print("Invalid Input! Please Enter A Number Corresponding To A ClashRule.")

    # After The User Listened To Instructions
    result = add_course_assessment(coursecode, assessmentcode, start_date, start_time, end_date, end_time, selected_rule)
    if result.get("status") != "error":
        success_message = result["Message"]
        course_assessment_data = result["CourseAssessment"]

        print(f"\n{'='*50}")
        print(f"Success: {success_message}")
        print(f"\n{'Assessment Details':^50}")
        print(f"{'-'*50}")
        
        for key, value in course_assessment_data.items():
            print(f"{key}: {value}")
        
        print(f"\n{'='*50}")
    elif result.get("status") == "error":
        error_message = result["message"]
        print(f"{error_message}")
    else:
        print(f"Error: An Unexpected Error Occurred While Assigning Assessment To {coursecode}")

# COMMAND #6 : REMOVE ASSESSMENT FROM A COURSE
@course_cli.command('remove-assessment', help='Remove Assessment From A Course')
@click.option('--coursecode', '-c', prompt='Enter Course Code', required=True)
@click.option('--courseassessmentcode', '-c', prompt='Enter Course Assessment Code', required=True)
def remove_assessment_from_course(coursecode,courseassessmentcode):
    result = delete_course_assessment(courseassessmentcode)

    if result:
        print(f"{result}")
    else:
        print(f"\nError: An error occurred while removing assessment from {coursecode}\n")

# COMMAND #7 : VIEW ALL ASSESSMENTS FOR A COURSE
@course_cli.command('list-assessments', help='View All Assessments For A Course')
@click.option('--coursecode', '-c', prompt='Enter Course Code', required=True)
def get_all_assessments_for_course(coursecode):
    assessments = list_course_assessments(coursecode)

    if assessments:
        print(f"\n{assessments}\n")
    else:
        print("\nError: An error occurred while obtaining all assessments for the course\n")

app.cli.add_command(course_cli)


"""
Assessment Commands 
Written by Jalene Armstrong (Jalene A) - Task 07.1.3. Assessment Group Commands Implementation
"""

assessment_cli = AppGroup('assessment', help='Assessment Object Commands')

# COMMAND #1 : CREATE ASSESSMENT
@assessment_cli.command('create', help="Creates A New Assessment For A Particular Course")
@click.option('--assessment_title', '-at', prompt="Enter Assessment Title", help="Title Of Assessment")
def create_assessment_command(assessment_title):

    print("\nSelect Assessment Type:")
    for idx, assessment_enum in enumerate(AssessmentTypes):
        print(f"{idx + 1}. {assessment_enum.name} - {assessment_enum.value}")

    while True:
        try:
            assessment_type_input = click.prompt("\nSelect Assessment Type (Enter Number)", type=int)
            if 1 <= assessment_type_input <= len(AssessmentTypes):
                selected_assessment_type = list(AssessmentTypes)[assessment_type_input - 1].name
                selected_type = selected_assessment_type
                break
            else:
                print("Invalid Selection! You Must Choose A Valid Assessment Type From The List.")
        except ValueError:
            print("Invalid Input! Please Enter A Number Corresponding To An Assessment Type.")

    new_assessment = create_assessment(assessmentTitle=assessment_title, assessmentType=selected_type)

    if new_assessment and "Message" in new_assessment and new_assessment["Message"] == "Assessment Created Successfully":
            print(f"\nSUCCESS: New Assessment '{assessment_title}' - Type: {selected_type} Added Successfully!.")
    elif new_assessment and "Error Message" in new_assessment:
        print(f"ERROR: {new_assessment['Error Message']}")
    else:
        print("ERROR: Something Went Wrong. Please Try Again.")

# COMMAND #2 : SEARCH ASSESSMENT
@assessment_cli.command('search', help="Search For An Assessment")
@click.option('--assessment_id', '-a', prompt="Enter The Assessment ID", help="ID Number Of Assessment")
def fetch_assessment_command(assessment_id):
    fetched_assessment = get_assessment_by_id(assessmentID=assessment_id)

    if fetched_assessment:
        print(f"Assessment Details:\n{fetched_assessment}")
    else:
        print(f"ERROR: Assessment With ID: {assessment_id} Not Found.")

# COMMAND #2.5 : SEARCH ALL ASSESSMENTS BASED ON TYPE
@assessment_cli.command('search-type', help="Retrieve And Displays All Assessments Based On Type")
@click.option('--assessment_type', '-aty', prompt="Enter Assessment Type", help="Type Of Assessment")
def fetch_assessment_by_type_command(assessment_type):
    print(get_assessments_by_type(assessment_type))

# COMMAND #3 : LIST ALL ASSESSMENTS
@assessment_cli.command('list-all', help="Retrieves And List All Assessments In The Database")
@click.option('--format', '-f', prompt="Enter Desired Output Format : String or JSON", help="Output Format Of Choice : String Or JSON")
def list_all_assessments_command(format):
    if format.lower() == 'string':
        print(list_assessments())
    else:
        print(list_assessments_json())

# # COMMAND #4 : UPDATE ASSESSMENT
@assessment_cli.command('update', help="Updates An Assessment")
@click.option('--assessment_id', '-at', prompt="Enter Assessment ID", help="ID Number Of Assesment")
@click.option('--new_assessment_title', '-atnew', default=None, help="New Assessment Title (Optional)")
@click.option('--new_assessment_type', '-atypenew', default=None, help="New Assessment Type (Optional)")
def update_assessment_command(assessment_id, new_assessment_title, new_assessment_type):
    assessment_to_update = get_assessment_by_id(assessmentID=assessment_id)

    if not assessment_to_update:
        print(f"ERROR: Assessment With ID: {assessment_id} Does Not Exist.")
        return

    if not new_assessment_title:
            new_assessment_title = input(
                f"Enter New Assessment Title (Current: {assessment_to_update.assessmentTitle} | Press ENTER to skip): "
            ) or assessment_to_update.assessmentTitle

    print(f"\nCurrent Assessment Type: {assessment_to_update.assessmentType.name}")

    print("\nSelect New Assessment Type:")
    for idx, assessment_enum in enumerate(AssessmentTypes):
        print(f"{idx + 1}. {assessment_enum.name} - {assessment_enum.value}")

    if not new_assessment_type:
        while True:
            new_assessment_type_input = input("\nSelect New Assessment Type (Enter Number Or Press ENTER To Skip): ")
            if not new_assessment_type_input:
                new_assessment_type = assessment_to_update.assessmentType
                break
            try:
                new_assessment_type_index = int(new_assessment_type_input)
                if 1 <= new_assessment_type_input <= len(AssessmentTypes):
                    new_assessment_type = list(AssessmentTypes)[new_assessment_type_index - 1].name
                    break
                else:
                    print("Invalid Selection! You Must Choose A Valid Assessment Type From The List.")
            except ValueError:
                print("Invalid Input! Please Enter A Number Corresponding To An Assessment Type.")

    if new_assessment_title == assessment_to_update.assessmentTitle and new_assessment_type == assessment_to_update.assessmentType:
        print(f"No Changes Made To Assessment With ID: '{assessment_to_update.assessmentID}'")
        return

    updated_assessment = update_assessment(
        assessmentID=assessment_id,
        new_title=new_assessment_title,
        new_type=new_assessment_type
    )

    if updated_assessment is None:
        print("ERROR: Failed To Update The Assessment.")
    elif "Error Message" in updated_assessment:
        print(f"ERROR: {updated_assessment['Error Message']}")
    else:
        print(f"SUCCESS: Assessment Updated Successfully!\nUpdated Details: {updated_assessment['Assessment']}")

app.cli.add_command(assessment_cli)


"""
Programme Commands 
Written by Jalene Armstrong (Jalene A) - Task 07.2.1. Programme Group Commands Implementation
"""
programme_cli = AppGroup('programme', help='Programme Object Commands')

# COMMAND #1 : CREATE PROGRAMME
@programme_cli.command('create', help="Creates & Adds A New Programme To The Database")
@click.option('--programme_title', '-pt', prompt="Enter Programme Title", help="Title Of Programme")
@click.option('--programme_desc', '-pd', prompt="Enter Programme Description", help="Description Of The Programme")
def create_programme_command(programme_title, programme_desc):
    new_programme = create_programme(programme_title, programme_desc)

    if new_programme and "Message" in new_programme and new_programme["Message"] == "Programme Created Successfully":
            print(f"SUCCESS: New Programme '{programme_title}' Added Successfully!.")
    elif new_programme and "Error Message" in new_programme:
        print(f"ERROR: {new_programme['Error Message']}")
    else:
        print("ERROR: Something Went Wrong. Please Try Again.")

# COMMAND #2 : ADD A COURSE TO A PROGRAMME
@programme_cli.command('add-course', help='Add Course To Programme')
@click.option('--programme_title', '-pt', prompt='Enter Programme Title', required=True)
@click.option('--course_code', '-c', prompt='Enter Course Code', required=True)
def add_course_to_programme_command(programme_title, course_code):
    fetched_programme = get_programme_by_title(programmeTitle=programme_title)
    if not fetched_programme:
        print(f"ERROR: Programmme '{programme_title}' Does Not Exist.")
        return

    new_programme_course = add_course_to_programme(courseCode=course_code, programmeID=fetched_programme.programmeID)

    if new_programme_course is None:
        print(f"ERROR: Failed To Add Course: '{course_code}' To Programme: '{programme_title}'.")
    elif "Error" in new_programme_course:
        print(f"ERROR: {new_programme_course['Error']}")
    else:
        print(f"SUCCESS: Programme Updated Successfully!\nUpdated Details: {new_programme_course['CourseProgramme']}")

# COMMAND #3 : UPDATE PROGRAMME
@programme_cli.command('update', help="Updates Information For An Existing Programme")
@click.option('--programme_title', '-pt', prompt="Enter Programme Title", help="Title Of The Programme")
@click.option('--new_programme_title', '-ptnew', default=None, help="New Programme Title (Optional)")
@click.option('--new_programme_desc', '-pdnew', default=None, help="New Programme Description (Optional)")
def update_programme_command(programme_title, new_programme_title, new_programme_desc):
    programme_to_update = get_programme_by_title(programmeTitle=programme_title)

    if not programme_to_update:
        print(f"ERROR: Programmme '{programme_title}' Does Not Exist.")
        return

    new_programme_title = new_programme_title or input(f"Enter New Programme Name (Current: {programme_to_update.programmeTitle} | Press ENTER To Skip): ") or programme_to_update.programmeTitle
    new_programme_desc = new_programme_desc or input(f"Enter New Programme Description (Press ENTER To Skip): ") or programme_to_update.programmeDescription

    if new_programme_title == programme_to_update.programmeTitle and new_programme_desc == programme_to_update.programmeDescription:
        print(f"No Changes Made To Programme: '{new_programme_title}")
        return

    updated_programme = update_programme(
        programmeTitle=programme_title,
        new_title=new_programme_title,
        new_description=new_programme_desc
    )

    if updated_programme is None:
        print("ERROR: Failed To Update The Semester.")
    elif "Error Message" in updated_programme:
        print(f"ERROR: {updated_programme['Error Message']}")
    else:
        print(f"SUCCESS: Programme Updated Successfully!\nUpdated Details: {updated_programme['Programme']}")

# COMMAND #4 : LIST ALL PROGRAMMES
@programme_cli.command('list-all', help="Retrieve And Lists All Programmes In The Database")
@click.argument("format", default="json")
def list_programmes_command(format):
    if format == 'string':
        print(list_programmes())
    else:
        print(list_programmes_json())

# COMMAND #5 : LIST ALL COURSE WITHIN A PROGRAMME
@programme_cli.command('list-courses', help="List All Courses For A Specific Programme")
@click.option('--programme_id', '-pt', prompt="Enter Programme ID", help="ID Of The Programme")
def list_programme_courses_command(programme_id):
    print(list_programme_courses(programmeID=programme_id))

# COMMAND #6 : SEARCH PROGRAMME
@programme_cli.command('search', help="Search For A Programme")
@click.option('--programme_id', '-p', prompt="Enter The Programme ID", help="ID Number Of Programme")
def fetch_assessment_command(programme_id):
    fetched_programme = get_programme_by_id(programmeID=programme_id)

    if fetched_programme:
        print(f"Programme Details:\n{fetched_programme}")
    else:
        print(f"ERROR: Programme With ID: {programme_id} Not Found.")

# COMMAND #7 : REMOVE COURSE FROM A PROGRAMME
@programme_cli.command('remove-course', help='Remove Course From A Programme')
@click.option('--programme_id', '-p', prompt='Enter Programme ID', required=True)
@click.option('--course_code', '-c', prompt='Enter Course Code', required=True)
def remove_course_from_programme_command(programme_id, course_code):
    result = remove_course_from_programme(programmeID=programme_id, courseCode=course_code)
    if result:
        print(f"{result}")
    else:
        print(f"Error: An Error Occurred While Removing Course '{course_code}' From Programme\n")

app.cli.add_command(programme_cli)


"""
Semester Commands 
Written by Jalene Armstrong (Jalene A) - Task 07.2.2. Semester Group Commands Implementation
"""
semester_cli = AppGroup('semester', help='Semester Object Commands')

# COMMAND #1 : CREATE SEMESTER
@semester_cli.command('create', help="Creates Adds A New Semester")
@click.option('--semester_name', '-n', prompt="Enter Semester Name", help="Name Of The Semester")
@click.option('--academic_year', '-a', prompt="Enter Academic Year (YYYY/YYYY)", help="Academic Year Of The Semester")
@click.option('--start_date', '-s', prompt="Enter Start Date (YYYY-MM-DD)", type=click.DateTime(formats=["%Y-%m-%d"]), help="Start Date Of The Semester")
@click.option('--end_date', '-e', prompt="Enter End Date (YYYY-MM-DD)", type=click.DateTime(formats=["%Y-%m-%d"]), help="End Date Of The Semester")
def add_semester_command(semester_name, academic_year, start_date, end_date):
    start_date = start_date.date()
    end_date = end_date.date()

    new_semester = add_semester(semester_name, academic_year, start_date, end_date)

    if new_semester and "New Semester Added" in new_semester:
            print(f"SUCCESS: New semester '{semester_name}' Added For {academic_year}.")
    elif new_semester and "Error Message" in new_semester:
        print(f"ERROR: {new_semester['Error Message']}")
    else:
        print("ERROR: Something Went Wrong. Please Try Again.")

# COMMAND #2 : SEARCH SEMESTER
@semester_cli.command('search', help="Gets Details For A Specific Semester")
@click.option('--semester_id', '-n', prompt="Enter Semester ID", help="ID Of The Semester")
def fetch_semester_command(semester_id):
    fetched_semester = get_semester_by_id(semesterID=semester_id)

    if isinstance(fetched_semester, dict) and "Error Message" in fetched_semester:
        print(f"ERROR: {fetched_semester['Error Message']}")
    elif isinstance(fetched_semester, Semester):
        print(f"Semester Details: {fetched_semester}")
    else:
        print("ERROR: Failed To Fetch Requested Semester.")

# COMMAND #3 : UPDATE SEMESTER
@semester_cli.command('update', help="Updates Information For An Existing Semester")
@click.option('--semester_id', '-s', prompt="Enter Semester ID", help="ID Of The Semester")
@click.option('--new_semester_name', '-snew', default=None, help="New Semester Name (Optional)")
@click.option('--new_academic_year', '-anew', default=None, help="New Academic Year (Optional)")
@click.option('--start_date', '-st', default=None, type=click.DateTime(formats=["%Y-%m-%d"]), help="New Start Date (Optional)")
@click.option('--end_date', '-e', default=None, type=click.DateTime(formats=["%Y-%m-%d"]), help="New End Date (Optional)")
def update_semester_command(semester_id, new_semester_name, new_academic_year, start_date, end_date):
    semester_to_update = get_semester_by_id(semesterID=semester_id)

    if not semester_to_update:
        print(f"ERROR: Semester With ID: {semester_id} Not Found.")
        return

    new_semester_name = new_semester_name or input(f"Enter New Semester Name (Current: {semester_to_update.semesterName} | Press ENTER To Skip): ") or semester_to_update.semesterName
    new_academic_year = new_academic_year or input(f"Enter New Academic Year (Current: {semester_to_update.academicYear} | Press ENTER To Skip): ") or semester_to_update.academicYear
    start_date = start_date or (input(f"Enter New Start Date (Current: {semester_to_update.startDate} | Press ENTER To Skip): ") or semester_to_update.startDate)
    end_date = end_date or (input(f"Enter New End Date (Current: {semester_to_update.endDate} | Press ENTER To Skip): ") or semester_to_update.endDate)

    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    if isinstance(end_date, str):
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

    updated_semester = update_semester(
        new_semesterName=new_semester_name,
        new_academicYear=new_academic_year,
        startDate=start_date,
        endDate=end_date
    )

    if updated_semester is None:
        print("ERROR: Failed To Update The Semester.")
    elif "Error Message" in updated_semester:
        print(f"ERROR: {updated_semester['Error Message']}")
    else:
        print(f"SUCCESS: Semester Updated Successfully!\nUpdated Details: {updated_semester['Semester Updated']}")

# COMMAND #4 : LIST ALL SEMESTERS
@semester_cli.command('list-all', help="Retrieve And Lists All Semesters In The Database")
@click.argument("format", default="json")
def list_semesters_command(format):
    if format == 'string':
        print(list_semesters())
    else:
        print(list_semesters_json())

# COMMAND #4.5 : LIST ALL SEMESTERS BASED ON ACADEMIC YEAR
@semester_cli.command('list-year', help="Retrieve And Lists All Semesters In The Database Based On Academic Year")
@click.option('--academic_year', '-a', prompt="Enter Academic Year (YYYY/YYYY)", help="Academic Year Of The Semester")
def list_year_semesters_command(academic_year):
    print(get_semesters_by_academic_year(academic_year))

# COMMAND #5 : LIST ALL COURSES IN A SEMESTER
@semester_cli.command('list-courses', help="List All Courses For A Specific Semester")
@click.option('--semester_id', '-s', prompt="Enter Semester ID", help="ID Of The Semester")
def list_semester_courses_command(semester_id):
    print(list_courses_for_semester(semesterID=semester_id))

# COMMAND #6 : ADD COURSE OFFERING TO SEMESTER
@semester_cli.command('add-offering', help='Add Course To A Semester')
@click.option('--semester_id', '-s', prompt='Enter Semester ID', required=True)
@click.option('--course_code', '-c', prompt='Enter Course Code', required=True)
def add_course_offering_command(semester_id, course_code):
    fetched_semester = get_semester_by_id(semesterID=semester_id)

    if not fetched_semester:
        print(f"ERROR: Semester With ID: '{semester_id}' Does Not Exist.")
        return

    new_course_offering = add_course_offering(semesterID=semester_id, courseCode=course_code)

    if new_course_offering is None:
        print(f"ERROR: Failed To Add Course: '{course_code}' To Semester.")
    elif "Error" in new_course_offering:
        print(f"ERROR: {new_course_offering['Error']}")
    else:
        print(f"SUCCESS: Semester Course Offering Added Successfully!\nNew CourseOffering Details: {new_course_offering['CourseOffering']}")

# COMMAND #6.5 : UPDATE COURSE OFFERING
@semester_cli.command('update-offering', help='Update A CourseOffering In A Semester')
@click.option('--semester_id', '-s', prompt='Enter Semester ID', required=True)
@click.option('--course_code', '-c', prompt='Enter Course Code', required=True)
@click.option('--students_enrolled', '-s', prompt='Enter Students Enrolled', required=True)
def update_course_offering_command(semester_id, course_code, students_enrolled):
    fetched_semester = get_semester_by_id(semesterID=semester_id)

    if not fetched_semester:
        print(f"ERROR: Semester With ID: '{semester_id}' Does Not Exist.")
        return

    updated_course_offering = update_course_offering(courseCode=course_code, semesterID=semester_id, totalStudentsEnrolled=students_enrolled)

    if updated_course_offering is None:
        print(f"ERROR: Failed To Update Course: '{course_code}' Offering With The Semester.")
    elif "Error" in updated_course_offering:
        print(f"ERROR: {updated_course_offering['Error']}")
    else:
        if 'CourseOffering' in updated_course_offering:
            print(f"SUCCESS: Semester Course Offering Updated Successfully!\nUpdated Details: {updated_course_offering['CourseOffering']}")
        else:
            print(f"ERROR: Unexpected result. 'CourseOffering' not found in the response.")

# COMMAND #7 REMOVE COURSE OFFERING FROM SEMESTER
@semester_cli.command('remove-offering', help='Remove CourseOffering From A Semester')
@click.option('--semester_id', '-s', prompt='Enter Semester ID', required=True)
@click.option('--course_code', '-c', prompt='Enter Course Code', required=True)
def remove_course_offering_command(semester_id, course_code):
    fetched_semester = get_semester_by_id(semesterID=semester_id)

    if not fetched_semester:
        print(f"ERROR: Semester With ID: '{semester_id}' Does Not Exist.")
        return

    result = remove_course_offering(courseCode=course_code, semesterID=semester_id)

    if "Error" in result:
        print(f"ERROR: {result['Error']}")
    else:
        print(f"SUCCESS: {result['Message']}")

app.cli.add_command(semester_cli)

"""
Admin Commands 
Written by Jalene Armstrong (Jalene A) - Task 07.2.3. Admin Group Commands Implementation
"""

admin_cli = AppGroup('admin', help='Admin Object Commands')

# COMMAND #1 : CREATE ADMIN
@admin_cli.command('create', help="Creates An Admin Account")
@click.option("--firstname", "-f", prompt="Enter Admin First Name", required=True, help="Admin First Name")
@click.option("--lastname", "-l", prompt="Enter Admin Last Name", required=True, help="Admin Last Name")
@click.option("--email", "-e", prompt="Enter Admin Email", required=True, help="Admin Email Address")
@click.option("--password", "-p", prompt="Enter Admin Password", hide_input=True, confirmation_prompt=True, help="Admin Password")
def create_admin_command(firstname, lastname, email, password):
    existing_admin = Admin.query.filter_by(email=email).first()
    if existing_admin:
        print(f"ERROR: An Admin Account With Email - '{email}' Already Exists.")
        return

    new_admin = create_admin(firstname, lastname, password, email)
    if new_admin:
        print(f"SUCCESS: Admin - '{firstname} {lastname}' Created Successfully!")
    else:
        print(f"ERROR: Failed To Create Admin '{firstname} {lastname}'.")

# COMMAND #2 : DELETE ADMIN
@admin_cli.command('delete', help="Deletes An Admin Account")
@click.option("--email", "-e", prompt="Enter Email Of Admin To Delete", required=True, help="Admin Email Address")
def delete_admin_command(email):
    admin = get_admin_by_email(email)
    if not admin:
        print(f"ERROR: Admin With Email '{email}' Not Found.")
        return

    print(f"Deleting Admin: {admin}")
    result = delete_admin(email)
    if isinstance(result, dict) and "error" in result:
        print(f"ERROR: {result['error']}")
    elif result:
        print(f"SUCCESS: Admin with Email '{email}' Deleted Successfully!")
    else:
        print(f"ERROR: Failed To delete Admin With Email '{email}'.")

# COMMAND #3 : UPDATE ADMIN
@admin_cli.command('update', help="Updates An Existing Admin Account")
@click.option('--current_email', '-c', prompt="Enter Email Of Admin To Edit", help="Enter Current Admin Email", required=True)
@click.option('--firstname', '-f', default=None, help="Enter New First Name (Optional)")
@click.option('--lastname', '-l', default=None, help="Enter New Last Name (Optional)")
@click.option('--password', '-p', default=None, help="Enter New Password (Optional)")
@click.option('--email', '-e', default=None, help="Enter New Email (Optional)")
def update_admin_command(current_email, firstname, lastname, password, email):

    admin_to_update = get_admin_by_email(current_email)
    if not admin_to_update:
        print(f"ERROR: Admin With Email '{current_email}' Not Found.")
        return

    if not firstname:
        firstname = input(f"Enter New First Name (Current: {admin_to_update.firstName} |Press ENTER To Skip): ") or admin_to_update.firstName
    if not lastname:
        lastname = input(f"Enter New Last Name (Current: {admin_to_update.lastName} | Press ENTER To Skip): ") or admin_to_update.lastName
    if not password:
        password = input("Enter New Password (Press ENTER To Skip):" ) or admin_to_update.password
    if not email:
        email = input(f"Enter New Email (Current: {admin_to_update.email} | Press ENTER To Skip): ") or admin_to_update.email

    if email != admin_to_update.email:
        existing_admin = Admin.query.filter_by(email=email).first()
        if existing_admin:
            print(f"ERROR: The Email '{email}' Is Already In Use By Another Admin.")
            return

    updated_admin = update_admin(current_email, firstname, lastname, password, email)

    if isinstance(updated_admin, dict) and 'error' in updated_admin:
        print(f"ERROR: {updated_admin['error']}")
    elif updated_admin:
        print(f"SUCCESS: Admin '{current_email}' Updated Successfully!")
        print(updated_admin)
    else:
        print("ERROR: Failed To Update Admin. Ensure The Current Email Exists And New Email Isn't Already In Use.")

# COMMAND #4 - SEARCH STAFF PROFILE
@admin_cli.command('search', help='Search For An Admin')
@click.option('--admin_email', prompt='Enter Admin Email', required=True)
def search_admin_command(admin_email):
    admin = get_admin_by_email(adminEmail=admin_email)
    if admin:
        print(f"{admin}")
    else:
        print("Admin Not Found Or User is Not An Admin.")

# COMMAND #5 : LIST ALL ADMIN
@admin_cli.command('list-all', help="Retrieve And Lists All Admins In The Database")
def list_admins_command():
    adminMembers = get_all_admin_users()
    if adminMembers:
        for admin in adminMembers:
            print(admin)
    else:
        print("No Admin Members Found")

app.cli.add_command(admin_cli)

'''
Test Commands
Written by Daniel Young (DaNJO-Y) - Integration (Task 08.2.1 - Task 08.2.5)
Modified by Jalene Armstrong (JaleneA) - Unit & App (Task 09.1. Post-CLI and Post-Tests Cleanup)
'''

test = AppGroup('test', help='Testing Commands')

@test.command("user", help="Run User Tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    elif type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTest"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

@test.command("staff", help="Run Staff Tests")
@click.argument("type", default="all")
def staff_tests_command(type):
    if type == "int":
        sys.exit(pytest.main(["-k", "StaffIntegrationTests"]))
    elif type == "unit":
        sys.exit(pytest.main(["-k", "StaffUnitTest"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

@test.command("admin", help="Run Admin Tests")
@click.argument("type", default="all")
def admin_tests_command(type):
    if type == "int":
        sys.exit(pytest.main(["-k", "AdminIntegrationTests"]))
    elif type == "unit":
        sys.exit(pytest.main(["-k", "AdminUnitTest"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

@test.command("course", help="Run Course Tests")
@click.argument("type", default="all")
def course_tests_command(type):
    if type == "int":
        sys.exit(pytest.main(["-k", "CourseIntegrationTests"]))
    elif type == "unit":
        sys.exit(pytest.main(["-k", "CourseUnitTest"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

@test.command("semester", help="Run Semester Tests")
@click.argument("type", default="all")
def semester_tests_command(type):
    if type == "int":
        sys.exit(pytest.main(["-k", "SemesterIntegrationTests"]))
    elif type == "unit":
        sys.exit(pytest.main(["-k", "SemesterUnitTest"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

# Unit Tests Only
@test.command("programme", help="Run Programme Tests")
@click.argument("type", default="all")
def programme_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "ProgrammeUnitTest"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

@test.command("assessment", help="Run Assessment Tests")
@click.argument("type", default="all")
def assessment_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "AssessmentUnitTest"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

app.cli.add_command(test)