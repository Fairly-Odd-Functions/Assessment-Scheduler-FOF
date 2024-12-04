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
    data = request.get_json()
    firstName = data['firstName']
    lastName = data['lastName']
    email = data['email']
    password = data['password']

    result = register_staff(firstName, lastName, password, email)

    if result is None:
        return jsonify(error = "Staff with this email or password already exists"), 400
    
    if isinstance(result, dict):
        return jsonify(error = result["error"]), 400
    
    if result:
        return jsonify(result.get_json()), 201

    return jsonify(error = "An unknown error occurred"), 500
    
# 02 : Create Admin
@admin_views.route('/createAdmin', methods=['POST'])
@jwt_required(Admin)
def create_admin_action():
    data = request.get_json()
    firstName = data['firstName']
    lastName = data['lastName']
    email = data['email']
    password = data['password']

    result = create_admin(firstName=firstName,
                          lastName=lastName,
                          password=password,
                          email=email)

    if result is None:
        return jsonify(error = "Admin with this email already exists"), 400
    
    if result:
        response_json = result.get_json()
        return jsonify(message = "Admin Created Successfully!", admin=response_json), 201

    return jsonify(error = "An unknown error occurred"), 500

# 03 : Get All Staff Users
@admin_views.route('/allStaff', methods=['GET'])
@jwt_required(Admin)
def list_all_staff_action():
    allStaff = get_all_staff()

    if not allStaff:
        return jsonify(error = "No Staff Found."), 404

    allStaff = [staff.get_json() for staff in allStaff]
    return jsonify(allStaff), 200

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
@admin_views.route('/updateStaff/<string:staffEmail>', methods=['PUT'])
@jwt_required(Admin)
def update_staff_action(staffEmail):
    data = request.get_json()
    new_firstName = data['firstName']
    new_lastName = data['lastName']
    new_email = data['email']
    new_password = data['password']

    result = update_staff(staffEmail=staffEmail,
                          firstName=new_firstName,
                          lastName=new_lastName,
                          password=new_password,
                          email=new_email)

    if isinstance(result, dict) and "error" in result:
        return jsonify(error=result["error"]), 400
    
    if isinstance(result, Staff):
        response_json = result.get_json()
        return jsonify(message="Staff Member Updated Successfully!", staff=response_json), 200

    return jsonify(error="An unknown error occurred"), 500

# 06 : Remove Admin
@admin_views.route('/removeAdmin/<string:adminEmail>', methods=['DELETE'])
@jwt_required(Admin)
def remove_admin_action(adminEmail):
    admin = Admin.query.filter_by(email=adminEmail).first()

    if not admin:
        return jsonify(error = "No Admin Found."), 404

    result = delete_admin(adminEmail)

    if isinstance(result, dict) and "error" in result:
        return jsonify(error=result["error"]), 400

    if result is not None:
        return jsonify(message="Admin deleted successfully"), 200

    return jsonify(error="An unknown error occurred"), 500

# 07 : Update Admin
@admin_views.route('/updateAdmin/<string:adminEmail>', methods=['PUT'])
@jwt_required(Admin)
def update_admin_action(adminEmail):
    try:
        data = request.get_json()
        new_firstName = data['firstName']
        new_lastName = data['lastName']
        new_email = data['email']
        new_password = data['password']

        result = update_admin(adminEmail=adminEmail,
                              firstName=new_firstName,
                              lastName=new_lastName,
                              password=new_password,
                              email=new_email)

        if isinstance(result, dict) and "error" in result:
            return jsonify(error=result["error"]), 400

        if isinstance(result, Admin):
            response_json = result.get_json()
            return jsonify(message="Admin Member Updated Successfully!", admin=response_json), 200

        return jsonify(error="An unknown error occurred"), 500

    except Exception as e:
        print(f"Error occurred while updating admin: {e}")
        return jsonify(error="An error occurred while updating the admin"), 500

# 08 : Remove Staff
@admin_views.route('/removeStaff/<string:staffEmail>', methods=['DELETE'])
@jwt_required(Admin)
def remove_staff_action(staffEmail):
    try:
        result = delete_staff(staffEmail)

        if "Error" in result:
            return jsonify(error = result), 400

        if "Staff member deleted successfully" in result:
            return jsonify(message = result), 200

        return jsonify(error = "An unknown error occurred"), 500
    except Exception as e:
            print(f"{e}")
            return jsonify(error="An error occurred while updating the admin"), 500

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

