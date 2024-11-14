from App.models import CourseAssessment
from App.models import Assessment
from App.models import Course
from App.database import db

def add_CourseAsm(courseCode, assessmentID, assessmentTitle, assessmentType, startDate, dueDate): #startTime, endTime, clashDetected were removed  
    #Add new Assessment to Course
    # newAsm = addCourseAsg(courseCode, a_ID, startDate, endDate, startTime, endTime)
    # return newAsm
    newAsg = CourseAssessment(courseCode, assessmentID, assessmentTitle, assessmentType, startDate, dueDate) #startTime, endTime, clashDetected were removed  
    db.session.add(newAsg)  #add to db
    db.session.commit()
    return newAsg

def list_Assessments():
    return Assessment.query.all()  

def get_Assessment_id(aType):
    assessment=Assessment.query.filter_by(category=aType).first()
    return assessment.assessmentID

def get_Assessment_type(assessmentID):
    assessment=Assessment.query.filter_by(assessmentID=assessmentID).first()
    return assessment.category.name

def get_CourseAsm_id(id): #is the courseCode being used here? *New Comment
    return CourseAssessment.query.filter_by(id=id).first()   

def get_CourseAsm_code(code):
    return CourseAssessment.query.filter_by(courseCode=code).all()

def get_CourseAsm_level(level):
    courses = Course.query(level=level).all()
    assessments=[]
    for c in courses:
        assessments = assessments + get_CourseAsm_code(c)
    return assessments

def delete_CourseAsm(courseAsm): #delete based on their assessmentID e.g.delete_CourseAsm(assessmentID)
    db.session.delete(courseAsm)
    db.session.commit()
    return True        


#Will have to get back to this
def get_clashes():
    return CourseAssessment.query.filter_by(clashDetected=True).all()
