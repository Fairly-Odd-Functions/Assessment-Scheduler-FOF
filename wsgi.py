import click, sys, csv, pytest
from flask import Flask
from App.models import *
from App.controllers import *
from datetime import datetime
from App.main import create_app
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

'''
|   Staff Group Commands
|   Written by RynniaRyan (Rynnia.R) - Task 07.1.1. Staff Group Commands Implementation
'''
staff_cli = AppGroup('staff', help='Staff object commands')

# COMMAND #1 - ADD STAFF
@staff_cli.command('add', help='Add a new staff member')
@click.option('--firstname', prompt='Enter First Name', required=True)
@click.option('--lastname', prompt='Enter Last Name', required=True)
@click.option('--email', prompt='Enter Email', required=True)
@click.option('--password', prompt='Enter Password', required=True)
def add_staff(firstname, lastname, email, password):
    newStaff = register_staff(firstname, lastname, password, email)

    if newStaff:
        print(f"\nNew Staff Member '{newStaff.firstName} {newStaff.lastName}' Added! \n")
    else:
        print("\nError: Email or password already in use!\n")

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
@staff_cli.command('list', help='List all staff members')
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
@staff_cli.command('get-courses', help='View staff with their assigned course/s')
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

# Command #1 : CREATE A COURSE
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

# COMMAND #2 : EDIT A COURSE
@course_cli.command('edit', help='Edit A Course')
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

# COMMAND #3 : SEARCH FOR A COURSE
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
@click.option('--assessmentcode', '-a', prompt='Enter Assessment Code', required=True)

# Start Date
@click.option('--start_date', '-sd', prompt="Enter Start Date (YYYY-MM-DD)", 
              type=click.DateTime(formats=["%Y-%m-%d"]), help="Start Date Of The Assessment")
# Start Time
@click.option('--start_time', '-st', prompt="Enter Start Time (HH:MM:SS)", 
              type=click.DateTime(formats=["%H:%M:%S"]), help="Start Time Of The Assessment")
# End Date
@click.option('--end_date', '-ed', prompt="Enter End Date (YYYY-MM-DD)", 
              type=click.DateTime(formats=["%Y-%m-%d"]), help="End Date Of The Assessment")
# End Time
@click.option('--end_time', '-et', prompt="Enter End Time (HH:MM:SS)", 
              type=click.DateTime(formats=["%H:%M:%S"]), help="End Time Of The Assessment")
def add_assessment_to_course(coursecode, assessmentcode, start_date, start_time, end_date, end_time):
    result = add_course_assessment(coursecode, assessmentcode, start_date, start_time, end_date, end_time)

    if result:
        print(f"{result}")
    else:
        print(f"\nError: An error occurred while assigning assessment to {coursecode}\n")

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

@assessment_cli.command('create_assessment', help="Creates A New Assessment For A Particular Course")
@click.option('--assessment_title', '-at', prompt="Enter Assessment Title", help="Title Of Assessment")
@click.option('--assessment_type', '-aty', prompt="Enter Assessment Type", help="Type Of Assessment")
def create_assessment_command(assessment_title, assessment_type):
    new_assessment = create_assessment(assessment_title, assessment_type)

    if new_assessment and "Message" in new_assessment and new_assessment["Message"] == "Assessment Created Successfully":
            print(f"SUCCESS: New Assessment '{assessment_title}' Added Successfully!.")
    elif new_assessment and "Error Message" in new_assessment:
        print(f"ERROR: {new_assessment['Error Message']}")
    else:
        print("ERROR: Something Went Wrong. Please Try Again.")

@assessment_cli.command('by_title', help="Retrieve And Displays All Assessments Based On Title")
@click.option('--assessment_title', '-at', prompt="Enter Assessment Title", help="Title Of Assessment")
def fetch_assessment_by_title_command(assessment_title):
    print(get_assessments_by_title(assessment_title))

