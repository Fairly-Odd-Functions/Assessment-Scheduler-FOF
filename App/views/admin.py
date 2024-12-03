import os, csv
from App.database import db
from App.models import Admin
from datetime import datetime
from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required
from App.controllers import *
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
# IMPORTS TO CLEAN UP

admin_views = Blueprint('admin_views', __name__, template_folder='../templates')

# * - PPC [Previous Project's Code :D]

"""
Users [8]
Written By Rynnia(Rynnia.R) - Task 10.3. Implement API Views for Admin (Main)
"""
# 01 : Register Staff
@admin_views.route('/registerStaff', methods=['POST'])
@jwt_required(Admin)
def register_staff_action():
    data = request.form
    firstName = data.get('firstName')
    lastName = data.get('lastName')
    email = data.get('email')
    password = data.get('password')

    result = register_staff(firstName, lastName, password, email)

    if result is None:
        return jsonify(error = "Staff with this email or password already exists"), 400
    
    if isinstance(result, dict):
        return jsonify(error = result["error"]), 400
    
    if result:
        return jsonify(message = "Staff registered successfully"), 201

    return jsonify(error = "An unknown error occurred"), 500
    
# 02 : Create Admin
@admin_views.route('/createAdmin', methods=['POST'])
@jwt_required(Admin)
def create_admin_action():
    
    data = request.form
    firstName = data.get('firstName')
    lastName = data.get('lastName')
    email = data.get('email')
    password = data.get('password')

    result = create_admin(firstName, lastName, password, email)

    if result is None:
        return jsonify(error = "Admin with this email already exists"), 400
    
    if result:
        return jsonify(message = "Admin created successfully"), 201

    return jsonify(error = "An unknown error occurred"), 500

# 03 : Get All Staff Users
@admin_views.route('/allStaff', methods=['GET'])
@jwt_required(Admin)
def list_all_staff_action():
    
    allStaff = get_all_staff()

    if allStaff is None:
        #there is no staff
        return jsonify(error = "No Staff Found."), 404

    elif allStaff:

        allStaff = [staff.get_json() for staff in allStaff]
        return jsonify(allStaff), 200    
    else:
        return jsonify(error = "An unknown error occurred"), 500

# 04 : Get All Admin Users
@admin_views.route('/allAdmin', methods=['GET'])
@jwt_required(Admin)
def list_all_admin_action():
    
    allAdmin = get_all_admin_users_json()

    if allAdmin is None:
        return jsonify(error = "No Admin Found."), 404

    elif allAdmin:
        return jsonify(allAdmin), 200    
    
    else:
        return jsonify(error = "An unknown error occurred"), 500

# 05 : Update Staff
@admin_views.route('/updateDmin/<string:staffEmail>', methods=['POST'])
@jwt_required(Admin)
def update_staff_action(staffEmail):
    
    data = request.form
    firstName = data.get('firstName')
    lastName = data.get('lastName')
    email = data.get('email')
    password = data.get('password')

    result = update_staff(staffEmail, firstName, lastName, password, email)

    if "error" in result:
        return jsonify(error = result["error"]), 400
    
    if result:
        return jsonify(message = "Staff member updated successfully"), 200

    return jsonify(error = "An unknown error occurred"), 500

# 06 : Remove Admin
@admin_views.route('/removeAdmin/<string:adminEmail>', methods=['POST'])
@jwt_required(Admin)
def remove_admin_action(adminEmail):

    admin = Admin.query.filter_by(email=adminEmail).first()

    if not admin:
        return jsonify(error = "No Admin Found."), 404

    if admin:
        result = delete_admin(adminEmail)

        if "error" in result:
            return jsonify(error=result["error"]), 400
        
        if result is not None:
            return jsonify(message="Admin deleted successfully"), 200

    return jsonify(error="An unknown error occurred"), 500

# 07 : Update Admin
@admin_views.route('/updateAdmin/<string:adminEmail>', methods=['POST'])
@jwt_required(Admin)
def update_admin_action(adminEmail):
    
    data = request.form
    firstName = data.get('firstName')
    lastName = data.get('lastName')
    email = data.get('email')
    password = data.get('password')

    result = update_admin(adminEmail, firstName, lastName, password, email)

    if "error" in result:
        return jsonify(error = result["error"]), 400
    
    if result:
        return jsonify(message = "Admin updated successfully"), 200

    return jsonify(error = "An unknown error occurred"), 500
    
