from App.database import db
from werkzeug.security import check_password_hash, generate_password_hash

class User(db.Model):
    __tablename__ = 'user'
    
    #Attributes
    userID = db.Column(db.Integer, unique=True, primary_key=True) 
    firstName = db.Column(db.String(120), nullable=False) 
    lastName = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique = True)

    #Distinguishes between different user types ('admin', 'staff')
    user_type = db.Column(db.String(30))

    __mapper_args__ = {
        'polymorphic_identity': 'user',
    }

    def __init__(self, userID, firstName, lastName, password, email, user_type):
        self.staffD = userID
        self.firstName = firstName
        self.lastName = lastName
        self.set_password(password)
        self.email = email
        self.user_type = user_type

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)
    
    def get_json(self):
        return {
            "firstName": self.firstName,
            "lastName": self.lastName,
            "password": self.password,
            "email": self.email
        }
        
    def __str__(self):
        return f"Staff(id={self.userID}, 
                firstName={self.firstName}, 
                lastName={self.lastName}, 
                email={self.email})"
    
    def __repr__(self):
        return (
            f"Staff(userID={self.userID}, firstName='{self.firstName}', "
            f"lastName='{self.lastName}', email='{self.email}')"
        )