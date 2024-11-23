from App.models import CourseAssessment
from App.models import Assessment
from App.models import Course
from App.database import db

def add_course_assessment(courseCode, assessmentID, assessmentTitle, assessmentType, startDate, dueDate): #startTime, endTime, clashDetected were removed  
    #Add new Assessment to Course
    # newAsm = addCourseAsg(courseCode, a_ID, startDate, endDate, startTime, endTime)
    # return newAsm
    try:
        if not courseCode or not assessmentID or not assessmentTitle or not assessmentType or not startDate or not dueDate:
            return {"Error Message": "All fields are required"}
        
        existingAssessment = CourseAssessment.query.filter_by(courseCode = courseCode, assessmentID = assessmentID).first()
        if existingAssessment != None:
            return {"Error Message": "Assessment Already Exist"}
        
        newAssessment = CourseAssessment(courseCode = courseCode, assessmentID = assessmentID, assessmentTitle = assessmentTitle, assessmentType = assessmentType, startDate = startDate, dueDate = dueDate) #startTime, endTime, clashDetected were removed  
        db.session.add(newAssessment)  #add to db
        db.session.commit()
        return {"New Assessment Added" : newAssessment}
    
    except Exception as e:
      print(f"Error While Adding New Assessment: {e}")
      db.session.rollback() 
      return None 

def list_Assessments():
    return Assessment.query.all()  

def get_Assessment_id(assessmentType):
    assessment=Assessment.query.filter_by(category=assessmentType).first()
    if assessment != None:
        return assessment.assessmentID
    return {"Error Message": "Assessment Not Found"}

def get_Assessment_type(assessmentID):
    assessment=Assessment.query.filter_by(assessmentID=assessmentID).first()
    if assessment!= None:
        return assessment.category.name
    return {"Error Message": "Assessment Not Found"}

def get_CourseAsm_id(assessmentID): #is the courseCode being used here? *New Comment
    return CourseAssessment.query.filter_by(assessmentID=assessmentID).first()   

def get_CourseAsm_code(courseCode):
    return CourseAssessment.query.filter_by(courseCode=courseCode).all()

def get_CourseAsm_level(courseLevel):
    try:
        courses = Course.query.filter_by(level=courseLevel).all()
        assessments=[courses.courseCode for course in courses]
        #for c in courses:
        #    assessments = assessments + get_CourseAsm_code(c)
        return CourseAssessment.query.filter(CourseAssessment.courseCode.in_(assessments)).all()
    
    except Exception as e:
      print(f"Error While Getting Course Assessment Level: {e}")
      db.session.rollback() 
      return None 

def delete_CourseAsm(courseAsm):
    
    try:
        if not courseAsm:
            return {"Error Message": "Course Assessment Not Found"}
        
        db.session.delete(courseAsm)
        db.session.commit()
        return {"Course Assessment was Deleted"}
    
    except Exception as e:
      print(f"Error While Deleting a Course Assessment: {e}")
      db.session.rollback() 
      return None


def get_clashes():
    return CourseAssessment.query.filter_by(clashDetected=True).all() #does not have a clashDetected field anymore
