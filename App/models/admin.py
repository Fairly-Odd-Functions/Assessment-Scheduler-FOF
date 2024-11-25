from App.database import db
from App.models import User 

class Admin(User):
  __tablename__ = 'admin'
  adminID = db.Column(db.Integer, db.ForeignKey('user.userID'), primary_key=True)

  __mapper_args__ ={
    'polymorphic_identity': 'admin'
  }
  
  def __init__(self, adminID, firstName, lastName, password, email):
    # Calling the constructor of the parent class (User) with the provided arguments
    super().__init__(adminID, firstName, lastName, password, email)

  def __str__(self):
    return f"Admin(id={self.adminID}, email={self.email})" 
  
  def get_json(self):
    return {
      "firstName": self.firstName,
      "lastName": self.lastName,
      "email": self.email
    }  