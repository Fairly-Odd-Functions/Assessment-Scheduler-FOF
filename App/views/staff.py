from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, get_flashed_messages, session
from flask_login import current_user
from flask import current_app as app
from flask_mail import Mail, Message
from sqlalchemy import not_
from App.controllers import Staff
from App.controllers import Course, Semester
from App.controllers import CourseAssessment
from App.controllers.clashDetection import validate_assessment_clash
from App.controllers.courseAssessment import add_course_assessment
from App.database import db
from App.models.assessment import Assessment
import json
from flask_jwt_extended import current_user as jwt_current_user, get_jwt_identity
from flask_jwt_extended import jwt_required
from datetime import date, timedelta
import time
# IMPORTS TO CLEAN UP

staff_views = Blueprint('staff_views', __name__, template_folder='../templates')

# * - PPC [Previous Project's Code :D]

"""
Special Feature - Demonstrated Via Scheduling Assessments
Written By Jalene Armstrong (JaleneA) - Task 10.4. Implement API View For Staff (Main)
"""

# 01 : Schedule A Course Assessment
@staff_views.route('/scheduleAssessment', methods=['POST'])
@jwt_required(Staff)
def schedule_course_assessment_action():
    courseCode = request.form.get('courseCode')
    assessmentID = request.form.get('assessmentID')
    startDate = request.form.get('startDate')
    startTime = request.form.get('startTime')
    endDate = request.form.get('endDate')
    endTime = request.form.get('endTime')
    clashRule = request.form.get('clashRule')

    result = add_course_assessment(courseCode, assessmentID, startDate, startTime, endDate, endTime, clashRule)

    if "Error" in result:
        return jsonify({"error": result["Error"]}), 400

    if result.get("status") == "error":
        return jsonify(result), 400
    
    return jsonify({
        "message": result["Message"],
        "courseAssessment": result["CourseAssessment"]
    }), 201

"""
Assessment
Written By
"""

# 02 : Delete Assessment *
@staff_views.route('/deleteAssessment/<string:courseAssessmentID>', methods=['GET'])
@jwt_required()
def delete_assessment_action(courseAssessmentID):
    # courseAsm = get_CourseAsm_id(caNum) # Gets selected assessment for course
    # delete_CourseAsm(courseAsm)
    # print(caNum, ' deleted')
    # return redirect(url_for('staff_views.get_assessments_page'))
    pass 

# 03 : Update Assessment *
@staff_views.route('/updateAssessment/<int:courseAssessmentID>', methods=['POST'])
@jwt_required()
def update_assessment_action(courseAssessmentID):
    # if request.method=='POST':
    #     #get form details
    #     course = request.form.get('myCourses')
    #     asmType = request.form.get('AssessmentType')
    #     startDate = request.form.get('startDate')
    #     endDate = request.form.get('endDate')
    #     startTime = request.form.get('startTime')
    #     endTime = request.form.get('endTime')

    #     #update record
    #     assessment=get_CourseAsm_id(id)
    #     if assessment:
    #         assessment.a_ID=asmType
    #         if startDate!='' and endDate!='' and startTime!='' and endTime!='':
    #             assessment.startDate=startDate
    #             assessment.endDate=endDate
    #             assessment.startTime=startTime
    #             assessment.endTime=endTime

    #         db.session.commit()

    #         clash=detect_clash(assessment.id)
    #         if clash:
    #             assessment.clashDetected = True
    #             db.session.commit()
    #             flash("Clash detected! The maximum amount of assessments for this level has been exceeded.")
    #             time.sleep(1)

    # return redirect(url_for('staff_views.get_assessments_page'))
    pass

# 04 : View Course Schedule *
@staff_views.route('/courseSchedule', methods=['GET'])
@jwt_required()
def view_course_schedule_action():
    # # Retrieve data from page
    # id = request.form.get('id')
    # startDate = request.form.get('startDate')
    # startTime = request.form.get('startTime')
    # endDate = request.form.get('endDate')
    # endTime = request.form.get('endTime')

    # # Get course assessment
    # assessment=get_CourseAsm_id(id)
    # if assessment:
    #     assessment.startDate=startDate
    #     assessment.endDate=endDate
    #     assessment.startTime=startTime
    #     assessment.endTime=endTime

    #     db.session.commit()
        
    #     clash=detect_clash(assessment.id)
    #     if clash:
    #         assessment.clashDetected = True
    #         db.session.commit()
    #         session['message'] = assessment.courseCode+" - Clash detected! The maximum amount of assessments for this level has been exceeded."
    #     else:
    #         session['message'] = "Assessment modified"
    # return session['message']
    pass

# 05 : Search Scheduled Assessment
@staff_views.route("/searchAssessment", methods=["GET"])
@jwt_required()
def search_assessment_action():
    pass