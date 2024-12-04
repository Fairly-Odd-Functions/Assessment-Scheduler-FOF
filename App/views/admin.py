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
Written By Katoya Ottley

Task Re-Assigned:
Written By: Jalene Armstrong (JaleneA) - Task: 10.3.2. Implement API Views for Admin (CourseOffering)
"""

# 01: Add Course Offering
@admin_views.route('/addCourseOffering/<string:courseCode>', methods=['POST'])
@jwt_required(Admin)
def add_offering_action(courseCode):
    try:
        data = request.get_json()
        semesterID = data["semesterID"]
        totalStudentsEnrolled = data["totalStudentsEnrolled"]

        newCourseOffering = add_course_offering(courseCode, semesterID, totalStudentsEnrolled)

        if "Error" in newCourseOffering:
            return jsonify(error=newCourseOffering["Error"]), 400

        elif "Message" in newCourseOffering:
            course_offering_data = newCourseOffering["CourseOffering"]
            course_offering_data["courseOfferingID"] = newCourseOffering["CourseOffering"]["offeringID"]

            message = f'Course: {course_offering_data["courseCode"]} for Semester ID {course_offering_data["semesterID"]} With {course_offering_data["totalStudentsEnrolled"]} Students Was Added Successfully!'

            response_data = {
                "message": message,
                "courseOfferingID": course_offering_data["courseOfferingID"]
            }
            return jsonify(response_data), 201
    
    except Exception as e:
        print (f"Error While Adding Course Offering: {e}")
        return jsonify(error = "An Error Occurred While Adding Course Offering"), 500

# 02 : Remove Course Offering
@admin_views.route('/removeCourseOffering', methods=['DELETE'])
@jwt_required(Admin)
def remove_offering_action():
    try:
        data = request.get_json()
        courseCode = data["courseCode"]
        semesterID = data["semesterID"]

        if not courseCode or not semesterID:
            return jsonify(error= "All Fields are Required To Remove Course Offering"), 400

        removeCourseOffering = remove_course_offering(courseCode, semesterID)
        if "Error" in removeCourseOffering:
            return jsonify(error=removeCourseOffering["Error"]), 400

        message = removeCourseOffering["Message"]
        return jsonify(message=message), 201

    except Exception as e:
        print (f"Error While Removing Course Offering: {e}")
        return jsonify(error = "An Error Occurred While Removing Course Offering"), 500

''' 
Controller Available In CLI Polishing Branch - To Be Implemented in main

# 03 : Update Course Offering
@admin_views.route('/updateCourseOffering', methods=['POST'])
@jwt_required(Admin)
def update_offering_action():
    pass
'''

# 04 : List All Offerings
@admin_views.route('/listAllOfferings', methods=['GET'])
@jwt_required(Admin)
def list_all_offerings_action():
    try:
        course_offerings = get_all_offerings()

        if "Error" in course_offerings:
            return jsonify(error=course_offerings["Error"]), 500
        elif "Message" in course_offerings:
            return jsonify(message=course_offerings["Message"]), 404

        return jsonify(course_offerings), 200

    except Exception as e:
        print(f"Error While Fetching All Offerings: {e}")
        return jsonify(error="An Error Occurred While Listing All Course Offerings"), 500

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