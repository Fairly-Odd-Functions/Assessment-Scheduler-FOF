from .user import User
from App.database import db
from flask_login import UserMixin # type: ignore

class Admin(User, UserMixin):
    __tablename__ = 'admin'

    # Attributes
    adminID = db.Column(db.Integer, db.ForeignKey('user.userID'), primary_key=True)

    __mapper_args__ ={
      'polymorphic_identity': 'admin'
    }

    def __init__(self, firstName, lastName, password, email):
      # Calling the constructor of the parent class (User) with the provided arguments
      super().__init__(firstName, lastName, password, email, user_type='admin')

    def get_json(self):
      return {
        "firstName": self.firstName,
        "lastName": self.lastName,
        "email": self.email
      }

    def __str__(self):
      return f"Admin(userID={self.adminID}, firstname={self.firstName}, lastname={self.lastName}, email={self.email})"

    def __repr__(self):
      return (
        f"Admin(adminID={self.adminID}, firstName='{self.firstName}', lastName='{self.lastName}', "
        f"email='{self.email}')"
      )