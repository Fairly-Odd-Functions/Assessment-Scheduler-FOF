from App.database import db
from App.models import Assessment
from App.services.assessment import *

def create_assessment(assessmentTitle, assessmentType, startDate, dueDate):
    try:
        if not assessmentTitle or not assessmentType:
            return {"Error Message": "All Fields Are Required"}

        date_validity = validate_dates(startDate=startDate, dueDate=dueDate)
        if "Error" in date_validity:
            return date_validity

        start_date = date_validity["startDate"]
        due_date = date_validity["dueDate"]

        new_assessment = Assessment(assessmentTitle=assessmentTitle, assessmentType=assessmentType, startDate=start_date, dueDate=due_date)
        db.session.add(new_assessment)
        db.session.commit()
        return {"Message": "Assessment Created Successfully", "Assessment": new_assessment.get_json()}

    except Exception as e:
        print(f"Error Creating Assessment: {e}")
        db.session.rollback()
        return {"Error Message": "Failed To Create Assessment"}

def get_assessments_by_title(assessmentTitle):
    try:
        assessments = Assessment.query.filter_by(assessmentTitle=assessmentTitle).all()
        if assessments:
            return assessments
        else:
            return {"Error Message": f"There Are No Assessments With Title: {assessmentTitle} In The Database"}

    except Exception as e:
        print(f"Error Fetching Assessments: {e}")
        return {"Error Message": "Failed To Fetch Assessments"}

def get_assessments_by_type(assessmentType):
    try:
        assessments = Assessment.query.filter_by(assessmentType=assessmentType).all()
        if assessments:
            return assessments
        else:
            return {"Error Message": f"There Are No Assessments With Type: {assessmentType} In The Database"}

    except Exception as e:
        print(f"Error Fetching Assessments: {e}")
        return {"Error Message": "Failed To Fetch Assessments"}

def list_assessments():
    try:
        assessments = Assessment.query.all()
        if assessments:
            return assessments
        else:
            return {"Message": "No Assessments Found"}
    except Exception as e:
        print(f"Error Listing Assessments: {e}")
        return {"Error Message": "Failed To List Assessments"}

def list_assessments_json():
    try:
        assessments = Assessment.query.all()
        if assessments:
            return [assessments.get_json() for assessment in assessments]
        else:
            return {"Message": "No Assessments Found"}

    except Exception as e:
        print(f"Error Listing Assessments: {e}")
        return {"Error Message": "Failed To List Assessments"}