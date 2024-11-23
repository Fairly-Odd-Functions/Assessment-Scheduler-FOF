from App.models import Semester
from App.database import db

def add_semester(startDate,endDate,semesterID,semesterTitle): #maxAssessments removed
    try:
        if not startDate or not endDate or not semesterID or not semesterTitle:
            return {"Error Message": "All fields are required"}
        
        existingSemester = Semester.query.filter_by(semesterID = semesterID).first()
        if existingSemester != None:
            return {"Error Message": "Semester {semesterID} Already Exists"}
        

        new_semester = Semester(startDate=startDate,endDate=endDate,semesterID=semesterID,semesterTitle=semesterTitle)
        db.session.add(new_semester)
        db.session.commit()
        return {"New Semester Added": new_semester}
    
    except Exception as e:
        print(f"Error While Adding Semester: {e}")
        db.session.rollback()
        return None
