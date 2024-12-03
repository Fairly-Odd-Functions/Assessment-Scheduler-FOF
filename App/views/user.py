from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from App.models import Staff, Admin
from flask_jwt_extended import current_user as jwt_current_user, get_jwt_identity
from flask_jwt_extended import jwt_required
from App.database import db
from App.controllers import *
# IMPORTS TO CLEAN UP

user_views = Blueprint('user_views', __name__, template_folder='../templates')

# @user_views.route('/login', methods=['POST'])
# def login_staff_action():
#     email = request.form.get('email')
#     password = request.form.get('password')
#     user = db.session.query(Staff).filter(Staff.email==email).first()
#     if user == None:
#         user = db.session.query(Admin).filter(Admin.u_ID==email).first()
#         if user!=None:
#             if login_admin(email, password):
#                 return user, 'Login Successful' , 200
#             else:
#                 return 'Login Failed' , 401
#     else:
#         if login_staff(email, password):
#             return 'Login Successful' , 200
#         else:
#             return 'Login Failed' , 401

# 02 : Get Course Degree Programme - Written by RynniaRyan (Rynnia.R)
# @user_views.route("/courseProgramme/<string:courseCode>", methods=["GET"])
# @jwt_required()
# def get_course_programme_action(courseCode):
#     try:
#         courseProgramme = get_degree_programme(courseCode)
#         if courseProgramme:
#             return jsonify(courseProgramme), 200
#         else:
#             return jsonify(error="Course Programme not found"), 404
    
#     except Exception as e:
#         print(f"Error: {e}")
#         return jsonify(error=f"An Error Occurred While Obtaining Course Programme for '{courseCode}'"), 500


"""
User Views [total : 11]
Written by RynniaRyan (Rynnia.R) - Task 10.2 Implement API Views for User
Comment: Original views template made by Jalene has been modified and moved to Admin Views as requested :)
"""

# 01 : Search Course by Code or Title
@user_views.route('/courseSearch', methods=['GET'])
@jwt_required()
def search_course_action():
    course_code = request.args.get('code', type=str)  #Converts whatever value to a string
    course_title = request.args.get('title', type=str)

    if course_code:
        try:
            course = get_course_by_code(course_code)
            if course:
                return jsonify(course.get_json()), 200
            else:
                return jsonify(error="Course not found"), 404
        except Exception as e:
            print(f"Error: {e}")
            return jsonify(error=f"An error occurred while searching for the course"), 500
    elif course_title:
        try:
            course = Course.query.filter_by(courseTitle=course_title).first()
            if course:
                return jsonify(course), 200
            else:
                return jsonify(error="No courses found with this title"), 404
        except Exception as e:
            print(f"Error: {e}")
            return jsonify(error=f"An error occurred while searching for the course"), 500
    else:
        return jsonify(error="Please provide either a course code or title"), 400
    
# 02 : Get Admin by Email
@user_views.route("/adminSearch/<string:email>", methods=["GET"])
@jwt_required()
def search_admin_action(email):
    if email:
        try:
            admin = get_admin_by_email(email)
            if admin:
                return jsonify(admin), 200
            else:
                return jsonify(error="Admin not found"), 404
            
        except Exception as e:
            print(f"Error: {e}")
            return jsonify(error=f"An error occurred while searching for the admin"), 500
    else:
        return jsonify(error="Please provide an email"), 400
        return jsonify(error="Please provide either an email or first name and last name"), 400

# 03 : Get Staff by Email
@user_views.route("/staffSearch/<string:email>", methods=["GET"])
@jwt_required()
def search_staff_action(email):

    if email:
        try:
            staff = get_staff_by_email(email)
            if staff:
                return jsonify(staff), 200
            else:
                return jsonify(error="Staff not found"), 404
            
        except Exception as e:
            print(f"Error: {e}")            
            return jsonify(error=f"An error occurred while searching for the staff with email '{email}'"), 500
    else:
        return jsonify(error="Please provide an email"), 400

# 04 : Get Staff Courses
@user_views.route("/staffCourses\<string:email>", methods=["GET"])
@jwt_required()
def get_staff_courses_action(email):

    if email:
        try :
            staff_courses = get_staff_with_courses(email)
            if staff_courses:
                return jsonify(staff_courses), 200
            else:
                return jsonify(error="Staff not found"), 404
            
        except Exception as e:
            print(f"Error: {e}")
            return jsonify(error=f"An error occurred while searching for the staff with email '{email}'"), 500
    else:
        return jsonify(error="Please provide an email"), 400
    
# 05 : Get Course Staff - Not to be confused with get staff with courses
@user_views.route("/courseStaff", methods=["GET"])
@jwt_required()
def get_course_staff_action():

    #Obtaining specified coursecode, semesterName and  academicYear
    courseCode = request.args.get('courseCode', type=str)
    semesterName = request.args.get('semesterName', type=str)
    academicYear = request.args.get('academicYear', type=str)

    if courseCode:
        try:    
            course_staff = get_course_staff(courseCode, semesterName, academicYear)    
            if course_staff:        
                return jsonify(course_staff), 200
            else:
                return jsonify(error="Course not found"), 404
            
        except Exception as e:
            print(f"Error: {e}")
            return jsonify(error=f"An error occurred while searching for the course with code '{courseCode}'"), 500
    else:
        return jsonify(error="Please provide a course code"), 400