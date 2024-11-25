from App.database import db

class Semester(db.Model):
    __tablename__='semester'

    # Attributes
    semesterID = db.Column(db.Integer, primary_key= True, autoincrement=True)
    semesterName = db.Column(db.String(120),nullable = False)
    academicYear = db.Column(db.String(9), nullable=False)
    startDate = db.Column(db.Date,nullable=False)
    endDate = db.Column(db.Date,nullable=False)

    def __init__(self, semesterName, academicYear, startDate, endDate):
        self.semesterName = semesterName
        self.academicYear = academicYear
        self.startDate = startDate
        self.endDate = endDate

    def get_json(self):
        return{
            "semester_name":self.semesterName,
            "academicYear": self.academicYear,
            "startDate":self.startDate,
            "endDate":self.endDate
        }

    def __str__(self):
        return f"{self.semesterName} {self.academicYear} (Start: {self.startDate}, End: {self.endDate})"

    def __repr__(self):
        return (
            f"Semester(semesterID={self.semesterID}, semesterName='{self.semesterName}', "
            f"academicYear='{self.academicYear}', startDate='{self.startDate}', endDate='{self.endDate}')"
        )