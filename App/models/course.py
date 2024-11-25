from App.database import db

class Course(db.Model):
    __tablename__ = 'course'

    # Attributes
    courseCode = db.Column(db.String(9), primary_key=True)
    courseTitle = db.Column(db.String(120), nullable=False)
    courseCredits = db.Column(db.Integer, default=0)
    courseDescription = db.Column(db.String(1024), nullable=False)
    courseLevel = db.Column(db.Integer, nullable=False)

    # Relationships
    offerings = db.relationship('CourseOffering', backref='course', lazy=True)

    def __init__(self, courseCode, courseTitle, courseCredits=0, courseDescription="", courseLevel=1):
        self.courseCode = courseCode
        self.courseTitle = courseTitle
        self.courseCredits = courseCredits
        self.courseDescription = courseDescription
        self.courseLevel = courseLevel

    def get_json(self):
        return {
            "courseCode": self.courseCode,
            "courseTitle": self.courseTitle,
            "courseCredits": self.courseCredits,
            "courseDescription": self.courseDescription,
            "courseLevel": self.courseLevel,
        }

    def __str__(self):
        return f"{self.courseTitle} ({self.courseCode}) - {self.courseCredits} credits, Level {self.courseLevel}"

    def __repr__(self):
        return (
            f"Course(courseCode='{self.courseCode}', courseTitle='{self.courseTitle}', "
            f"courseCredits={self.courseCredits}, courseDescription='{self.courseDescription[:30]}...', "
            f"courseLevel={self.courseLevel})"
        )