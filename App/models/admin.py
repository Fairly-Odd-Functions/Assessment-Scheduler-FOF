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
  
  # ~~~~~~~~~~~~ FEEDBACK ~~~~~~~~~~~~
  # ^^^^^^^^^^^^^^^^
  # COMMENT (RYNNIA):     (1) Staff is not defined change to Admin
  #
  #                       (2) Staff(self, userID, firstName, lastName, password,   email, status)  , 
  #                           status would not be passed properly because __init__ for Staff does not have status as a parameter.
  #
  #                       (3) There is no specification for staffType it should be hardcoded as ‘staff’ for example 
  #
  #                       (4) Status is not specified within Model diagram, unless you meant to include it and left it as is?
  #                           This needs to be discussed
  # -----------------------------------------------------------------------------------------------------------------------------
  # JaleneA
  #   - What is UserMixin?
  #
  #   - Why is their an inclusion of self within the Staff parameter?
  #     should just be userID, firstName, lastName, password, email and staffType
  #
  #   - staffType won't be hardcorded as "Staff", but rather is depends on what's inputted in the parameter of the function.
  #
  #   - The __tablename__ annonation, its not something I've ever seen sir used in its flaskmvc repository.
  #
  #   - Points 2 & 4 from Rynnia
  # -----------------------------------------------------------------------------------------------------------------------------


  def __str__(self):
        return f"Admin(id={self.adminID}, email={self.email})" 