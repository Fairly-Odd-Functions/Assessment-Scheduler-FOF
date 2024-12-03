from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from App.models import Staff, Admin
from flask_jwt_extended import current_user as jwt_current_user, get_jwt_identity
from flask_jwt_extended import jwt_required
from App.database import db
from App.controllers import *
# IMPORTS TO CLEAN UP

user_views = Blueprint('user_views', __name__, template_folder='../templates')

"""
User Views [total : 5]
Written by RynniaRyan (Rynnia.R) - Task 10.2 Implement API Views for User
Comment: Original views template made by Jalene has been modified and moved to Admin Views as requested :)
"""

# 01 : Search Course by Code or Title
@user_views.route('/courseSearch/<string:courseCode>', methods=['GET'])
@jwt_required()
def search_course_action(courseCode):

    if courseCode:
        try:
            course = get_course_by_code(courseCode) #course variable already holds a dictionary
            
            if course.get("Error"):
                return jsonify(course), 404
            else:
                return jsonify(course), 200
            
        except Exception as e:
            print(f"Error: {e}")
            return jsonify(error=f"An error occurred while searching for the course"), 500
    else:
        return jsonify(error="Please provide a course code"), 400
    
# 02 : Get Admin by Email
@user_views.route("/adminSearch/<string:email>", methods=["GET"])
@jwt_required()
def search_admin_action(email):
    if email:
        try:
            admin = get_admin_by_email(email)
            if admin is None:
                return jsonify(error="Admin not found"), 404
            else:
                return jsonify(admin.get_json()), 200
            
        except Exception as e:
            print(f"Error: {e}")
            return jsonify(error=f"An error occurred while searching for admin with email '{email}'"), 500
    else:
        return jsonify(error="Please provide an email"), 400

# 03 : Get Staff by Email
@user_views.route("/staffSearch/<string:email>", methods=["GET"])
@jwt_required()
def search_staff_action(email):

    if email:
        try:
            staff = get_staff_by_email(email)

            if staff is None:
                return jsonify(error="Staff not found"), 404
            else:
                return jsonify(staff.get_json()), 200
            
        except Exception as e:
            print(f"Error: {e}")            
            return jsonify(error=f"An error occurred while searching for staff with email '{email}'"), 500
    else:
        return jsonify(error="Please provide an email"), 400

# 04 : Get Staff Courses
@user_views.route("/staffCourses\<string:email>", methods=["GET"])
@jwt_required()
def get_staff_courses_action(email):

    if email:
        try :
            staff_courses = get_staff_with_courses(email)

            if staff_courses is None:
                return jsonify(error="Staff not found"), 404
            else:
                return jsonify(staff_courses), 200
            
        except Exception as e:
            print(f"Error: {e}")
            return jsonify(error=f"An error occurred while searching for the staff with email '{email}'"), 500
    else:
        return jsonify(error="Please provide an email"), 400
    
# 05 : Get Course Staff - Not to be confused with get staff with courses
@user_views.route("/courseStaff", methods=["GET"])
@jwt_required()
def get_course_staff_action():

    data = request.get_json()
    courseCode = data.get('courseCode')
    semesterName = data.get('semesterName')
    academicYear = data.get('academicYear')
 

    if not courseCode or not semesterName or not academicYear:
        try:    
            course_staff = get_course_staff(courseCode, semesterName, academicYear)    

            if course_staff.get("Error"):        
                return jsonify(course_staff), 404
            
            elif course_staff.get("Message"):
                return jsonify(course_staff), 404
            
            else:
                return jsonify(course_staff), 200
            
        except Exception as e:
            print(f"Error: {e}")
            return jsonify(error=f"An error occurred while searching for the course with code '{courseCode}'"), 500
    else:
        return jsonify(error="Please provide a course code"), 400