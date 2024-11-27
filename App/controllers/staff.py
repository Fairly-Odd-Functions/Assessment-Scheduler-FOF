from App.database import db
from App.models import Staff, CourseStaff

# Register A New Staff Account [Edited by Rynnia]
def register_staff(firstName, lastName, password, email):
    
    try:
        # Check If Email Is Already Used
        email_check = db.session.query(Staff).filter(Staff.email == email).count()

        # Check If Password Is Already In Use [Added check for duplicate password]
        password_check = db.session.query(Staff).filter(Staff.password == password).count()

        if email_check > 0:
                return None
        #[Added check for duplicate password]
        elif password_check > 0:
            return None 
        else:
            new_staff = Staff (
                firstName=firstName,
                lastName=lastName,
                password=password,
                email=email
            )

            db.session.add(new_staff)
            db.session.commit()

            return new_staff
        
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}

# ALT: Add Multiple Courses To A Staff Member
def add_multiple_courses_to_staff(staffEmail, courseCodes):
    staff_member = Staff.query.filter_by(email=staffEmail).first()
    if not staff_member:
        return None

    existing_courses = CourseStaff.query.filter_by(staffID=staff_member.staffID).filter(CourseStaff.courseCode.in_(courseCodes)).all()
    existing_course_codes = [item.courseCode for item in existing_courses]

    # Only Add Courses That Are Not Already Assigned
    new_courses = []
    for courseCode in courseCodes:
        if courseCode not in existing_course_codes:
            new_course_staff = CourseStaff(courseCode=courseCode, staffID=staff_member.staffID)
            db.session.add(new_course_staff)
            new_courses.append(new_course_staff)

    db.session.commit()

    return new_courses

# Get Courses Associated With A Staff Member
def get_staff_courses(staffEmail):
    staff_member = Staff.query.filter_by(email=staffEmail).first()
    if not staff_member:
        return []

    course_listing = CourseStaff.query.filter_by(staffID=staff_member.staffID).all()
    return [item.courseCode for item in course_listing]

# Update Staff Information [Edited by Rynnia]
def update_staff(staffEmail, firstName=None, lastName=None, password=None, email=None):
    try: 
        staff_member = Staff.query.filter_by(email=staffEmail).first()
        if not staff_member:
            return None

        # Update Relevant Staff Attributes
        if firstName:
            staff_member.firstName = firstName
        if lastName:
            staff_member.lastName = lastName
        if password:
            staff_member.set_password(password)
        if email:
            # Checking If Email Is Unique
            if email and Staff.query.filter_by(email=email).first() != staff_member:
                if Staff.query.filter_by(email=email).count() > 0:
                    #[Added a more appropriate error message]
                    return {"error":"Email address is already in use by another staff member. Please choose a different email address."}
                staff_member.email = email

        db.session.commit()
        return staff_member

    except Exception as e:
        db.session.rollback()
        return {"error":str(e)}

# Delete A Staff Member  [Edited by Rynnia]
def delete_staff(staffEmail):
    try:
        staff_member = Staff.query.filter_by(email=staffEmail).first()
        if not staff_member:
            return "Error: Staff member not found" #[Replaced return None with a more appropriate error message]

        # Delete Course Associations
        CourseStaff.query.filter_by(staffID=staff_member.staffID).delete()

        db.session.delete(staff_member)
        db.session.commit()

        return "Staff member deleted successfully"
    
    except Exception as e:
        db.session.rollback()
        return f"Error deleting staff member: {str(e)}"

# Get Staff By Email
def get_staff_by_email(staffEmail):
    staff_member = Staff.query.filter_by(email=staffEmail).first()
    if not staff_member:
        return None
    return staff_member

# Get All Staff Members
def get_all_staff():
    staff_list = Staff.query.all()
    return staff_list

# Remove A Staff Member From A Course
def remove_staff_from_course(staffEmail, courseCode):
    staff_member = Staff.query.filter_by(email=staffEmail).first()
    if not staff_member:
        return None

    course_staff = CourseStaff.query.filter_by(staffID=staff_member.staffID, courseCode=courseCode).first()
    if not course_staff:
        return None

    db.session.delete(course_staff)
    db.session.commit()

    return course_staff

# Check If Staff Is Assigned To A Course
def is_staff_assigned_to_course(staffEmail, courseCode):
    staff_member = Staff.query.filter_by(email=staffEmail).first()
    if not staff_member:
        return False

    course_staff = CourseStaff.query.filter_by(staffID=staff_member.staffID, courseCode=courseCode).first()
    return course_staff is not None

# Get Staff With Their Assigned Course/s
def get_staff_with_courses(staffEmail):
    staff_member = Staff.query.filter_by(email=staffEmail).first()
    if not staff_member:
        return None

    courses = [item.courseCode for item in staff_member.assigned_courses]
    return {
        "Staff": staff_member.get_json(),
        "Courses": courses
    }