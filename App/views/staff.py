from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, get_flashed_messages, session
from flask_login import current_user
from flask import current_app as app
from flask_mail import Mail, Message
from sqlalchemy import not_
from App.database import db
import json
from flask_jwt_extended import current_user as jwt_current_user, get_jwt_identity
from flask_jwt_extended import jwt_required
from datetime import date, timedelta
import time
from App.models import *
from App.controllers import *
# IMPORTS TO CLEAN UP

staff_views = Blueprint('staff_views', __name__, template_folder='../templates')

"""
Staff Views
Written By Jalene Armstrong (JaleneA) - Task 10.4. Implement API View For Staff (Main)
"""

# 01 : Create Course Assessment
@staff_views.route('/createAssessment', methods=['POST'])
@jwt_required(Staff)
def create_course_assessment_action():
    data = request.get_json()
    assessmentTitle = data['assessmentTitle']
    assessmentType = data['assessmentType']

    result = create_assessment(
        assessmentTitle=assessmentTitle,
        assessmentType=assessmentType)

    if "Error Message" in result:
        return jsonify({
            "message": result["Error Message"]
        }), 400

    if "Assessment" in result:
        return jsonify({
            "message": result["Message"],
            "CourseAssessment": result["Assessment"]
        }), 201

    return jsonify({
        "message": "An unknown error occurred."
    }), 500

"""
Special Feature - Demonstrated Via Scheduling Assessments
Written By Jalene Armstrong (JaleneA) - Task 10.4. Implement API View For Staff (Main)
"""

# 02 : Schedule A Course Assessment
@staff_views.route('/scheduleAssessment', methods=['POST'])
@jwt_required(Staff)
def schedule_course_assessment_action():
    data = request.get_json()

    courseCode = data['courseCode']
    assessmentID = data['assessmentID']
    startDate = data['startDate']
    startTime = data['startTime']
    endDate = data['endDate']
    endTime = data['endTime']
    clashRule = data['clashRule']

    start_date = datetime.strptime(startDate, "%Y-%m-%d").date()
    end_date = datetime.strptime(endDate, "%Y-%m-%d").date()
    start_time = datetime.strptime(startTime, "%H:%M").time()
    end_time = datetime.strptime(endTime, "%H:%M").time()

    result = add_course_assessment(
        courseCode=courseCode, 
        assessmentID=assessmentID,
        startDate=start_date,
        startTime=start_time,
        endDate=end_date,
        endTime=end_time,
        clashRule=clashRule)

    if "Error" in result:
        return jsonify({"error": result["Error"]}), 400

    if result.get("status") == "error":
        return jsonify(result), 400
    
    return jsonify({
        "message": result["Message"],
        "courseAssessment": result["CourseAssessment"]
    }), 201

# 03 : Delete Assessment
@staff_views.route('/deleteAssessment/<int:courseAssessmentID>', methods=['DELETE'])
@jwt_required(Staff)
def delete_assessment_action(courseAssessmentID):
    result = delete_course_assessment(courseAssessmentID)

    if "Error" in result:
        return jsonify({"error": result["Error"]}), 400
    return jsonify(result), 200

# 04 : Reshedule Assessment
@staff_views.route('/rescheduleAssessment/<int:courseAssessmentID>', methods=['PUT'])
@jwt_required()
def reschedule_assessment_action(courseAssessmentID):
    data = request.get_json()
    newStartDate = data.get('startDate')
    newStartTime = data.get('startTime')
    newEndDate = data.get('endDate')
    newEndTime = data.get('endTime')

    startDate = datetime.strptime(newStartDate, "%Y-%m-%d").date()
    endDate = datetime.strptime(newEndDate, "%Y-%m-%d").date()
    startTime = datetime.strptime(newStartTime, "%H:%M").time()
    endTime = datetime.strptime(newEndTime, "%H:%M").time()

    result = reschedule_course_assessment(courseAssessmentID, newStartDate=startDate, newEndDate=endDate, newStartTime=startTime, newEndTime=endTime)

    if "Error" in result:
        return jsonify({"error": result["Error"]}), 400
    return jsonify(result), 200

# 05 : View Course Schedule
@staff_views.route('/viewCourseSchedule/<string:courseCode>', methods=['GET'])
@jwt_required()
def view_course_schedule_action(courseCode):
    data = request.get_json()
    startDate = data['startDate']
    endDate = data['endDate']

    if not courseCode or not startDate or not endDate:
        return jsonify({"Error": "Missing Required Fields."}), 400

    try:
        start_date = datetime.strptime(startDate, '%Y-%m-%d').date()
        end_date = datetime.strptime(endDate, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({"Error": "Invalid Date Format. Please Use YYYY-MM-DD."}), 400

    result = get_scheduled_assessments(courseCode, start_date, end_date)

    if "Error" in result:
        return jsonify(result), 400

    return jsonify(result), 200

# 06 : Search Scheduled Assessment
@staff_views.route("/searchCourseAssessment/<int:courseAssessmentID>", methods=["GET"])
@jwt_required()
def search_course_assessment_action(courseAssessmentID):
    result = get_course_assessment(courseAssessmentID=courseAssessmentID)

    if "Error" in result:
        return jsonify({"error": result["Error"]}), 400
    return jsonify(result), 200