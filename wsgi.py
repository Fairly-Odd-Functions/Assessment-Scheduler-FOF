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

# @assessment_cli.command('create_assessment', help="Creates A New Assessment For A Particular Course")
# @assessment_cli.command('fetch_assessment', help="Retrieve And Displays Requested Assessment")
# @assessment_cli.command('list_all_assessments', help="Retrieves And List All Assessments In The Database")

app.cli.add_command(assessment_cli)
