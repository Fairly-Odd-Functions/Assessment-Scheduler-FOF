from App.database import db
from App.models import User, Admin, Staff

# Create A New User
def create_user(firstName, lastName, password, email, user_type):
    if user_type not in ['staff', 'admin']:
        return None

    if User.query.filter_by(email=email).first():
        return None

    if user_type == 'staff':
        new_user = Staff(firstName=firstName, lastName=lastName, password=password, email=email)
    elif user_type == 'admin':
        new_user = Admin(firstName=firstName, lastName=lastName, password=password, email=email)

    db.session.add(new_user)
    db.session.commit()
    return new_user

# Get All Admin Users
def get_all_admin_users():
    return Admin.query.all()

# Get All Staff Users
def get_all_staff_users():
    return Staff.query.all()

# Get All Admin Users in JSON Format
def get_all_admin_users_json():
    admin_list = Admin.query.all()
    return [admin.get_json() for admin in admin_list]

# Get All Staff Users in JSON Format
def get_all_staff_users_json():
    staff_list = Staff.query.all()
    return [staff.get_json() for staff in staff_list]

# Validate Staff Account
def validate_Staff(staffEmail, password):
    staff = Staff.query.filter_by(email=staffEmail).first()
    if staff and staff.check_password(password):
        return staff
    return None

# Validate Admin Account
def validate_Admin(adminEmail, password):
    admin = Admin.query.filter_by(email=adminEmail).first()
    if admin and admin.check_password(password):
        return admin
    return None

# Get User Account
def get_user(email, password):
    user = validate_Staff(email, password)
    if user:
        return user # User Is A Staff
    user = validate_Admin(email, password)
    if user:
        return user # User Is An Admin
    return None

# Get User ID Via Email
def get_userID(email):
    user = User.query.filter_by(email=email).first()
    if user:
        return user.userID
    return None