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
Course [3]
Written By Rynnia Ryan (Rynnia.R) - Task 10.3.4. Implement API Views for Admin (CourseStaff)
"""

# 01 : Add Course Staff - My idea is that when on view of a course you can add a staff member hence course code
@admin_views.route('/addCourseStaff/<int:courseCode>', methods=['POST'])
@jwt_required(Admin)
def add_course_staff_action(courseCode):

    staffEmail = request.form.get('staffEmail')
    semesterName = request.form.get('semesterName')
    academicYear = request.form.get('academicYear')

    staff = get_staff_by_email(staffEmail)
    if staff is None:
        return jsonify(error="Staff member not found"), 404

    if staffEmail:
        result = add_course_staff(courseCode, semesterName, academicYear, staff.staffID)
        
        if result["Error"]:
            return jsonify(result), 400
        
        elif result["Message"]:
            return jsonify(result), 201
        
        else:
            return jsonify(result), 500

    else:
        return jsonify(error="Please provide all required fields"), 400


# 02 : Add Multiple Course to a Staff
@admin_views.route('/addMultipleCourseStaff', methods=['POST'])
@jwt_required(Admin)
def add_multiple_courses_to_staff_action():

    #Getting CSv file from the request
    file = request.files['file']

    if not file:
        return jsonify(error="Please Upload a CSV File"), 400
    
    staffEmail = request.form.get('staffEmail')
    if not staffEmail:
        return jsonify(error="Please provide staff email"), 400

    staff = get_staff_by_email(staffEmail)
    if staff is None:
        return jsonify(error="Staff Member Not Found"), 404

    #Reading CSV file, splitting it into lines and saving each line into a list
    csv_data = file.read().decode('utf-8')
    lines = csv_data.splitlines()
    course_codes = []

    for line in lines:
        columns = line.split(',')
        course_code = columns[0] #Getting the course code from the first column
        course_codes.append(course_code)

    result = add_multiple_courses_to_staff(staffEmail, course_codes)

    if result["Error"]:
        return jsonify(result), 400

    elif result["Message"]:
        return jsonify(result), 201

    else:
        return jsonify(result), 500

# 03 : Remove Course Staff
@admin_views.route('/removeCourseStaff/<int:courseCode>', methods=['POST'])
@jwt_required(Admin)
def remove_course_staff_action(courseCode):
    staffEmail = request.form.get('staffEmail')
    semesterName = request.form.get('semesterName')
    academicYear = request.form.get('academicYear')

    staff = get_staff_by_email(staffEmail)
    if staff is None:
        return jsonify(error="Staff Member Not Found."), 404
    
    result = remove_course_staff(courseCode, semesterName, academicYear, staff.staffID)

    if result["Error"]:
        return jsonify(result), 400

    elif result["Message"]:
        return jsonify(result), 200

    else:
        return jsonify(result), 500




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
Written ByKatoya Ottley
Task: 10.3.4. Implement API Views for Admin (CourseStaff)
"""
# 01 : Assign a Staff to Multiple Courses *
@admin_views.route('/addStaff', methods=['POST'])
@jwt_required(Admin)
def add_courses_to_staff_action():
    try:
        data = request.get_json()
        staffEmail = data.get("staffEmail")
        courseCodes = data.get("courseCodes")
        
        if not staffEmail or not courseCodes :
            return jsonify(error= "All Fields are Required To Assign Staff to Courses"), 400

        #if not is_valid_staff_id(staffID):
        #    return jsonify(error = "Invalid Staff ID, Please Try Again."), 400

        newStaff =  add_multiple_courses_to_staff(staffEmail, courseCodes)
        if newStaff is None:
            return jsonify(error = "Failed To Add Staff To The Course or Staff Already Assigned to Those Courses."), 400

        message = f'Staff: {newStaff.staffID} Assigned to {courseCodes} Successfully!'
        return jsonify(message=message), 201
    
    except Exception as e:
        print (f"Error While Assigning Staff To Courses: {e}")
        return jsonify(error = "An Error Occurred While Assigning Staff To Courses"), 500
    

''' Present In Admin (Course)
# 01 : Add Course Staff
@admin_views.route('/addCourseStaff', methods=['POST'])
@jwt_required(Admin)
def add_course_staff_action():
    pass
'''

'''' Present In Admin (Course)
# 02 : Remove Course Staff
@admin_views.route('/removeCourseStaff', methods=['POST'])
@jwt_required(Admin)
def remove_course_staff_action():
    pass
'''

''' Present In Admin (Course)
# 03 : Update Course Staff
@admin_views.route('/updateCourseStaff', methods=['POST'])
@jwt_required(Admin)
def update_course_staff_action():
    pass
'''

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