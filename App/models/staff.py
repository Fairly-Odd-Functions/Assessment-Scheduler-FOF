import flask_login
from App.database import db
from .user import User
import enum
from flask_login import UserMixin

class Staff(User):
  __tablename__ = 'staff'
  staffID = db.Column(db.Integer, db.ForeignKey('user.userID'), primary_key=True)
  
  
  __mapper_args__ ={
    'polymorphic_identity': 'staff'
  }

  def __init__(self, userID, firstName, lastName, password, email):
    super().__init__(userID, firstName, lastName, password, email)
  
  def get_id(self):
    return self.u_ID 

  def to_json(self):
    return {
        "staff_ID": self.staffID,
    } 
  
  def login(self):
    return flask_login.login_user(self)

  def __str__(self):
        return f"Staff(id={self.userID}, email={self.email})"

