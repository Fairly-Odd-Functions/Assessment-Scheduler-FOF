import click, sys, csv
from flask import Flask
from datetime import datetime
from App.main import create_app
from App.database import db, get_migrate
from flask.cli import with_appcontext, AppGroup
from App.controllers import *
from App.models import *

app = create_app()
migrate = get_migrate(app)

# Command 01 : Creates And Initializes The Database
@app.cli.command("init", help="Creates And Initializes The Database")
def init():
    initialize()
    print('Database Initialized!')

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

    new_semester_name = new_semester_name or input(f"Enter New Semester Name (Current: {semester_to_update.semesterName}): ") or semester_to_update.semesterName
    new_academic_year = new_academic_year or input(f"Enter New Academic Year (Current: {semester_to_update.academicYear}): ") or semester_to_update.academicYear
    start_date = start_date or (input(f"Enter New Start Date (Current: {semester_to_update.startDate}): ") or semester_to_update.startDate)
    end_date = end_date or (input(f"Enter New End Date (Current: {semester_to_update.endDate}): ") or semester_to_update.endDate)

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
        print(f"SUCCESS: Semester '{semester_name}' Updated Successfully! Updated Details: {updated_semester['Semester Updated']}")

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
        firstname = input(f"Enter New First Name (Current: {admin_to_update.firstName}): ") or admin_to_update.firstName
    if not lastname:
        lastname = input(f"Enter New Last Name (Current: {admin_to_update.lastName}): ") or admin_to_update.lastName
    if not password:
        password = input("Enter New Password: ") or admin_to_update.password
    if not email:
        email = input(f"Enter New Email (Current: {admin_to_update.email}): ") or admin_to_update.email

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