@assessment_cli.command('by_type', help="Retrieve And Displays All Assessments Based On Type")
@click.option('--assessment_type', '-aty', prompt="Enter Assessment Type", help="Type Of Assessment")
def fetch_assessment_by_type_command(assessment_type):
    print(get_assessments_by_type(assessment_type))

@assessment_cli.command('list_all', help="Retrieves And List All Assessments In The Database")
@click.option('--format', '-f', prompt="Enter Desired Output Format : String or JSON", help="Output Format Of Choice : String Or JSON")
def list_all_assessments_command(format):
    if format.lower() == 'string':
        print(list_assessments())
    else:
        print(list_assessments_json())

app.cli.add_command(assessment_cli)


"""
Programme Commands 
Written by Jalene Armstrong (Jalene A) - Task 07.2.1. Programme Group Commands Implementation
"""
programme_cli = AppGroup('programme', help='Programme Object Commands')

@programme_cli.command('create_programme', help="Creates & Adds A New Programme To The Database")
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

@programme_cli.command('add_course', help='Add Course To Programme')
@click.option('--programme_title', '-pt', prompt='Enter Programme Title', required=True)
@click.option('--course_code', '-c', prompt='Enter Course Code', required=True)
def add_course_to_programme_command(programme_title, course_code):
    fetched_programme = get_programme_by_title(programmeTitle=programme_title)
    if not fetched_programme:
        print(f"ERROR: Programmme '{programme_title}' Does Not Exist.")
        return

    new_programme_course = add_course_to_programme(courseCode=course_code, programmeID=fetched_programme.get('programmeID'))

    if new_programme_course is None:
        print(f"ERROR: Failed To Add Course: '{course_code}' To Programme: '{programme_title}'.")
    elif "Error" in new_programme_course:
        print(f"ERROR: {new_programme_course['Error']}")
    else:
        print(f"SUCCESS: Programme Updated Successfully!\nUpdated Details: {new_programme_course['CourseProgramme']}")

@programme_cli.command('update_programme', help="Updates Information For An Existing Programme")
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

@programme_cli.command('list_programmes', help="Retrieve And Lists All Programmes In The Database")
@click.argument("format", default="json")
def list_programmes_command(format):
    if format == 'string':
        print(list_programmes())
    else:
        print(list_programmes_json())

@programme_cli.command('list_programme_courses', help="List All Courses For A Specific Programme")
@click.option('--programme_title', '-pt', prompt="Enter Programme Title", help="Title Of The Programme")
def list_programme_courses_command(programme_title):
    print(list_programme_courses(programme_title))

app.cli.add_command(programme_cli)


"""
Semester Commands 
Written by Jalene Armstrong (Jalene A) - Task 07.2.2. Semester Group Commands Implementation
"""
semester_cli = AppGroup('semester', help='Semester Object Commands')

@semester_cli.command('add_semester', help="Creates Adds A New Semester")
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

@semester_cli.command('fetch_semester', help="Gets Details For A Specific Semester")
@click.option('--semester_name', '-n', prompt="Enter Semester Name", help="Name Of The Semester")
@click.option('--academic_year', '-a', prompt="Enter Academic Year (YYYY/YYYY)", help="Academic Year Of The Semester")
def fetch_semester_command(semester_name, academic_year):
    fetched_semester = get_semester(semesterName=semester_name, academicYear=academic_year)

    if isinstance(fetched_semester, dict) and "Error Message" in fetched_semester:
        print(f"ERROR: {fetched_semester['Error Message']}")
    elif isinstance(fetched_semester, Semester):
        print(f"Semester Details: {fetched_semester}")
    else:
        print("ERROR: Failed To Fetch Requested Semester.")

