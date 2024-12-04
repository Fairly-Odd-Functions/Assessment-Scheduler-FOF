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
Course [6]
Written By: Katoya Ottley
Task: 10.3.1. Implement API Views for Admin (Course)
"""

# 01 : Add Course *
@admin_views.route('/addCourse', methods=['POST'])
@jwt_required(Admin)
def add_course_action():
    try:
        data = request.get_json()
        courseCode = data.get("courseCode")
        courseTitle = data.get("courseTitle")
        courseCredits = data.get("courseCredits")
        courseDescription = data.get("courseDescription")
        courseLevel = data.get("courseLevel")

        if not courseCode or not courseTitle or not courseCredits or not courseDescription or not courseLevel:
            return jsonify(error= "All Fields are Required To Add Course", data=data), 400

        newCourse = add_course(courseCode, courseTitle, courseCredits, courseDescription, courseLevel)
        if newCourse is None:
            return jsonify(error = "Failed To Add Course or Course Already Exists.", data=data), 400

        message = f'Course: {newCourse.courseCode} - {newCourse.courseTitle} Added Successfully!'
        return jsonify(message=message, data= {
                                                    "courseCode": newCourse.courseCode,
                                                    "courseTitle": newCourse.courseTitle,
                                                    "courseCredits": newCourse.courseCredits,
                                                    "courseDescription": newCourse.courseDescription,
                                                    "courseLevel": newCourse.courseLevel
                                                }), 201
    
    except Exception as e:
        print (f"Error While Adding Course: {e}")
        return jsonify(error = "An Error Occurred While Adding Course", exception=str(e)), 500


# 02 : Update Course *
@admin_views.route('/updateCourse', methods=['PUT'])
@jwt_required(Admin)
def update_course_action():
    try:
        data = request.get_json()
        courseCode = data.get("courseCode")
        new_courseTitle = data.get("new_courseTitle")
        new_courseCredits = data.get("new_courseCredits")
        new_courseDescription = data.get("new_courseDescription")
        new_courseLevel = data.get("new_courseLevel")

        #if not is_valid_course_code(courseCode):
        #    return jsonify(error = "Invalid Course Code, Please Try Again"), 400
        
        updatedCourse = edit_course(courseCode, new_courseTitle=None, new_courseCredits=None, new_courseDescription=None, new_courseLevel=None)
        if updatedCourse is None:
            return jsonify(error = "Failed To Update Course or Course Does Not Exists."), 400

        message = f'Course: {updatedCourse.courseCode} - {updatedCourse.new_courseTitle} Updated Successfully!'
        return jsonify(message=message), 201
    
    except Exception as e:
        print (f"Error While Updating Course: {e}")
        return jsonify(error = "An Error Occurred While Updating Course"), 500

# 03 : Get Course By Code*
@admin_views.route('/search/<str:courseCode>', methods=['GET'])
@jwt_required(Admin)
def search_course_action(courseCode):
    try:
        #if not is_valid_course_code(courseCode):
        #    return jsonify(error = "Invaild Course Code, Please Try Again."), 400
        
        course = get_course_by_code(courseCode)
        if not course:
            return jsonify(error= f"Course With ID: {courseCode} Not Found"), 404
        
        return jsonify(course), 200
    
    except Exception as e:
        return jsonify(error = f"An Error Occurred While Searching for Course With Code: {courseCode}"), 500

# 04 : List All Courses*
@admin_views.route('listCourses', methods=['GET'])
@jwt_required(Admin)
def list_course_action():
    try:
        
        courseList = list_courses()
        return jsonify(courseList), 200

    except Exception as e:
        return jsonify(error = f"An Error Occurred While Listing Courses"), 500

# 05 : Assign A Staff to A Course *
@admin_views.route('/addStaff', methods=['POST'])
@jwt_required(Admin)
def add_course_staff_action():
    try:
        data = request.get_json()
        courseCode = data.get("courseCode")
        semesterName = data.get("semesterName")
        academicYear = data.get("academicYear")
        staffID = data.get("staffID")
        
        if not courseCode or not semesterName or not academicYear or not staffID:
            return jsonify(error= "All Fields are Required To Assign Staff to Course"), 400

        #if not is_valid_staff_id(staffID):
        #    return jsonify(error = "Invalid Staff ID, Please Try Again."), 400

        newStaff =  add_course_staff(courseCode, semesterName, academicYear, staffID)
        if newStaff is None:
            return jsonify(error = "Failed To Add Staff To The Course or Staff Already Assigned to That Course."), 400

        message = f'Staff: {newStaff.staffID} Assigned to {courseCode} for Academic Year {academicYear}, Semester {semesterName} Added Successfully!'
        return jsonify(message=message), 201
    
    except Exception as e:
        print (f"Error While Assigning Staff To Course: {e}")
        return jsonify(error = "An Error Occurred While Assigning Staff To Course"), 500
    
# 06 : Remove A Staff from A Course *
@admin_views.route('/removeStaff', methods=['DELETE'])
@jwt_required(Admin)
def add_course_staff_action():
    try:
        data = request.get_json()
        courseCode = data.get("courseCode")
        semesterName = data.get("semesterName")
        academicYear = data.get("academicYear")
        staffID = data.get("staffID")
        
        if not courseCode or not semesterName or not academicYear or not staffID:
            return jsonify(error= "All Fields are Required To Remove Staff From A Course"), 400

        #if not is_valid_staff_id(staffID):
        #    return jsonify(error = "Invalid Staff ID, Please Try Again."), 400

        removeStaff =  remove_course_staff(courseCode, semesterName, academicYear, staffID)
        if removeStaff is None:
            return jsonify(error = "Failed To Remove Staff From Course or Staff Is Not Assigned to That Course."), 400

        message = f'Staff: {removeStaff.staffID} From {courseCode} for Academic Year {academicYear}, Semester {semesterName} Removed Successfully!'
        return jsonify(message=message), 201
    
    except Exception as e:
        print (f"Error While Removing Staff From Course: {e}")
        return jsonify(error = "An Error Occurred While Removing Staff From Course"), 500

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