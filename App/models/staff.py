from .user import User
from App.database import db
from flask_login import UserMixin # type: ignore

class Staff(User, UserMixin):
    __tablename__ = 'staff'

    # Attributes
    staffID = db.Column(db.Integer, db.ForeignKey('user.userID'), primary_key=True)

    __mapper_args__ ={
      'polymorphic_identity': 'staff'
    }

    def __init__(self, firstName, lastName, password, email):
      # Passing Relevant Fields To User Constructor
      super().__init__(firstName, lastName, password, email, user_type='staff')

    def get_json(self):
      return {
          "first_name": self.firstName,
          "last_name": self.lastName,
          "email": self.email
      }

    def __str__(self):
          return f"Staff(userID={self.staffID}, firstname={self.firstName}, lastname={self.lastName}, email={self.email})"