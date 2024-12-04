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
Written By Daniel Young
"""

# 01 : Add Semester *
@admin_views.route('/addSemester', methods=['POST'])
@jwt_required(Admin)
def add_semester_action():
    try:
        data = request.json
        semesterName = data['semesterName']
        academicYear = data['academicYear']
        startDate = data['startDate']
        endDate = data['endDate']
        response = add_semester(semesterName, academicYear, startDate, endDate)
        if "Error Message" in response:
            return jsonify({"message" : response['Error Message']}),400
        else:
            return jsonify(response),201
    except Exception as e:
        return jsonify(error=f'An Error Occurred While trying to add semester'), 500

# 02 : Update Semester
@admin_views.route('/updateSemester', methods=['POST'])
@jwt_required(Admin)
def update_semester_action():
    try:
        data = request.get_json()
        semesterName = data.get("semesterName")
        academicYear = data.get("academicYear")
        new_semesterName = data.get("new_semesterName")
        new_academicYear = data.get("new_academicYear")
        startDate = data.get("startDate")
        endDate = data.get("endDate")
        response = update_semester(semesterName, academicYear, new_semesterName=None, new_academicYear=None, startDate=None, endDate=None)
        if "Error Message" in response:
            return jsonify({"message" : response['Error Message']}),400
        else:
            return jsonify(response),201
    except Exception as e:
        return jsonify(error=f'An Error Occurred While trying to update semester'), 500

# 09 : Search Semester
@admin_views.route('/searchSemester', methods=['GET'])
@jwt_required(Admin)
def search_semester_action():
    # try:
        data = request.get_json()
        semesterName = data.get("semesterName")
        academicYear = data.get("academicYear")
        response = get_semester(semesterName, academicYear)
        if "Error Message" in response:
            return jsonify({"message" : response['Error Message']}),400
        else:
            message=f'{response.semesterName} retrieved'
            return jsonify(message=message),201
    # except Exception as e:
        # return jsonify(error=f'An Error Occurred While trying to find semester'), 500

# 10 : List Semesters
@admin_views.route('/listSemesters', methods=['GET'])
@jwt_required(Admin)
def list_semesters_action():
    try:
        response = list_semesters()
        if "Error Message" in response:
            return jsonify({"message" : response['Error Message']}),400
        else:
            return jsonify(response),201
    except Exception as e:
        return jsonify(error=f'An Error Occurred While trying to list semesters'), 500


# 11 : List Semester Courses
@admin_views.route('/listSemesterCourses', methods=['GET'])
@jwt_required(Admin)
def list_semester_courses_action():
    try:
        data = request.get_json()
        semesterName = data.get("semesterName")
        academicYear = data.get("academicYear")
        response = list_courses_for_semester(semesterName, academicYear)
        if "Error Message" in response:
            return jsonify({"message" : response['Error Message']}),400
        else:
            return jsonify(response),201
    except Exception as e:
        return jsonify(error=f'An Error Occurred While trying to list Courses for the semesters'), 500

@admin_views.route('/getSemesterByAcademicYear', methods=['GET'])
@jwt_required(Admin)
def get_semester_by_academic_year():
    try:
        data = request.get_json()
        academicYear = data.get("academicYear")
        response = get_semesters_by_academic_year(academicYear)
        if "Error Message" in response:
            return jsonify({"message" : response['Error Message']}),400
        else:
            return jsonify(response),201
    except Exception as e:
        return jsonify(error=f'An Error Occurred While trying to Semesters or an academic year'), 500



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
    programmeTitle = data['programmeTitle']
    new_title = data['new_title']
    new_description = data['new_description']

    response = update_programme(programmeTitle, new_title=None, new_description=None)
    if "Error Message" in response:
        return jsonify({"message" : response["Error Message"]}), 400
    if "Programme" in response:
        return jsonify({"message" : reponse['Message'],
                    "Programme": response['Programme']
        }),201
    return jsonify({"message":"An unknown error occorred"}),500
                    

# 05 : Get Programme Course
@admin_views.route('/getProgrammeCourse', methods=['GET'])
@jwt_required(Admin)
def get_programme_course_action():
    
    data = request.json
    programmeID = data['programmeID']
    
    response = get_course_programme(programmeID)
    if "Error" in response:
        return jsonify ({"message" : response["Error"]}),400
    if "Message" in response:
        return jsonify ({"message" : response['Message']}),404
    if "CourseProgrammes" in response:
        return jsonify({"CourseProgrammes":response["CourseProgrammes"]}),201
    return jsonify({"message":"An unknown error occured"}),500

# 07 : List Programmes
@admin_views.route('/listProgrammes', methods=['GET'])
@jwt_required(Admin)
def list_programmes_action():
    try :
        response = list_programmes()
        if "Error Message" in response:
            return jsonify ({"message" : response['Error Message']}),400
        if "Message" in rsponse:
            return jsonify ({"message" : response['Message']}),404
        return jsonify(response),201
    except Exeption as e:
         return jsonify(error=f'An Error Occurred While Searching For Programmes'), 500

    
# 08 : List Programme Courses
@admin_views.route('/listProgrammeCourses', methods=['GET'])
@jwt_required(Admin)
def list_programme_courses_action():
    try:
        data = request.json
        programmeTitle = data['programmeTitle']

        response = list_programme_courses(programmeTitle)
        if "Error Message" in response:
            return jsonify ({"message" : response['Error Message']}), 400
        else:
            return jsonify(response), 201
    except Exception as e:
        return jsonify(error=f'An Error Occurred While Searching For Programmes Courses'), 500
   

# 08 : Programme by ID
@admin_views.route('/getProgrammeByID<int:programmeID>', methods=['GET'])
@jwt_required(Admin)
def get_programme_by_id_action(programmeID):
    try:
        data = request.json
        programmeID = data['programmeID']

        response = get_programme_by_id(programmeID)
        if response is None:
            return jsonify (error=f"No programme found with ID:{programmeID} "), 404
        else:
            return jsonify(response), 201
    except Exception as e:
        return jsonify(error=f'An Error Occurred While Searching For Programmes Courses'), 500


# 08 : Programme by title
@admin_views.route('/getProgrammeByTitle<string:programmeTitle>', methods=['GET'])
@jwt_required(Admin)
def get_programme_by_title_action(programmeTitle):
    try:
        data = request.json
        programmeTitle = data['programmeTitle']

        response = get_programme_by_title(programmeTitle)
        if "Error Message" in response:
            return jsonify ({"message" : response['Error Message']}), 400
        else:
            return jsonify(response), 201
    except Exception as e:
        return jsonify(error=f'An Error Occurred While Searching For Programmes Courses'), 500
