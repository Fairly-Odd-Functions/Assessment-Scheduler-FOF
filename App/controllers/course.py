from App.models import Course
from App.database import db

def add_Course(courseCode, courseTitle, courseDescription, courseLevel, offeredSemester, clashRules, courseCredits): #aNum removed and clashRuleID and courseCredits were added // clashRuleID was changed to clashRules to match the new model diagram
    try:
        if not courseCode or not courseTitle or not courseDescription or not courseLevel or not offeredSemester or not clashRules or not courseCredits:
            return {"Error Message":"All fields are required"}
        
        # Check if courseCode is already in db ie. course was already added
        existingCourse = Course.query.filter_by(courseCode = courseCode, offeredSemester = offeredSemester).first()  
        if existingCourse != None: 
            return {"This Course Already Exist": existingCourse}
        
        
        #Add new Course
        newCourse = Course(courseCode = courseCode, courseTitle = courseTitle, courseDescription = courseDescription, courseLevel = courseLevel, offeredSemester = offeredSemester, clashRules = clashRules, courseCredits = courseCredits) #Had to change since addCourse() is no longer in the models
        db.session.add(newCourse)
        db.session.commit()
        return {"Course Added Successfully": newCourse} 
    
    except Exception as e:
        print(f"Error Adding a New Course: {e}")
        db.session.rollback() 
        return None 
    

def list_Courses():
    try:
        return Course.query.all()
    
    except Exception as e:
        print(f"Error While Trying to List Courses: {e}") 
        return None 
 

def get_course(courseCode, offeredSemester):
    try:
        course = Course.query.filter_by(courseCode = courseCode, offeredSemester=offeredSemester).first()
        if not course:
            return {"Error Message": "Course Not Found"}
        return {"Course Found" : course}
    except Exception as e:
        print(f"Error While Trying to Find Course: {e}") 
        return None 
    
def get_list_coursecode(courseCode):
    return Course.query.filter_by(courseCode=courseCode).all()

def edit_course(review, staff, is_positive, comment):
    if review.reviewer == staff:
        review.isPositive = is_positive
        review.comment = comment
        db.session.add(review)
        db.session.commit()
        return review
    return None    

def delete_Course(courseCode, offeredSemester): #parameter should be updated e.g. delete_Course(courseCode, offeredSemester) for unique identification, since different courses can have the same course codes but are offered during differnet semesters *New Comment
    try:
        course = Course.query.filter_by(courseCode = courseCode, offeredSemester=offeredSemester).first()
        if not course:
            return {"Error Message": "Course Not Found"}
        db.session.delete(course)
        db.session.commit()
        return {"Course Deleted": course}
    
    except Exception as e:
        print(f"Error Deleting the Course: {e}")
        db.session.rollback() 
        return None 
         