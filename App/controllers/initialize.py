from App.models import *
from flask import jsonify
from App.database import db
from App.controllers import *
from datetime import datetime, date

def initialize():
    try:
        db.drop_all()
        db.create_all()

        # Create Default Admin User
        bob = Admin(firstName="Bob", lastName="Bobberson", password="bobpass", email="bob.bobberson@mail.com")

        # Create Default Staff User
        rick = Staff(firstName="Rick", lastName="Rickson", password="rickpass", email="rick.rickson@mail.com")

        # To Be Populated With Good Data For Postman
        course = Course(courseCode="COMP3603", courseTitle="Course", courseCredits=3, courseDescription="Yap", courseLevel=3)
        db.session.add(course)

        db.session.add(bob)
        db.session.add(rick)
        db.session.commit()

    except Exception as e:
        print(f"Error: {e}")
        return jsonify(error="An Error Occurred While Initializing Database"), 500