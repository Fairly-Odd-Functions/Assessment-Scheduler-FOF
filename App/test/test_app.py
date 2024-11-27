import os, tempfile, pytest, logging, unittest

from App.main import create_app
from App.database import db, create_db
#from App.views.auth import login
from App.models import User 

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

class UserUnitTest(unittest.TestCase):

    #UNIT TEST - #19: Create User
    def test_unit_19_create_user(self):
        user = User("Hope", "Ice", "hopepass", "hope.ice@gmail.com", "staff" )
        assert user.email == "hope.ice@gmail.com"

        #print("User Info:", user) #Testing Output
    
    
    # UNIT TEST - #24: Set Password
    def test_unit_24_set_password(self):
        password = "sampass"
        staff = User("Sam", "Smit", "sampass", "sam.smith@gmail.com", "staff")
        assert staff.password != password

        #print("Password: ", staff)

    # UNIT TEST - #25: Check Password
    def test_unit_25_check_password(self):
        password = "janepass"
        staff = User("Jane", "Doe", "janepass", "jane.doeh@gmail.com", "staff")
        assert staff.check_password(password)
