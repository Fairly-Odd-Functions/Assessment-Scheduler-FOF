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

class UserIntegrationTests(unittest.TestCase):
    
    # def test_integration_01_authenticate_user_valid(self):
    #     new_user = create_user("Robert", "Watson", "robpass", "rob22@email.com", "staff")
    #     response = login_user(new_user)
    #     assert response is not None

    # def test_integration_02_authenticate_user_invalid(self):
    #     new_user = create_user()

    def test_integration_02_get_user(self):
        new_user = create_user("Jenny", "Voe", "voepass", "voe55@email.com", "staff")
        test = get_user("voe55@email.com","voepass")
        assert test is not None

    def test_integration_03_get_user_invalid(self):
        new_user = create_user("Lily", "Daisy", "daisypass", "daisy35@email.com", "staff")
        test = get_user("daisy35@email.com","notdaisypass")
        assert test is None

class StaffIntegrationTests(unittest.TestCase):
    def test_integration_04_create_admin(self):
        admin = create_admin("Jill", "Hillington", "jillpass", "jillandhills@email.com")
        assert admin.email == "jillandhills@email.com"

    def test_integration_05_get_all_admin_users_json(self):
        admin = create_admin("David", "Johnson", "davepass", "davesquare@email.com")
        admin_users = get_all_admin_users_json()
        self.assertListEqual([{"firstName" : "Jill",
                            "lastName" : "Hillington",
                            "email" : "jillandhills@email.com"},

                            {"firstName" : "David",
                            "lastName" : "Johnson",
                            "email" : "davesquare@email.com"}], admin_users)

class CourseIntegrationTests(unittest.TestCase):
    def test_integration_06_add_course(self):
        add_course("12345","Theory of Maths",3,"Introduction to the nature of numbers, functions and proofs fo University",1)
        course = get_course("12345")
        self.assertDictEqual({"courseCode" : "12345",
                            "courseTitle" : "Theory of Maths",
                            "courseCredits" : 3,
                            "courseDescription" : "Introduction to the nature of numbers, functions and proofs fo University",
                            "courseLevel" : 1}, course)
                    
    def test_integration_07_list_courses(self):
        add_course("12300","Governance and Technology",4,"Welcome to the harmony of technology in the field of Government arts",2)
        courses = list_courses()
        self.assertListEqual([{"courseCode" : "12345",
                            "courseTitle" : "Theory of Maths",
                            "courseCredits" : 3,
                            "courseDescription" : "Introduction to the nature of numbers, functions and proofs fo University",
                            "courseLevel" : 1},
                            
                            {"courseCode" : "12300",
                            "courseTitle" : "Governance and Technology",
                            "courseCredits" : 4,
                            "courseDescription" : "Welcome to the harmony of technology in the field of Government arts",
                            "courseLevel" : 2}],courses)


