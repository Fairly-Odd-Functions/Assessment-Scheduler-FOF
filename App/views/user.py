from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from App.models import Staff, Admin
from flask_jwt_extended import current_user as jwt_current_user, get_jwt_identity
from flask_jwt_extended import jwt_required
from App.database import db
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
        


# 01:  List Courses
@user_views.route('/coursesList', methods=['GET'])
@jwt_required()
def list_courses_action():
    pass

# 02 : Get Course By CourseCode
@user_views.route('/courseSearch', methods=['GET'])
@jwt_required()
def search_course_action():
    pass

# 03 : Get Course Degree Programme
@user_views.route("/courseProgramme/<string:courseCode>", methods=["GET"])
@jwt_required()
def get_course_programme_action(courseCode):
    pass
    
# 04 : Get Course Offering
@user_views.route('/getCourseOfferings', methods=['GET'])
@jwt_required()
def get_offerings_action():
    pass
    
# 05 : Get Programme Course
@user_views.route('/getProgrammeCourse', methods=['GET'])
@jwt_required()
def get_programme_course_action():
    pass
    
# 06 : Get Course Staff
@user_views.route('/getCourseStaff', methods=['GET'])
@jwt_required()
def get_course_staff_action():
    pass

# 07 : List Programmes
@user_views.route('/listProgrammes', methods=['GET'])
@jwt_required()
def list_programmes_action():
    pass

# 08 : List Programme Courses
@user_views.route('/listProgrammeCourses', methods=['GET'])
@jwt_required()
def list_programme_courses_action():
    pass

# 09 : Search Semester
@user_views.route('/searchSemester', methods=['GET'])
@jwt_required()
def search_semester_action():
    pass

# 10 : List Semesters
@user_views.route('/listSemesters', methods=['GET'])
@jwt_required()
def list_semesters_action():
    pass

# 11 : List Semester Courses
@user_views.route('/listSemesterCourses', methods=['GET'])
@jwt_required()
def list_semester_courses_action():
    pass