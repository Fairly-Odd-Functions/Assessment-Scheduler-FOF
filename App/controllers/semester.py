from App.models import Semester
from App.database import db

def add_sem(startDate,endDate,semesterID,semesterTitle): #maxAssessments removed
    new_sem = Semester(startDate=startDate,endDate=endDate,semesterID=semesterID,semesterTitle=semesterTitle)
    db.session.add(new_sem)
    db.session.commit()
    return new_sem