from App.database import db
from App.models import Assessment

def create_assessment(assessmentTitle, assessmentType):
    try:
        if not assessmentTitle or not assessmentType:
            return {"Error Message": "All Fields Are Required"}

        new_assessment = Assessment(assessmentTitle=assessmentTitle, assessmentType=assessmentType)
        db.session.add(new_assessment)
        db.session.commit()
        return {"Message": "Assessment Created Successfully", "Assessment": new_assessment.get_json()}

    except Exception as e:
        print(f"Error Creating Assessment: {e}")
        db.session.rollback()
        return {"Error Message": "Failed To Create Assessment"}

def update_assessment(assessmentID, new_title=None, new_type=None):
    try:
        assessment = Assessment.query.get(assessmentID)
        if not assessment:
            return {"Error Message": f"There Is No Assessment With ID: {assessmentID} In The Database"}

        if new_title and new_title != assessment.assessmentTitle:
            assessment.assessmentTitle = new_title
        if new_type:
            assessment.assessmentType = new_type

        db.session.commit()
        return {"Message": "Assessment Updated Successfully", "Assessment": assessment}

    except Exception as e:
        print(f"Error Updating Assesment: {e}")
        db.session.rollback()
        return {"Error Message": "Failed To Update Assessment"}

def get_assessment_by_id(assessmentID):
    try:
        assessment = Assessment.query.filter_by(assessmentID=assessmentID).first()
        if assessment:
            return assessment
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_assessments_by_title(assessmentTitle):
    try:
        assessments = Assessment.query.filter_by(assessmentTitle=assessmentTitle).all()
        if assessments:
            return {"Assessments": [assessment.get_json() for assessment in assessments]}
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
            return {"Assessments": [assessment.get_json() for assessment in assessments]}
        else:
            return {"Message": "No Assessments Found"}

    except Exception as e:
        print(f"Error Listing Assessments: {e}")
        return {"Error Message": "Failed To List Assessments"}