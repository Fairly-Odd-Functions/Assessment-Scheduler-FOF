import os
from flask import Flask
from flask_login import LoginManager, current_user
from flask_uploads import DOCUMENTS, IMAGES, TEXT, UploadSet, configure_uploads
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from datetime import datetime, timedelta
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt_identity,
    jwt_required,
    set_access_cookies,
    unset_jwt_cookies,
)

from App.controllers.auth import setup_flask_login, setup_jwt
from App.database import init_db
from App.config import config

from App.views import views

def add_views(app):
    for view in views:
        app.register_blueprint(view)

def configure_app(app, config, overrides):
    for key, value in config.items():
        if key in overrides:
            app.config[key] = overrides[key]
        else:
            app.config[key] = config[key]

def create_app(config_overrides={}):
    app = Flask(__name__, static_url_path='/static')
    configure_app(app, config, config_overrides)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEVER_NAME'] = '0.0.0.0'
    app.config['PREFERRED_URL_SCHEME'] = 'https'
    app.config['UPLOAD_FOLDER'] = 'App/uploads'  # Configure upload folder (adjust as needed)
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'assessment.scheduler.emails@gmail.com'
    app.config['MAIL_PASSWORD'] = 'mygl qlni lqrz naxm' #'urbs kwoy tvlm zowc' # App Password used 
    app.config['MAIL_USE_TLS'] = True 
    # app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_DEFAULT_SENDER'] = 'assessment.scheduler.emails@gmail.com'
    app.config['JWT_ACCESS_COOKIE_NAME'] = 'access_token'
    app.config["JWT_TOKEN_LOCATION"] = ["cookies", "headers"]
    app.config["JWT_COOKIE_SECURE"] = True
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False
    app.config['DEBUG'] = True
    CORS(app)
    photos = UploadSet('photos', TEXT + DOCUMENTS + IMAGES)
    configure_uploads(app, photos)
    add_views(app)
    init_db(app)
    jwt = setup_jwt(app)
    setup_flask_login(app)
    app.app_context().push()
    return app

import csv
from App.models import db, Admin, Staff, Programme, Course, Assessment, AssessmentTypes, Semester

def parse_users():
    try:
        filepath = os.path.join(os.path.dirname(__file__), 'csv', 'users.csv')
        with open(filepath, encoding='unicode_escape') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                user_type = row['user_type'].lower()

                if user_type == 'staff':
                    staff_member = Staff(
                        firstName=row['firstName'],
                        lastName=row['lastName'],
                        password=row['password'],
                        email=row['email'],
                    )
                    db.session.add(staff_member)

                elif user_type == 'admin':
                    admin_member = Admin(
                        firstName=row['firstName'],
                        lastName=row['lastName'],
                        password=row['password'],
                        email=row['email']
                    )
                    db.session.add(admin_member)
                else:
                    print(f"ERROR: Invalid user_type '{user_type}' In CSV, Skipping This Entry.")
                    continue
            db.session.commit()
        return "SUCCESS: Users Successfully Added To The Database!"

    except Exception as e:
        print(f"ERROR: An Error Occurred While Processing The CSV File: {e}")
        return "ERROR: Failed To Add Users To The Database."

def parse_programmes():
    try:
        filepath = os.path.join(os.path.dirname(__file__), 'csv', 'programmes.csv')
        with open(filepath, encoding='unicode_escape') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                programme = Programme(
                    programmeTitle=row['programmeTitle'],
                    programmeDescription=row['programmeDescription']
                )
                db.session.add(programme)
            db.session.commit()
        return "SUCCESS: Programmes Successfully Added To The Database!"

    except Exception as e:
        print(f"ERROR: An Error Occurred While Processing The CSV File: {e}")
        return "ERROR: Failed To Add Programmes To The Database."

def parse_courses():
    try:
        filepath = os.path.join(os.path.dirname(__file__), 'csv', 'courses.csv')
        with open(filepath, encoding='unicode_escape') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                course = Course(
                    courseCode=row['courseCode'],
                    courseTitle=row['courseTitle'],
                    courseCredits=row['courseCredits'],
                    courseDescription=row['courseDescription'],
                    courseLevel=row['courseLevel']
                )
                db.session.add(course)
            db.session.commit()
        return "SUCCESS: Courses Successfully Added To The Database!"

    except Exception as e:
        print(f"ERROR: An Error Occurred While Processing The CSV File: {e}")
        return "ERROR: Failed To Add Courses To The Database."

def parse_assessments():
    try:
        filepath = os.path.join(os.path.dirname(__file__), 'csv', 'assessments.csv')
        with open(filepath, encoding='unicode_escape') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                assessment_type = AssessmentTypes[row['assessmentType'].upper()]
                assessment = Assessment(
                    assessmentTitle=row['assessmentTitle'],
                    assessmentType=assessment_type
                )
                db.session.add(assessment)
            db.session.commit()
        return "SUCCESS: Assessments Successfully Added To The Database!"

    except Exception as e:
        print(f"ERROR: An Error Occurred While Processing The CSV File: {e}")
        return "ERROR: Failed To Add Assessments To The Database."

def parse_semesters():
    try:
        filepath = os.path.join(os.path.dirname(__file__), 'csv', 'semesters.csv')
        with open(filepath, encoding='unicode_escape') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                start_date = datetime.strptime(row['startDate'], '%Y-%m-%d').date() if row['startDate'] else None
                end_date = datetime.strptime(row['endDate'], '%Y-%m-%d').date() if row['endDate'] else None
        
                semester = Semester(
                    semesterName=row['semesterName'],
                    academicYear=row['academicYear'],
                    startDate=start_date,
                    endDate=end_date
                )
                db.session.add(semester)
            db.session.commit()
        return "SUCCESS: Semesters Successfully Added To The Database!"

    except Exception as e:
        print(f"ERROR: An Error Occurred While Processing The CSV File: {e}")
        return "ERROR: Failed To Add Semesters To The Database."