# 08 : Remove Staff
@admin_views.route('/removeStaff/<string:staffEmail>', methods=['POST'])
@jwt_required(Admin)
def remove_staff_action(staffEmail):
    
    result = delete_staff(staffEmail)

    if "Error" in result:
        return jsonify(error = result), 400
    
    if "Staff member deleted successfully" in result:
        return jsonify(message = result), 200

    return jsonify(error = "An unknown error occurred"), 500

"""
Course [2]
Written By
"""

# 01 : Add Course *
@admin_views.route('/addCourse', methods=['POST'])
@jwt_required(Admin)
def add_course_action():
    if request.method == 'POST':
        courseCode = request.form.get('course_code')
        title = request.form.get('title')
        description = request.form.get('description')
        data = request.form
        level = request.form.get('level')
        semester = request.form.get('semester')
        numAssessments = request.form.get('numAssessments')
        #course = add_Course(courseCode,title,description,level,semester,numAssessments)
        pass

# 02 : Update Course *
@admin_views.route('/updateCourse', methods=['POST'])
@jwt_required(Admin)
def update_course_action():
    if request.method == 'POST':
        courseCode = request.form.get('code')
        title = request.form.get('title')
        description = request.form.get('description')
        level = request.form.get('level')
        semester = request.form.get('semester')
        numAssessments = request.form.get('assessment')
        # programme = request.form.get('programme')

        #delete_Course(get_course(courseCode)) # Woah that's extreme
        #add_Course(courseCode, title, description, level, semester, numAssessments)
        flash("Course Updated Successfully!") 
    pass


"""
Semester [2]
Written By
"""

# 01 : Add Semester *
@admin_views.route('/addSemester', methods=['POST'])
@jwt_required(Admin)
def add_semester_action():
    # if request.method == 'POST':
        # semBegins = request.form.get('teachingBegins')
        # semEnds = request.form.get('teachingEnds')
        # semChoice = request.form.get('semester')
        # maxAssessments = request.form.get('maxAssessments') #used for class detection feature
        # add_sem(semBegins,semEnds,semChoice,maxAssessments)
    pass

# 02 : Update Semester
@admin_views.route('/updateSemester', methods=['POST'])
@jwt_required(Admin)
def update_semester_action():
    pass


"""
ProgrammeCourse [2]
Written By
"""

# 01 : Add Programme Course
@admin_views.route('/addProgrammeCourse', methods=['POST'])
@jwt_required(Admin)
def add_programme_course_action():
    pass

# 02 : Remove Programme Course
@admin_views.route('/removeProgrammeCourse', methods=['POST'])
@jwt_required(Admin)
def remove_programme_course_action():
    pass


"""
CourseOffering [3]
Written By
"""

# 01: Add Course Offering
@admin_views.route('/addCourseOffering', methods=['POST'])
@jwt_required(Admin)
def add_offering_action():
    pass

# 02 : Remove Course Offering
@admin_views.route('/removeCourseOffering', methods=['POST'])
@jwt_required(Admin)
def remove_offering_action():
    pass

# 03 : Update Course Offering
@admin_views.route('/updateCourseOffering', methods=['POST'])
@jwt_required(Admin)
def update_offering_action():
    pass

"""
CourseStaff [3]
Written By
"""
# 01 : Add Course Staff
@admin_views.route('/addCourseStaff', methods=['POST'])
@jwt_required(Admin)
def add_course_staff_action():
    pass

# 02 : Remove Course Staff
@admin_views.route('/removeCourseStaff', methods=['POST'])
@jwt_required(Admin)
def remove_course_staff_action():
    pass

# 03 : Update Course Staff
@admin_views.route('/updateCourseStaff', methods=['POST'])
@jwt_required(Admin)
def update_course_staff_action():
    pass

"""
Programme [3]
Written By
"""

# 01 : Add Programme
@admin_views.route('/addProgramme', methods=['POST'])
@jwt_required(Admin)
def add_programme_action():
    pass

# 02 : Remove Programme
@admin_views.route('/removeProgramme', methods=['POST'])
@jwt_required(Admin)
def remove_programme_action():
    pass

# 03 : Update Programme
@admin_views.route('/updateProgramme', methods=['POST'])
@jwt_required(Admin)
def update_programme_action():
    pass