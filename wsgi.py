import click, sys, csv
from flask import Flask
from App.main import create_app
from App.database import db, get_migrate
from App.main import create_app
from App.database import db, get_migrate
from flask.cli import with_appcontext, AppGroup
from App.models import Staff, Course, Assessment, Programme, Admin

from App.controllers import *
 
app = create_app()

# This command creates and initializes the database
@app.cli.command("init", help="Creates And Initializes The Database")
def init():
    initialize()
    print('\n Database Intialized! \n')


'''
|   Staff Group Commands
|   These are a list of commands used to perform operations involving existing staff
'''
staff_cli = AppGroup('staff', help='Staff object commands')

# COMMAND #1 - ADD STAFF
@staff_cli.command('add', help='Add a new staff member')
def add_staff():
    
    firstName = input("Enter First Name: ")
    lastName = input("Enter Last Name: ")

    staffID = input("Enter Password (StafID e.g. 816012345): ")

    # Validate the staff ID
    while len(staffID) != 9 or not staffID.isdigit():
        staffID = input("Invalid staff ID. Please enter a 9-digit staff ID (e.g. 816012345): ")

    password = staffID  # Set the password to the give staff ID (Default password)

    email = input("Enter Email: ")

    newstaff = register_staff(firstName, lastName, password, email)

    if newstaff:
        print(f"\nNew Staff Member '{newstaff.firstName} {newstaff.lastName}' Added! \n")
    else:
        print("\n Staff Member Already Exists! \n")

# COMMAND #2 - UPDATE STAFF
@staff_cli.command('update', help='Update a staff member details')
def update_staff():
    
    #Prompting for staff
    staffEmail = input("Enter Staff Email: ")

    #Retrieving staff
    staff = get_staff_by_email(staffEmail)
    if not staff:
        print("\nStaff Member Does Not Exist!\n")
        return
    
    #Displaying staff details
    print("\nCurrent Staff Member Details:")
    print(staff)

    #Prompting for new details
    print("\nEnter New Details... \n")    
    firstName = input("Update First Name: ")
    lastName = input("Update Last Name: ")
    password = input("Update Password: ")
    email = input("Update Email: ")

    #Updating staff
    updated_staff = update_staff(staffEmail, firstName, lastName, password, email)

    #Displaying diferent results of the update
    if updated_staff != staff:
        print(updated_staff)

    elif updated_staff == staff:
        print("\n No Changes Were Made \n")

    else:
        print("\n Error! \n")
        print(updated_staff["error"])

app.cli.add_command(staff_cli)

