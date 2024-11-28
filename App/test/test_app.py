import os, tempfile, pytest, logging, unittest
from App.main import create_app
from App.database import db, create_db
from App.models import *

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