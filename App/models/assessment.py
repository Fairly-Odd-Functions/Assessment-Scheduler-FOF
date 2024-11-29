from App.database import db

class Assessment(db.Model):
    __tablename__ = 'assessment'

    # Attributes
    assessmentID = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    assessmentTitle = db.Column(db.String(120),nullable=False)
    assessmentType = db.Column(db.String(120),nullable=False)
    startDate = db.Column(db.DateTime, nullable=True)
    dueDate = db.Column(db.DateTime, nullable=True)

    def __init__(self, assessmentTitle, assessmentType, startDate=None, dueDate=None):
            self.assessmentTitle = assessmentTitle
            self.assessmentType = assessmentType
            self.startDate = startDate
            self.dueDate = dueDate 

    def get_json(self):
        return {
            'assessmentID': self.assessmentID,
            'assessmentTitle': self.assessmentTitle,
            'assessmentType': self.assessmentType,
            'startDate': self.startDate.isoformat() if self.startDate else None,
            'dueDate': self.dueDate.isoformat() if self.dueDate else None
        }

    def __str__(self):
        return (f"assessmentTitle={self.assessmentTitle},"
                f"assessmentType={self.assessmentType},"
                f"startDate={self.startDate},"
                f"dueDate={self.dueDate}")

    def __repr__(self):
        return (f"<Assessment(assessmentTitle='{self.assessmentTitle}', "
                f"assessmentType= '{self.assessmentType}', "
                f"Start Date= '{self.startDate}', "
                f"Due Date= '{self.dueDate}')>")