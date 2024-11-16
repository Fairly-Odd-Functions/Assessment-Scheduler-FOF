from App.database import db
from .user import User 
from App.models import User 
from flask_login import UserMixin, login_user
import flask_login
from flask_login import UserMixin, login_user
import flask_login


class Admin(User,UserMixin):
  __tablename__ = 'admin'
  adminID = db.Column(db.Integer, db.ForeignKey('user.userID'), primary_key=True)
  staffType = db.Column(db.String(120))

  __mapper_args__ ={
    'polymorphic_identity': 'admin'
  }

  def login(self):
      return flask_login.login_user(self)
  
  def __init__(self, userID, firstName, lastName, password, email):
    super().__init__(userID, firstName, lastName, password, email)

  def __createStaff__(userID, firstName, lastName, password, email, status):
    newStaff = Staff(self, userID, firstName, lastName, password, email, status)
    db.session.add(newStaff)  #add to db
    db.session.commit()
    return newStaff

  def __str__(self):
        return f"Admin(id={self.adminID}, email={self.email})" 