@semester_cli.command('update_semester', help="Updates Information For An Existing Semester")
@click.option('--semester_name', '-s', prompt="Enter Semester Name", help="Name Of The Semester")
@click.option('--academic_year', '-a', prompt="Enter Academic Year (YYYY/YYYY)", help="Academic Year Of The Semester")
@click.option('--new_semester_name', '-snew', default=None, help="New Semester Name (Optional)")
@click.option('--new_academic_year', '-anew', default=None, help="New Academic Year (Optional)")
@click.option('--start_date', '-st', default=None, type=click.DateTime(formats=["%Y-%m-%d"]), help="New Start Date (Optional)")
@click.option('--end_date', '-e', default=None, type=click.DateTime(formats=["%Y-%m-%d"]), help="New End Date (Optional)")
def update_semester_command(semester_name, academic_year, new_semester_name, new_academic_year, start_date, end_date):
    semester_to_update = Semester.query.filter_by(semesterName=semester_name, academicYear=academic_year).first()

    if not semester_to_update:
        print(f"ERROR: Semester '{semester_name}' for Academic Year '{academic_year}' Not Found.")
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
        semesterName=semester_name,
        academicYear=academic_year,
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
        print(f"SUCCESS: Semester '{semester_name}' Updated Successfully!\nUpdated Details: {updated_semester['Semester Updated']}")

@semester_cli.command('list_semesters', help="Retrieve And Lists All Semesters In The Database")
@click.argument("format", default="json")
def list_semesters_command(format):
    if format == 'string':
        print(list_semesters())
    else:
        print(list_semesters_json())

@semester_cli.command('list_year_semesters', help="Retrieve And Lists All Semesters In The Database Based On Academic Year")
@click.option('--academic_year', '-a', prompt="Enter Academic Year (YYYY/YYYY)", help="Academic Year Of The Semester")
def list_year_semesters_command(academic_year):
    print(get_semesters_by_academic_year(academic_year))

@semester_cli.command('list_semester_courses', help="List All Courses For A Specific Semester")
@click.option('--semester_name', '-s', prompt="Enter Semester  Name", help="Name Of The Semester")
@click.option('--academic_year', '-a', prompt="Enter Academic Year (YYYY/YYYY)", help="Academic Year Of The Semester")
def list_semester_courses_command(semester_name, academic_year):
    print(list_courses_for_semester(semester_name, academic_year))

app.cli.add_command(semester_cli)


"""
Admin Commands 
Written by Jalene Armstrong (Jalene A) - Task 07.2.3. Admin Group Commands Implementation
"""

admin_cli = AppGroup('admin', help='Admin Object Commands')

@admin_cli.command('create_admin', help="Creates An Admin Account")
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

@admin_cli.command('register_staff', help="Registers A Staff Account To The System")
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

@admin_cli.command('delete_admin', help="Deletes An Admin Account")
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

@admin_cli.command('update_admin', help="Updates An Existing Admin Account")
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

@admin_cli.command('list_admins', help="Retrieve And Lists All Admins In The Database")
@click.argument("format", default="json")
def list_admins_command(format):
    if format == 'string':
        print(get_all_admin_users())
    else:
        print(get_all_admin_users_json())

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
def user_tests_command(type):
    if type == "int":
        sys.exit(pytest.main(["-k", "StaffIntegrationTests"]))
    elif type == "unit":
        sys.exit(pytest.main(["-k", "StaffUnitTest"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

@test.command("admin", help="Run Admin Tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "int":
        sys.exit(pytest.main(["-k", "AdminIntegrationTests"]))
    elif type == "unit":
        sys.exit(pytest.main(["-k", "AdminUnitTest"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

@test.command("course", help="Run Course Tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "int":
        sys.exit(pytest.main(["-k", "CourseIntegrationTests"]))
    elif type == "unit":
        sys.exit(pytest.main(["-k", "CourseUnitTest"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

@test.command("semester", help="Run Semester Tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "int":
        sys.exit(pytest.main(["-k", "SemesterIntegrationTests"]))
    elif type == "unit":
        sys.exit(pytest.main(["-k", "SemesterUnitTest"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

# Unit Tests Only
@test.command("programme", help="Run Programme Tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "ProgrammeUnitTest"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

@test.command("assessment", help="Run Assessment Tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "AssessmentUnitTest"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

app.cli.add_command(test)