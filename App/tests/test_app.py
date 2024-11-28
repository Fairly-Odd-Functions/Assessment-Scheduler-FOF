import os, tempfile, pytest, logging, unittest
from App.main import create_app
from App.database import db, create_db
from App.models import *
from App.controllers import *

LOGGER = logging.getLogger(__name__)

@pytest.fixture(autouse=True, scope="function")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.session.remove()
    db.drop_all()

'''
    Unit Tests
'''

class AdminUnitTest(unittest.TestCase):
    
    #UNIT TEST - #1: Create Admin
    def test_unit_01_create_admin(self):
        admin = Admin("Jane", "Doe", "janepass", "jane.doe@gmail.com")
        assert admin.email == "jane.doe@gmail.com"

    #UNIT TEST - #3: Admin JSON
    def test_unit_03_admin_json(self):
        adminUser1 = Admin ("Star", "Light", "starpass", "star.light@gmail.com")
        admin_json = adminUser1.get_json()
        self.assertDictEqual({"firstName": "Star",
                              "lastName": "Light",
                              "email": "star.light@gmail.com"}, admin_json)

class StaffUnitTest(unittest.TestCase):

    #UNIT TEST - #8: Register Staff
    def test_unit_08_register_staff(self):
        newStaff = Staff("Greg", "Holder", "gregpass", "greg.holder@gmail.com")
        assert newStaff.email == "greg.holder@gmail.com"

    #UNIT TEST - #9: Staff JSON
    def test_unit_09_staff_json(self):
        newStaff = Staff ("Sam", "Jane", "sampass", "sam.jane@gmail.com")
        staff_json = newStaff.get_json()
        self.assertDictEqual({"first_name": "Sam",
                              "last_name": "Jane",
                              "email": "sam.jane@gmail.com"}, staff_json)
 
class UserUnitTest(unittest.TestCase):

    #UNIT TEST - #19: Create User
    def test_unit_19_create_user(self):
        user = User("Hope", "Ice", "hopepass", "hope.ice@gmail.com", "staff" )
        assert user.email == "hope.ice@gmail.com"
    
    # UNIT TEST - #24: Set Password
    def test_unit_24_set_password(self):
        password = "sampass"
        staff = User("Sam", "Smit", "sampass", "sam.smith@gmail.com", "staff")
        assert staff.password != password

    # UNIT TEST - #25: Check Password
    def test_unit_25_check_password(self):
        password = "janepass"
        staff = User("Jane", "Doe", "janepass", "jane.doeh@gmail.com", "staff")
        assert staff.check_password(password)

'''
    Integration Tests
'''

class UserIntegrationTests(unittest.TestCase):
    # def test_integration_01_authenticate_user_valid(self):
    #     new_user = create_user("Robert", "Watson", "robpass", "rob22@email.com", "staff")
    #     response = login_user(new_user)
    #     assert response is not None

    # def test_integration_02_authenticate_user_invalid(self):
    #     user = get_user("rob22@email.com", "robpass")
    #     response = login_user(user)
    #     assert response is None

    def test_integration_02_get_user(self):
        new_user = create_user("Jenny", "Voe", "voepass", "voe55@email.com", "staff")
        test = get_user("voe55@email.com","voepass")
        assert test is not None

    def test_integration_03_get_user_invalid(self):
        new_user = create_user("Lily", "Daisy", "daisypass", "daisy35@email.com", "staff")
        test = get_user("daisy35@email.com","notdaisypass")
        assert test is None

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