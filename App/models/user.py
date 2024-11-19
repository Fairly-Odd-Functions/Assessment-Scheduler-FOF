from App.database import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    # __abstract__ = True

    userID = db.Column(db.Integer, unique=True, primary_key=True) 
    firstName = db.Column(db.String(120), nullable=False) 
    lastName = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique = True)
    type = db.Column(db.String(120))

    
    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': 'type'
    }

    def __init__(self, userID, firstName, lastName, password, email):
        self.userID = userID
        self.firstName = firstName
        self.lastName = lastName
        self.set_password(password)
        self.email = email

    # ^^^^^^^^^^^^^^^^
    # COMMENT(RYNNIA):   (1) There is a new attribute ‘type’ which is not present within he Updated Model Diagram but
    #                        I can see why it is necessary for subclass implementation so:
    #                        Model Diagram Needs Updating to include attribute ‘type’
    #
    #                    (2) UserID should not be a parameter unless we talking about staffID given to them by university? so,
    #                        Are we using staffID as a parameter?

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)
    
    def to_json(self):
	    return {
            "userID": self.userID,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "password": self.password,
            "email":self.email
        }
        
    def __str__(self):
        return f"Staff(id={self.userID}, email={self.email})"