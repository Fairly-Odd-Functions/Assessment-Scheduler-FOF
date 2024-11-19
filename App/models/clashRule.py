from App.database import db

class ClashRule(db.Model):
  __tablename__ = 'clashrule'

  clashRuleID = db.Column(db.Integer, primary_key=True)
  userID = db.Column(db.Integer, db.ForeignKey('user.userID'), nullable=False)
  clashRuleTitle = db.Column(db.String(120), nullable=False)
  clashRuleDescription = db.Column(db.String(120),nullable=False)
  allowableDays = db.Column(db.Integer)
  
  def __init__(self, userID, clashRuleTitle, clashRuleDescription):
    self.userID = userID
    self.clashRuleTitle = clashRuleTitle
    self.clashRuleDescription = clashRuleDescription
    

  def to_json(self):
    return {
      "userID" : self.userID,
      "clashRuleTitle" : self.clashRuleTitle,
      "clashRuleDescription" : self.clashRuleDescription
      
    }

  def addNewRule(userID, clashRuleTitle, clashRuleDescription):
    newRule = ClashRule(userID, clashRuleTitle, clashRuleDescription)
    db.session.add(newRule)
    db.session.commit()
    return newRule
