from App.models import User, Admin, Staff

def validate_User(email, password, staffType):
    systemUser = staffType.query.filter_by(email=email).first() #can this work?
    #systemUser = User.query.filter_by(email=email).first() #or should it be this
    if systemUser and User.check_password(password):
        return systemUser
    return None

def get_user(email, password):
    for staffType in (Staff , Admin):
        systemUser = validate_User(email, password, staffType)
        if systemUser != None:
            return systemUser
    return None

def get_uid(email):
    for staffType in (Staff, Admin):
        systemUser= staffType.query.filter_by(email=email).first() #can this work?
        if systemUser != None:
            return systemUser.userID
    return None



''' Original Code
def validate_Staff(email, password):
    staff = Staff.query.filter_by(email=email).first()
    if staff and staff.check_password(password):
        return staff
    return None

def validate_Admin(email, password):
    admin = Admin.query.filter_by(email=email).first()
    if admin and admin.check_password(password):
        return admin
    return None

def get_user(email, password):
    user = validate_Staff(email, password)
    if user != None:
        return user
    user = validate_Admin(email, password)
    if user !=None:
        return user
    return None

def get_uid(email):
    user= Staff.query.filter_by(email=email).first()
    if user:
        return user.userID
    return None
'''