import click, sys, csv
from flask import Flask
from App.main import create_app
from App.database import db, get_migrate
from flask.cli import with_appcontext, AppGroup
from App.models import Staff, Course, Assessment, Programme, Admin

from App.controllers import *
from datetime import datetime
 
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
        print(f"\nError: An error occurred while adding course {coursecode}\n")
        print()

# COMMAND #2 : EDIT A COURSE
@course_cli.command('edit', help='Edit A Course')
@click.option('--coursecode', '-c', prompt='Enter Course Code To Edit', required=True)
def update_course(coursecode):

    response = get_course_by_code(coursecode)

    if 'Error' in response:
        print()
        print(response)
        print()
        return
    else:
        print(f"\nEnter New Course Details For {coursecode}. . .")

        coursetitle = input('\nEdit Course Title (press Enter to keep the current value): ') or None
        coursecredits = input('Edit Course Credits (press Enter to keep the current value): ') or None
        coursedescription = input('Edit Course Description (press Enter to keep the current value): ') or None
        courselevel = input('Edit Course Level (press Enter to keep the current value): ') or None

        result = edit_course(coursecode, coursetitle, coursecredits, coursedescription, courselevel)

        if result:
            print()
            print(result)
            print()
        else:
            print()
            print(f"\nError: An error occurred while updating course {coursecode}\n")
            print()

# COMMAND #3 : SEARCH FOR A COURSE
@course_cli.command('search', help='Search For A Course')
@click.option('--coursecode', '-c', prompt='Enter Course Code', required=True)
def search_course(coursecode):
    
    course= get_course_by_code(coursecode)

    if course:
        print()
        print(course)
        print()
    else:
        print()
        print("\nError: An error occurred while searching for the course\n")
        print()

# COMMAND #4 : VIEW ALL COURSES
@course_cli.command('list-all', help='View All Courses')
def get_all_courses():
    
    courses = list_courses()

    if courses:
        print()
        print(courses)
        print()
    else:
        print()
        print("\nError: An error occurred while obtaining all courses\n")
        print()

# COMMAND #5 : ADD ASSESSMENT TO A COURSE
@course_cli.command('add-assessment', help='Add Assessment To A Course')
@click.option('--coursecode', '-c', prompt='Enter Course Code', required=True)
@click.option('--assessmentcode', '-a', prompt='Enter Assessment Code', required=True)
def add_assessment_to_course(coursecode, assessmentcode):

    result = add_course_assessment(coursecode, assessmentcode)

    if result:
        print()
        print(result)
        print()
    else:
        print()
        print(f"\nError: An error occurred while assigning assessment to {coursecode}\n")
        print()

# COMMAND #6 : REMOVE ASSESSMENT FROM A COURSE
@course_cli.command('remove-assessment', help='Remove Assessment From A Course')
@click.option('--coursecode', '-c', prompt='Enter Course Code', required=True)
@click.option('--courseassessmentcode', '-c', prompt='Enter Course Assessment Code', required=True)
def remove_assessment_from_course(coursecode,courseassessmentcode):

    result = delete_course_assessment(courseassessmentcode)

    if result:
        print()
        print(result)
        print()
    else:
        print()
        print(f"\nError: An error occurred while removing assessment from {coursecode}\n")
        print()

# COMMAND #7 : VIEW ALL ASSESSMENTS FOR A COURSE
@course_cli.command('list-assessments', help='View All Assessments For A Course')
@click.option('--coursecode', '-c', prompt='Enter Course Code', required=True)
def get_all_assessments_for_course(coursecode):
    
    assessments = list_course_assessments(coursecode)

    if assessments:
        print()
        print(assessments)
        print()
    else:
        print()
        print("\nError: An error occurred while obtaining all assessments for the course\n")
        print()

app.cli.add_command(course_cli)