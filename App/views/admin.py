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
Written By
"""
# 01 : Register Staff
@admin_views.route('/registerStaff', methods=['POST'])
@jwt_required(Admin)
def register_staff_action():
    pass
    
# 02 : Create Admin
@admin_views.route('/createAdmin', methods=['POST'])
@jwt_required(Admin)
def create_admin_action():
    pass

# 03 : Get All Staff Users
@admin_views.route('/allStaff', methods=['GET'])
@jwt_required(Admin)
def list_all_staff_action():
    pass

# 04 : Get All Admin Users
@admin_views.route('/allAdmin', methods=['GET'])
@jwt_required(Admin)
def list_all_admin_action():
    pass

# 05 : Update Admin
@admin_views.route('/updateAdmin', methods=['POST'])
@jwt_required(Admin)
def update_admin_action():
    pass

# 06 : Remove Admin
@admin_views.route('/removeAdmin', methods=['POST'])
@jwt_required(Admin)
def remove_admin_action():
    pass

# 07 : Update Staff
@admin_views.route('/updateStaff', methods=['POST'])
@jwt_required(Admin)
def update_staff_action():
    pass

# 08 : Remove Staff
@admin_views.route('/removeStaff', methods=['POST'])
@jwt_required(Admin)
def remove_staff_action():
    pass

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
        course = add_Course(courseCode,title,description,level,semester,numAssessments)
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

        delete_Course(get_course(courseCode)) # Woah that's extreme
        add_Course(courseCode, title, description, level, semester, numAssessments)
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
Written By Daniel Young
"""
@admin_views.route('/addProgrammeCourse', methods=['POST'])
@jwt_required(Admin)
def add_programme_course_action():
    data = request.json
    courseCode = data['courseCode']
    programmeID = data['programmeID']

    response = add_course_to_programme(courseCode, programmeID)
    if "Error Message" in response:
        return jsonify ({"message" : response["Error Message"]}),400

    if "CourseProgramme" in response:
        return jsonify({
            "message" : response["Message"],
            "CourseProgramme" : response["CourseProgramme"]
        }),201
    return jsonify({"message":"An unknown error occured"}),500

# 02 : Remove Programme Course
@admin_views.route('/removeProgrammeCourse', methods=['POST'])
@jwt_required(Admin)
def remove_programme_course_action():
    data = request.json
    courseCode = data['courseCode']
    programmeID = data['programmeID']

    response = remove_course_from_programme(courseCode, programmeID)
    if "Error Message" in response:
        return jsonify ({"message" : response["Error Message"]}),400
    if "Message" in response:
        return jsonify({
            "message" : response["Message"]
        }),201
    return jsonify({"message":"Unable to delete"}), 500

# @admin_views.route('/getProgrammeCourse', methods=['GET'])


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
Written By Daniel Young
"""

# 01 : Add Programme
@admin_views.route('/addProgramme', methods=['POST'])
@jwt_required(Admin)
def add_programme_action():
    data = request.json
    programmeTitle = data['programmeTitle']
    programmeDescription = data['programmeDescription']

    response = create_programme(programmeTitle, programmeDescription)
    if "Error Message" in response:
        return jsonify({"message" : response["Error Message"]}), 400
    if "Programme" in response:
        return jsonify({
            "message" : reponse["Message"],
            "Programme" : response["Programme"]
        }),201
    return jsonify({"message":"An unknown error occorred"}),500

# 02 : Remove Programme
@admin_views.route('/removeProgramme', methods=['POST'])
@jwt_required(Admin)
def remove_programme_action():
    pass

# 03 : Update Programme
@admin_views.route('/updateProgramme', methods=['POST'])
@jwt_required(Admin)
def update_programme_action():
    data = request.json
    programmeTitle = data{}
    update_programme(programmeTitle, new_title=None, new_description=None)

# 05 : Get Programme Course
@user_views.route('/getProgrammeCourse', methods=['GET'])
@jwt_required()
def get_programme_course_action():
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

# 08 : Programme by ID
@user_views.route('/getProgrammeByID<int:programmeID>', methods=['GET'])
@jwt_required()
def get_programme_by_id_action(programmeID):
    pass

# 08 : Programme by title
@user_views.route('/getProgrammeByTitle<string:programmeTitle>', methods=['GET'])
@jwt_required()
def get_programme_by_id_action(programmeTitle):
    pass