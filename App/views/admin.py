import os, csv
from App.controllers import *
from App.database import db
from App.models import Admin
from datetime import datetime
from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required
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
Course [4]
Written By: Katoya Ottley

Task Re-Assigned:
Written By: Jalene Armstrong (JaleneA) - Task: 10.3.1. Implement API Views for Admin (Course)
"""

# 01 : Add Course
@admin_views.route('/addCourse', methods=['POST'])
@jwt_required(Admin)
def add_course_action():
    try:
        data = request.get_json()
        courseCode = data["courseCode"]
        courseTitle = data["courseTitle"]
        courseCredits = data["courseCredits"]
        courseDescription = data["courseDescription"]
        courseLevel = data["courseLevel"]

        if not courseCode or not courseTitle or not courseCredits or not courseDescription or not courseLevel:
            return jsonify(error= "All Fields are Required To Add Course"), 400

        result = add_course(courseCode=courseCode, 
                               courseTitle=courseTitle,
                               courseCredits=courseCredits,
                               courseDescription=courseDescription,
                               courseLevel=courseLevel)
        if "Error" in result:
            return jsonify(error=result["Error"]), 400
        
        if "Message" in result and "Course" in result:
            course = result["Course"]
            return jsonify(message=result["Message"], course=course), 201
        return jsonify(error="Unexpected Error Ocurrred While Adding The Course"), 500

    except Exception as e:
        print (f"Error While Adding Course: {e}")
        return jsonify(error = "An Error Occurred While Adding Course"), 500

# 02 : Update Course
@admin_views.route('/updateCourse/<string:courseCode>', methods=['PUT'])
@jwt_required(Admin)
def update_course_action(courseCode):
    try:
        data = request.get_json()

        new_courseTitle = data["courseTitle"]
        new_courseCredits = data["courseCredits"]
        new_courseDescription = data["courseDescription"]
        new_courseLevel = data["courseLevel"]

        if not any([new_courseTitle, new_courseCredits, new_courseDescription, new_courseLevel]):
            return jsonify(error="At Least One Field Is Required To Update The Course"), 400

        result = edit_course(
            courseCode,
            new_courseTitle=new_courseTitle,
            new_courseCredits=new_courseCredits,
            new_courseDescription=new_courseDescription,
            new_courseLevel=new_courseLevel)

        if "Error" in result:
            return jsonify(error=result["Error"]), 400
        
        updated_course = result["Course"]
        return jsonify(
            message=f'Course: {updated_course["courseCode"]} - {updated_course["courseTitle"]} Updated Successfully!',
            course=updated_course
        ), 200
       
    except Exception as e:
        print (f"Error While Updating Course: {e}")
        return jsonify(error = "An Error Occurred While Updating Course"), 500

# 03 : Get Course By Code
@admin_views.route('/searchCourse/<string:courseCode>', methods=['GET'])
@jwt_required(Admin)
def search_course_action(courseCode):
    try:
        course = get_course(courseCode)
        if isinstance(course, dict) and "Error" in course:
            return jsonify(error=course["Error"]), 404
        
        return jsonify(course.get_json()), 200
    
    except Exception as e:
        print(f"DEBUG: {e}")
        return jsonify(error = f"An Error Occurred While Searching for Course With Code: {courseCode}"), 500

# 04 : List All Courses
@admin_views.route('/listCourses', methods=['GET'])
@jwt_required(Admin)
def list_course_action():
    try:
        courseList = list_courses()
        return jsonify(courseList), 200
    except Exception as e:
        print(f"DEBUG: {e}")
        return jsonify(error = f"An Error Occurred While Listing Courses"), 500

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
ProgrammeCourse [4]
Written By Daniel Young
"""
@admin_views.route('/addProgrammeCourse', methods=['POST'])
@jwt_required(Admin)
def add_programme_course_action():
    data = request.json
    courseCode = data['courseCode']
    programmeID = data['programmeID']

    response = add_course_to_programme(courseCode, programmeID)
    if "Error" in response:
        return jsonify ({"message" : response["Error"]}),400

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
    if "Error" in response:
        return jsonify ({"message" : response["Error"]}),400
    if "Message" in response:
        return jsonify({
            "message" : response["Message"]
        }),201
    return jsonify({"message":"Unable to delete"}), 500

# 03 : Get Course Degree Programme
@admin_views.route("/courseProgramme/<string:courseCode>", methods=["GET"])
@jwt_required(Admin)
def get_course_programme_action(courseCode):
    try: 
        course_programme = get_degree_programme(courseCode)
        if course_programme is None:
            return jsonify(error=f'Course with ID:{courseCode} Not enlisted in Programme'),404
        return jsonify(course_programme),200
    except Exception as e:
        return jsonify(error=f'An Error Occurred While Searching For Course With ID: {courseCode}'), 500

# 04 : List Programme Courses
@admin_views.route('/listProgrammeCourses', methods=['GET'])
@jwt_required(Admin)
def list_programme_courses_action():
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

