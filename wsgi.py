import click, sys, csv
from flask import Flask
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
Assessment Commands 
Written by Jalene Armstrong (Jalene A) - Task 07.1.3. Assessment Group Commands Implementation
"""

assessment_cli = AppGroup('assessment', help='Assessment Object Commands')

@assessment_cli.command('create_assessment', help="Creates A New Assessment For A Particular Course")
@click.option('--assessment_title', '-at', prompt="Enter Assessment Title", help="Title Of Assessment")
@click.option('--assessment_type', '-aty', prompt="Enter Assessment Type", help="Type Of Assessment")
@click.option('--start_date', '-s', prompt="Enter Start Date (YYYY-MM-DD HH:MM:SS)", 
              type=click.DateTime(formats=["%Y-%m-%d %H:%M:%S"]), help="Start Date Of The Assessment")
@click.option('--due_date', '-e', prompt="Enter Due Date (YYYY-MM-DD HH:MM:SS)", 
              type=click.DateTime(formats=["%Y-%m-%d %H:%M:%S"]), help="End Date Of The Assessment")
def create_assessment_command(assessment_title, assessment_type, start_date, due_date):

    new_assessment = create_assessment(assessment_title, assessment_type, start_date, due_date)

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
