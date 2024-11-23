from App.models import Staff, CourseStaff
from App.database import db

def register_staff(firstName, lastName, userID, email, password):
    existingStaff = existingStaff.query(Staff).filter((Staff.email == email) |(Staff.userID == userID)).first() # from the code I have seen so far they only store unique email address, but we should check if some one is already registed using their userID *New Comment

    if existingStaff != None:
        return {"Existing Staff": existingStaff } #wondering if this can work
    
    newStaff = Staff.register(firstName, lastName, userID, email, password) #register() is not currently present in the Staff class
    db.session.add(newStaff)
    db.session.commit()
    return {"New Staff" : newStaff} #wondering if this can work


'''
def register_staff(firstName, lastName, userID, email, password):
    #Check if email is already used by another lecturer ie. lecturer already registered
    staff = db.session.query(Staff).filter(Staff.email == email).count() # from the code I have seen so far they only store unique email address, but we should check if some one is already registed using their userID *New Comment

    if staff == 0:
        newLect = Staff.register(firstName, lastName, userID, email, password)
        return newLect
    return None
'''

def login_staff(email, password):
    staff = db.session.query(Staff).filter(Staff.email==email).first()
    if staff != None:
        if staff.check_password(password):
            return {"Success": staff.login()} #wondering if this can work
    return {"Error Message" : "Login failed, invalid login details"}


def add_CourseStaff(userID,courseCode):
    try:
        existing_course_staff = CourseStaff.query.filter_by(userID=userID, courseCode=courseCode).first()
        if existing_course_staff:
            return {"Existing Course Staff Found" : existing_course_staff}  # Return existing CourseStaff if found

        # Create a new CourseStaff object
        new_course_staff = CourseStaff(userID=userID, courseCode=courseCode)

        # Add and commit to the database
        db.session.add(new_course_staff)
        db.session.commit()
        print (f"New Course Staff Added")
        return new_course_staff
        #return {"New Course Staff Added" : new_course_staff} #can this work or do I have to split it up?
    
    except Exception as e:
        print(f"Failed to add course satff: {e}")
        db.session.rollback()
        return None


def get_registered_courses(userID):
    course_listing = CourseStaff.query.filter_by(userID=userID).all()
    codes=[]
    for item in course_listing:
        codes.append(item.courseCode)
    return codes


'''
To be implemented
Schedule Assessment and/or Notify of clash
Request Override
'''