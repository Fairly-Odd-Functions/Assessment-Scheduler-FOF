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


class AdminIntegrationTests(unittest.TestCase):
    def test_integration_05_create_admin(self):
        admin = create_admin("Jill", "Hillington", "jillpass", "jillandhills@email.com")
        assert admin.email == "jillandhills@email.com"

    def test_integration_06_get_all_admin_users_json(self):
        admin = create_admin("David", "Johnson", "davepass", "davesquare@email.com")
        admin_users = get_all_admin_users_json()
        self.assertListEqual([{"firstName" : "Jill",
                            "lastName" : "Hillington",
                            "email" : "jillandhills@email.com"},

                            {"firstName" : "David",
                            "lastName" : "Johnson",
                            "email" : "davesquare@email.com"}], admin_users)
