from App.database import db
from App.models import Admin

# Create A New Admin
def create_admin(firstName, lastName, password, email):
    if Admin.query.filter_by(email=email).first():
        return None

    new_admin = Admin(firstName=firstName, lastName=lastName, password=password, email=email)
    db.session.add(new_admin)
    db.session.commit()
    return new_admin

# Get All Admin Users
def get_all_admin_users():
    return Admin.query.all()

# Get All Admin Users In JSON Format
def get_all_admin_users_json():
    admin_list = Admin.query.all()
    return [admin.get_json() for admin in admin_list]

# Update Admin Information
def update_admin(adminEmail, firstName=None, lastName=None, password=None, email=None):
    try:
        admin = Admin.query.filter_by(email=adminEmail).first()
        if not admin:
            return None

        # Update Relevant Admin Attributes
        if firstName:
            admin.firstName = firstName
        if lastName:
            admin.lastName = lastName
        if password:
            admin.set_password(password)
        if email:
            existing_admin = Admin.query.filter_by(email=email).first()
            if existing_admin:
                return None
            admin.email = email

        db.session.commit()
        return admin

    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}

# Delete An Admin
def delete_admin(adminEmail):
    try:
        admin = Admin.query.filter_by(email=adminEmail).first()
        if not admin:
            return None

        db.session.delete(admin)
        db.session.commit()
        return admin

    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}

# Get Admin By Email
def get_admin_by_email(adminEmail):
    admin = Admin.query.filter_by(email=adminEmail).first()
    if not admin:
        return None
    return admin

# Get All Admins
def get_all_admins():
    admin_list = Admin.query.all()
    return admin_list
