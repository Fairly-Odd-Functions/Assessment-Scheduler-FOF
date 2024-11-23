from App.models import Staff, CourseStaff
from App.database import db

def register_staff(firstName, lastName, userID, email, password):
    #Check if email is already used by another lecturer ie. lecturer already registered
    staff = db.session.query(Staff).filter(Staff.email == email).count() # from the code I have seen so far they only store unique email address, but we should check if some one is already registed using their userID *New Comment

    if staff == 0:
        newLect = Staff.register(firstName, lastName, userID, email, password)
        return newLect
    return None

def login_staff(email, password): #I'll need to vaiadate the staff *New Comment
    staff = db.session.query(Staff).filter(Staff.email==email).first()
    if staff != None:
        if staff.check_password(password):
            return staff.login()
    return "Login failed"

def add_CourseStaff(userID,courseCode):
    existing_course_staff = CourseStaff.query.filter_by(userID=userID, courseCode=courseCode).first()
    if existing_course_staff:
        return existing_course_staff  # Return existing CourseStaff if found

    # Create a new CourseStaff object
    new_course_staff = CourseStaff(userID=userID, courseCode=courseCode)

    # Add and commit to the database
    db.session.add(new_course_staff)
    db.session.commit()

    return new_course_staff

def get_registered_courses(userID):
    course_listing = CourseStaff.query.filter_by(userID=userID).all()
    codes=[]
    for item in course_listing:
        codes.append(item.courseCode)
    return codes