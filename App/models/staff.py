from App.database import db
from .user import User

class Staff(User):
  __tablename__ = 'staff'
  staffID = db.Column(db.Integer, db.ForeignKey('user.userID'), primary_key=True)

  __mapper_args__ ={
    'polymorphic_identity': 'staff'
  }

  def __init__(self, firstName, lastName, password, email):
    # Passing Relevant Fields To User Constructor
    super().__init__(firstName, lastName, password, email)

  def get_json(self):
    return {
        "irst_name": self.firstName,
        "last_name": self.lastName,
        "email": self.email
    } 

  def __str__(self):
        return f"Staff(ID={self.staffID}, email={self.email})"