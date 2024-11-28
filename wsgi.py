import click, sys, csv
from flask import Flask
from App.main import create_app
from App.database import db, get_migrate
from flask.cli import with_appcontext, AppGroup
from App.models import Staff, Course, Assessment, Programme, Admin

from App.controllers import *
 
# This commands file allow you to create convenient CLI commands for testing controllers!!
app = create_app()

# Command 01 : Creates And Initializes The Database
@app.cli.command("init", help="Creates And Initializes The Database")
def init():
    initialize()
    print('\nDatabase Initialized!\n')

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
        print()
        print(result)
        print()
    else:
        print()
        print("\nError: An error occurred while adding the course\n")
        print()


app.cli.add_command(course_cli)