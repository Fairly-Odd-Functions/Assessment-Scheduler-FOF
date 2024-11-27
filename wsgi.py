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
@click.option('--firstname', prompt='Enter First Name', required=True)
@click.option('--lastname', prompt='Enter the Last Name', required=True)
@click.option('--email', prompt='Enter Email', required=True)
@click.option('--password', prompt='Enter Password', required=True)
def add_staff(firstname, lastname, email, password):
    
    #Adding staff
    newStaff = register_staff(firstname, lastname, password, email)
    
    if newStaff:
        print(f"\nNew Staff Member '{newStaff.firstName} {newStaff.lastName}' Added! \n")
    else:
        print("\nStaff Member Already Exists! \n")

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
@click.option('--staffemail', prompt='Enter the staff email', required=True)
def delete_staff_profile(staffemail):

    result = delete_staff(staffemail)
    print("\n" + result)

    

app.cli.add_command(staff_cli)