"""
TO BE REFACTORED ~ JaleneA

# This command retrieves all staff objects
@app.cli.command('get-users')
def get_users():
    staff = Staff.query.all()
    for s in staff:
      print(s.to_json())
    print('end of staff objects')
    staff = Staff.query.all()
    for s in staff:
      print(s.to_json())
    print('end of staff objects')

# This command creates all the Assessment objects
@app.cli.command("asm")
def load_Asm():
    db.create_all()
    asm1 = Assessment(category='EXAM')
    db.session.add(asm1)
    db.session.commit()
    db.create_all()
    asm1 = Assessment(category='EXAM')
    db.session.add(asm1)
    db.session.commit()

    asm2 = Assessment(category='ASSIGNMENT')
    db.session.add(asm2)
    db.session.commit()
    asm2 = Assessment(category='ASSIGNMENT')
    db.session.add(asm2)
    db.session.commit()

    asm3 = Assessment(category='QUIZ')
    db.session.add(asm3)
    db.session.commit()
    asm3 = Assessment(category='QUIZ')
    db.session.add(asm3)
    db.session.commit()

    asm4 = Assessment(category='PROJECT')
    db.session.add(asm4)
    db.session.commit()
    asm4 = Assessment(category='PROJECT')
    db.session.add(asm4)
    db.session.commit()

    asm5 = Assessment(category='DEBATE')
    db.session.add(asm5)
    db.session.commit()
    asm5 = Assessment(category='DEBATE')
    db.session.add(asm5)
    db.session.commit()

    asm6 = Assessment(category='PRESENTATION')
    db.session.add(asm6)
    db.session.commit()
    asm6 = Assessment(category='PRESENTATION')
    db.session.add(asm6)
    db.session.commit()

    asm7 = Assessment(category='ORALEXAM')
    db.session.add(asm7)
    db.session.commit()
    asm7 = Assessment(category='ORALEXAM')
    db.session.add(asm7)
    db.session.commit()

    asm8 = Assessment(category='PARTICIPATION')
    db.session.add(asm8)
    db.session.commit()
    print('All assessments added')
    asm8 = Assessment(category='PARTICIPATION')
    db.session.add(asm8)
    db.session.commit()
    print('All assessments added')

# This command creates all the Programme objects
@app.cli.command("pgr")
def load_Pgr():
    db.create_all()
    pgr1 = Programme(p_name='Computer Science Major')
    db.session.add(pgr1)
    db.session.commit()
    db.create_all()
    pgr1 = Programme(p_name='Computer Science Major')
    db.session.add(pgr1)
    db.session.commit()

    pgr2 = Programme(p_name='Computer Science Minor')
    db.session.add(pgr2)
    db.session.commit()
    pgr2 = Programme(p_name='Computer Science Minor')
    db.session.add(pgr2)
    db.session.commit()

    pgr3 = Programme(p_name='Computer Science Special')
    db.session.add(pgr3)
    db.session.commit()
    pgr3 = Programme(p_name='Computer Science Special')
    db.session.add(pgr3)
    db.session.commit()

    pgr4 = Programme(p_name='Information Technology Major')
    db.session.add(pgr4)
    db.session.commit()
    pgr4 = Programme(p_name='Information Technology Major')
    db.session.add(pgr4)
    db.session.commit()

    pgr5 = Programme(p_name='Information Technology Minor')
    db.session.add(pgr5)
    db.session.commit()
    pgr5 = Programme(p_name='Information Technology Minor')
    db.session.add(pgr5)
    db.session.commit()

    pgr6 = Programme(p_name='Information Technology Special')
    db.session.add(pgr6)
    db.session.commit()
    pgr6 = Programme(p_name='Information Technology Special')
    db.session.add(pgr6)
    db.session.commit()

    print('All programmes added')
    print('All programmes added')

# This command assigns courses to staff
@app.cli.command("add-course")
@click.argument("staff_ID")
def assign_course(staff_ID):
    bob = Staff.query.filter_by(u_ID=staff_ID).first()

    if not bob:
        print(f'Staff with ID: {staff_ID} not found!')
        return
      
    bob.coursesAssigned = ["COMP1601", "COMP1602", "COMP1603"]
    db.session.add(bob)
    db.session.commit()
    print(bob)
    print('courses added')
    bob = Staff.query.filter_by(u_ID=staff_ID).first()

    if not bob:
        print(f'Staff with ID: {staff_ID} not found!')
        return
      
    bob.coursesAssigned = ["COMP1601", "COMP1602", "COMP1603"]
    db.session.add(bob)
    db.session.commit()
    print(bob)
    print('courses added')

#load course data from csv file
@app.cli.command("load-courses")
def load_course_data():
    with open('courses.csv') as file: #csv files are used for spreadsheets
      reader = csv.DictReader(file)
      for row in reader: 
        new_course = Course(courseCode=row['courseCode'], courseTitle=row['courseTitle'], description=row['description'], 
          level=row['level'], semester=row['semester'], preReqs=row['preReqs'], p_ID=row['p_ID'],)  #create object
        db.session.add(new_course) 
      db.session.commit() #save all changes OUTSIDE the loop
    print('database intialized')

    with open('courses.csv') as file: #csv files are used for spreadsheets
      reader = csv.DictReader(file)
      for row in reader: 
        new_course = Course(courseCode=row['courseCode'], courseTitle=row['courseTitle'], description=row['description'], 
          level=row['level'], semester=row['semester'], preReqs=row['preReqs'], p_ID=row['p_ID'],)  #create object
        db.session.add(new_course) 
      db.session.commit() #save all changes OUTSIDE the loop
    print('database intialized')
"""