# 05 : Get Course Degree Programme
# Written By Daniel
@admin_views.route("/getCourseProgramme/<string:courseCode>", methods=["GET"])
@jwt_required(Admin)
def get_course_programme_action(courseCode):
    try: 
        course_programme = get_degree_programme(courseCode)
        if course_programme is None:
            return jsonify(error=f'Course with ID:{courseCode} Not enlisted in Programme'),404
        return jsonify(course_programme.get_json()),200
    except Exception as e:
        print(f"{e}")
        return jsonify(error=f'An Error Occurred While Searching For Course With ID: {courseCode}'), 500

"""
Semester [2]
Written By Daniel Young
"""

# 01 : Add Semester *
@admin_views.route('/addSemester', methods=['POST'])
@jwt_required(Admin)
def add_semester_action():
    try:
        data = request.get_json()
        semesterName = data['semesterName']
        academicYear = data['academicYear']
        startDate = data['startDate']
        endDate = data['endDate']

        start_date = datetime.strptime(startDate, "%Y-%m-%d").date()
        end_date = datetime.strptime(endDate, "%Y-%m-%d").date()

        response = add_semester(semesterName=semesterName,
                                academicYear=academicYear,
                                startDate=start_date,
                                endDate=end_date)

        if "Error Message" in response:
            return jsonify({"message" : response['Error Message']}),400
        else:
            return jsonify(response),201
    except Exception as e:
        return jsonify(error=f'An Error Occurred While trying to add semester'), 500

# 02 : Update Semester
@admin_views.route('/updateSemester/<int:semesterID>', methods=['PUT'])
@jwt_required(Admin)
def update_semester_action(semesterID):
    try:
        data = request.get_json()
        new_semesterName = data.get("new_semesterName")
        new_academicYear = data.get("new_academicYear")
        startDate = data.get("startDate")
        endDate = data.get("endDate")

        start_date = datetime.strptime(startDate, "%Y-%m-%d").date()
        end_date = datetime.strptime(endDate, "%Y-%m-%d").date()

        response = update_semester(semester_id=semesterID,
                                   new_semesterName=new_semesterName,
                                   new_academicYear=new_academicYear,
                                   startDate=start_date,
                                   endDate=end_date)
        if "Error Message" in response:
            return jsonify({"message": response['Error Message']}), 400
        else:
            semester_data = response.get("Semester Updated", {})
            if semester_data:
                return jsonify({"Semester Updated": semester_data.get_json()}), 200
            else:
                return jsonify(error="Failed to update semester"), 500
    
    except Exception as e:
        print(f"{e}")
        return jsonify(error=f'An Error Occurred While trying to update semester'), 500

# 09 : Search Semester
@admin_views.route('/searchSemester/<int:semesterID>', methods=['GET'])
@jwt_required(Admin)
def search_semester_action(semesterID):
    try:
        response = get_semester_by_id(semesterID)

        if response is None:
            return jsonify({"message": f"Semester with ID {semesterID} not found"}), 404
        else:
            return jsonify(response.get_json()), 200
    except Exception as e:
        print(f"{e}")
        return jsonify(error=f'An Error Occurred While Trying To Find Semester'), 500

# 10 : List Semesters
@admin_views.route('/listSemesters', methods=['GET'])
@jwt_required(Admin)
def list_semesters_action():
    try:
        response = list_semesters_json()
        if "Error Message" in response:
            return jsonify({"message" : response['Error Message']}), 400
        else:
            return jsonify(response), 200
    except Exception as e:
        print(f"{e}")
        return jsonify(error=f'An Error Occurred While trying to list semesters'), 500

# 11 : List Semester Courses
@admin_views.route('/listSemesterCourses/<int:semesterID>', methods=['GET'])
@jwt_required(Admin)
def list_semester_courses_action(semesterID):
    try:
        course_offerings =  list_courses_for_semester(semesterID=semesterID)
        if "Error Message" in course_offerings:
            return jsonify({"message" : course_offerings['Error Message']}),400
        else:
            courses_data = [course.get_json() for course in course_offerings]
            return jsonify(courses_data), 200
    except Exception as e:
        print(f"{e}")
        return jsonify(error=f'An Error Occurred While trying to list Courses for the semesters'), 500

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
@admin_views.route('/removeProgrammeCourse', methods=['DELETE'])
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

