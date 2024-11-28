import os, tempfile, pytest, logging, unittest

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


class StaffIntegrationTests(unittest.TestCase):
    def test_integration_16_add_staff(self):
        new_staff = register_staff("Richard", "Maxwell", "maxpass", "max23@email.com")
        second_new_staff = register_staff("Terry", "Frey", "terrypass", "terry45@email.com")
        assert new_staff.email == "max23@email.com"
        assert second_new_staff.email == "terry45@email.com"

     
    def test_integration_17_get_staff_users_json(self):
        new_staff = register_staff("Hailey", "Vogue", "voguepass", "vogue87@email.com")
        staff = get_all_staff_users_json()
        self.assertListEqual([{"first_name": "Richard",
                                "last_name": "Maxwell",
                                "email": "max23@email.com"},
                            {"first_name": "Terry",
                                "last_name": "Frey",
                                "email": "terry45@email.com"},
                            {"first_name": "Hailey",
                                "last_name": "Vogue",
                                "email": "vogue87@email.com"}
                                ],staff)
