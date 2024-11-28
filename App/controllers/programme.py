from App.database import db
from App.models import Programme, CourseProgramme

def create_programme(programmeTitle, programmeDescription):
    try:
        if not programmeTitle or not programmeDescription :
            return {"Error Message": "All Fields Are Required"}

        existingProgramme = Programme.query.filter_by(programmeTitle=programmeTitle).first()
        if existingProgramme:
            return {"Error Message": f"Programme: '{programmeTitle}' Already Exists"}

        new_programme = Programme(programmeTitle=programmeTitle, programmeDescription=programmeDescription)
        db.session.add(new_programme)
        db.session.commit()
        return {"Message": "Programme Created Successfully", "Programme": new_programme}

    except Exception as e:
        print(f"Error Creating Programme: {e}")
        db.session.rollback()
        return {"Error Message": "Failed To Create Programme"}

def get_programme_by_title(programmeTitle):
    try:
        programme = Programme.query.filter_by(programmeTitle=programmeTitle).first()
        if programme:
            return programme
        else:
            return {"Error Message": f"There Is No Programme With Title: {programmeTitle} In The Database"}

    except Exception as e:
        print(f"Error Fetching Programme: {e}")
        return {"Error Message": "Failed To Fetch Requested Programme"}

def list_programmes():
    try:
        programmes = Programme.query.all()
        if programmes:
            return programmes
        else:
            return {"Message": "No Programmes Found"}
    except Exception as e:
        print(f"Error Listing Programmes: {e}")
        return {"Error Message": "Failed To List Programmes"}

def list_programmes_json():
    try:
        programmes = Programme.query.all()
        if programmes:
            return [programme.get_json() for programme in programmes]
        else:
            return {"Message": "No Programmes Found"}

    except Exception as e:
        print(f"Error Listing Programmes: {e}")
        return {"Error Message": "Failed To List Programmes"}

def update_programme(programmeTitle, new_title=None, new_description=None):
    try:
        programme = Programme.query.filter_by(programmeTitle=programmeTitle).first()
        if not programme:
            return {"Error Message": f"There Is No Programme With Title: {programmeTitle} In The Database"}

        if new_title:
            existingProgramme = Programme.query.filter_by(programmeTitle=new_title).first()
            if existingProgramme:
                return {"Error Message": f"A Programme With Title '{new_title}' Already Exists."}
            programme.programmeTitle = new_title
        if new_description:
            programme.programmeDescription = new_description

        db.session.commit()
        return {"Message": "Programme Updated Successfully", "Programme": programme}

    except Exception as e:
        print(f"Error Updating Programme: {e}")
        db.session.rollback()
        return {"Error Message": "Failed To Update Programme"}

def list_programme_courses(programmeTitle):
    try:
        programme = Programme.query.filter_by(programmeTitle=programmeTitle).first()
        if not programme:
            return {"Error Message": f"There Is No Programme With Title: {programmeTitle} In The Database"}
        
        programme_courses = CourseProgramme.query.filter_by(programmeID=programme.programmeID).all()
        if not programme_courses:
            return {"Error Message": f"No Courses Found For Programme: {programme.programmeTitle}"}
        return programme_courses

    except Exception as e:
        print(f"Error While Fetching Courses: {e}")
        return {"Error Message": "Failed To Fetch Courses."}