# 03 : List Programme Courses
@admin_views.route('/listProgrammeCourses/<int:programmeID>', methods=['GET'])
@jwt_required(Admin)
def list_programme_courses_action(programmeID):
    response = get_course_programme(programmeID)
    if "Error" in response:
        return jsonify ({"message" : response["Error"]}), 400
    if "Message" in response:
        return jsonify ({"message" : response['Message']}), 404
    if "CourseProgrammes" in response:
        return jsonify({"CourseProgrammes":response["CourseProgrammes"]}), 200
    return jsonify({"message":"An unknown error occured"}), 500

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
Written By Rynnia Ryan (Rynnia.R) - Task 10.3.4. Implement API Views for Admin (CourseStaff)
"""

# 01 : Add Course Staff - My idea is that when on view of a course you can add a staff member hence course code
@admin_views.route('/addCourseStaff/<string:courseCode>', methods=['POST'])
@jwt_required(Admin)
def add_course_staff_action(courseCode):
    try:
        data = request.get_json()
        staffEmail = data['staffEmail']
        semesterName = data['semesterName']
        academicYear = data['academicYear']

        staff = get_staff_by_email(staffEmail)
        if staff is None:
            return jsonify(error="Staff Member Not Found"), 404

        if staffEmail:
            result = add_course_staff(courseCode, semesterName, academicYear, staff.userID)
            print(result)

            if "Error" in result:
                print(f"Error Response: {result['Error']}")
                return jsonify(result), 400
            
            elif "Message" in result:
                return jsonify(result), 201
            
            else:
                return jsonify({"error": "Unknown response structure"}), 500

        else:
            return jsonify(error="Please provide all required fields"), 400
    except Exception as e:
        print(f"Error While Adding Staff To Course: {e}")
        return jsonify(error="An Error Occurred While Assigning Course To Staff"), 500

# 02 : Remove Course Staff
@admin_views.route('/removeCourseStaff/<string:courseCode>', methods=['DELETE'])
@jwt_required(Admin)
def remove_course_staff_action(courseCode):
    try:
        data = request.get_json()
        staffEmail = data['staffEmail']
        semesterName = data['semesterName']
        academicYear = data['academicYear']

        staff = get_staff_by_email(staffEmail)
        if staff is None:
            return jsonify(error="Staff Member Not Found."), 404
        
        result = remove_course_staff(courseCode=courseCode,
                                    semesterName=semesterName,
                                    academicYear=academicYear,
                                    staffID=staff.userID)

        if "Error" in result:
            print(f"Error Response: {result['Error']}")
            return jsonify(result), 400
        
        elif "Message" in result:
            return jsonify(result), 200
        
        else:
            return jsonify({"error": "Unknown response structure"}), 500
    except Exception as e:
            print(f"Error While Adding Staff To Course: {e}")
            return jsonify(error="An Error Occurred While Assigning Course To Staff"), 500
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
        programme_json = response["Programme"].get_json() if hasattr(response["Programme"], 'get_json') else response["Programme"]

        return jsonify({
            "message" : response["Message"],
            "Programme" : programme_json
        }), 201
    return jsonify({"message":"An unknown error occorred"}), 500

# 02 : Remove Programme ****
@admin_views.route('/removeProgramme', methods=['POST'])
@jwt_required(Admin)
def remove_programme_action():
    pass

# 03 : Update Programme
@admin_views.route('/updateProgramme/<int:programmeID>', methods=['PUT'])
@jwt_required(Admin)
def update_programme_action(programmeID):
    data = request.get_json()
    new_title = data['new_title']
    new_description = data['new_description']

    programme = Programme.query.filter_by(programmeID=programmeID).first()
    if not programme:
        return jsonify({"message": f"No Programme Found With ID: {programmeID}"}), 404

    programmeTitle = programme.programmeTitle

    response = update_programme(programmeTitle, new_title=new_title, new_description=new_description)
    if "Error Message" in response:
        return jsonify({"message" : response["Error Message"]}), 400

    if "Programme" in response:
        updated_programme = response["Programme"]
        return jsonify({
            "message": response['Message'],
            "Programme": {
                "programmeID": updated_programme.programmeID,
                "programmeTitle": updated_programme.programmeTitle,
                "programmeDescription": updated_programme.programmeDescription
            }
        }), 201
    return jsonify({"message":"An Unknown Error Occorred"}),500

# 04 : List Programmes
@admin_views.route('/listAllProgrammes', methods=['GET'])
@jwt_required(Admin)
def list_programmes_action():
    try :
        response = list_programmes_json()
        if "Error Message" in response:
            return jsonify ({"message" : response['Error Message']}),400
        if "Message" in response:
            return jsonify ({"message" : response['Message']}),404
        return jsonify(response),201
    except Exception as e:
         print(f"{e}")
         return jsonify(error=f'An Error Occurred While Searching For Programmes'), 500

# 05 : Programme by ID
@admin_views.route('/searchProgramme/<int:programmeID>', methods=['GET'])
@jwt_required(Admin)
def get_programme_by_id_action(programmeID):
    try:
        response = get_programme_by_id(programmeID)
        if response is None:
            return jsonify(error=f"No programme found with ID:{programmeID} "), 404
        else:
            return jsonify(response.get_json()), 200
    except Exception as e:
        print(f"{e}")
        return jsonify(error=f'An Error Occurred While Searching For Programmes Courses'), 500