"""
CourseOffering [4]
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

# # 05 : Assign A Staff to A Course *
# @admin_views.route('/addCourseStaff', methods=['POST'])
# @jwt_required(Admin)
# def add_course_staff_action():
#     try:
#         data = request.get_json()
#         courseCode = data.get("courseCode")
#         semesterName = data.get("semesterName")
#         academicYear = data.get("academicYear")
#         staffID = data.get("staffID")
        
#         if not courseCode or not semesterName or not academicYear or not staffID:
#             return jsonify(error= "All Fields are Required To Assign Staff to Course"), 400

#         #if not is_valid_staff_id(staffID):
#         #    return jsonify(error = "Invalid Staff ID, Please Try Again."), 400

#         newStaff =  add_course_staff(courseCode, semesterName, academicYear, staffID)
#         if newStaff is None:
#             return jsonify(error = "Failed To Add Staff To The Course or Staff Already Assigned to That Course."), 400

#         message = f'Staff: {newStaff.staffID} Assigned to {courseCode} for Academic Year {academicYear}, Semester {semesterName} Added Successfully!'
#         return jsonify(message=message), 201
    
#     except Exception as e:
#         print (f"Error While Assigning Staff To Course: {e}")
#         return jsonify(error = "An Error Occurred While Assigning Staff To Course"), 500
    
# # 06 : Remove A Staff from A Course *
# @admin_views.route('/removeCourseStaff', methods=['DELETE'])
# @jwt_required(Admin)
# def remove_course_staff_action():
#     try:
#         data = request.get_json()
#         courseCode = data.get("courseCode")
#         semesterName = data.get("semesterName")
#         academicYear = data.get("academicYear")
#         staffID = data.get("staffID")
        
#         if not courseCode or not semesterName or not academicYear or not staffID:
#             return jsonify(error= "All Fields are Required To Remove Staff From A Course"), 400

#         #if not is_valid_staff_id(staffID):
#         #    return jsonify(error = "Invalid Staff ID, Please Try Again."), 400

#         removeStaff =  remove_course_staff(courseCode, semesterName, academicYear, staffID)
#         if removeStaff is None:
#             return jsonify(error = "Failed To Remove Staff From Course or Staff Is Not Assigned to That Course."), 400

#         message = f'Staff: {removeStaff.staffID} From {courseCode} for Academic Year {academicYear}, Semester {semesterName} Removed Successfully!'
#         return jsonify(message=message), 201
    
#     except Exception as e:
#         print (f"Error While Removing Staff From Course: {e}")
#         return jsonify(error = "An Error Occurred While Removing Staff From Course"), 500

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
            "message" : response["Message"],
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
    data = request.get_json()
    programmeTitle = data.get("programmeTitle")
    new_title = data.get("new_title")
    new_description = data.get("new_description")

    response = update_programme(programmeTitle, new_title=None, new_description=None)
    if "Error Message" in response:
        return jsonify({"message" : response["Error Message"]}), 400
    if "Programme" in response:
        return jsonify({"message" : response['Message'],
                    "Programme": response['Programme']
        }),201
    return jsonify({"message":"An unknown error occorred"}),500
                    

# 05 : Get Programme Course
@admin_views.route('/getProgrammeCourse', methods=['GET'])
@jwt_required(Admin)
def get_programme_course_action():
    
    data = request.get_json()
    programmeID = data.get("programmeID")
    
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
        if "Message" in response:
            return jsonify ({"message" : response['Message']}),404
        return jsonify(response),201
    except Exception as e:
         return jsonify(error=f'An Error Occurred While Searching For Programmes'), 500

    
# 08 : List Programme Courses
@admin_views.route('/listProgrammeCourses', methods=['GET'])
@jwt_required(Admin)
def list_programme_courses_action():
    try:
        data = request.get_json
        programmeTitle = data.get("programmeTitle")

        response = list_programme_courses(programmeTitle)
        if "Error Message" in response:
            return jsonify ({"message" : response['Error Message']}), 400
        else:
            return jsonify(response), 201
    except Exception as e:
        return jsonify(error=f'An Error Occurred While Searching For Programmes Courses'), 500
   

# 08 : Programme by ID
@admin_views.route('/getProgrammeByID/<int:programmeID>', methods=['GET'])
@jwt_required(Admin)
def get_programme_by_id_action(programmeID):
    try:
        
        response = get_programme_by_id(programmeID)
        if response is None:
            return jsonify (error=f"No programme found with ID:{programmeID} "), 404
        else:
            return jsonify(response), 201
    except Exception as e:
        return jsonify(error=f'An Error Occurred While Searching For Programmes Courses'), 500


# 08 : Programme by title
@admin_views.route('/getProgrammeByTitle/<string:programmeTitle>', methods=['GET'])
@jwt_required(Admin)
def get_programme_by_title_action(programmeTitle):
    try:
        # data = request.json
        # programmeTitle = data['programmeTitle']

        response = get_programme_by_title(programmeTitle)
        if "Error Message" in response:
            return jsonify ({"message" : response['Error Message']}), 400
        else:
            return jsonify(response), 201
    except Exception as e:
        return jsonify(error=f'An Error Occurred While Searching For Programmes Courses'), 500
