import os, tempfile, pytest, logging, unittest
from datetime import date, datetime, timedelta

from App.main import create_app
from App.database import db, create_db
from App.models import Admin, Course, CourseAssessment, CourseOffering, CourseProgramme, CourseStaff, User, Staff, Semester
from App.controllers import *

LOGGER = logging.getLogger(__name__)

@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()

class SemesterIntegrationTests(unittest.TestCase):
    def test_integration_14_add_semester(self):
        message = add_semester("Semester 2", "2024-2025", date(2024, 9, 4), date(2024, 12, 20))
        assert message["New Semester Added"] == {"semesterID" : 1, "semesterName" : "Semester 2"}


    def test_integration_15_get_semester(self):
       add_semester("Semester 3", "2024-2025", date(2024, 5, 15), date(2024, 7, 20))
       semester = get_semester("Semester 3", "2024-2025")
       self.assertDictEqual({"semester_name":"Semester 3",
                            "academicYear": "2024-2025",
                            "startDate": date(2024, 5, 15),
                            "endDate":date(2024, 7, 20)},semester)

                            



