import os, tempfile, pytest, logging, unittest

from App.main import create_app
from App.database import db, create_db
#from App.views.auth import login
from App.models import Admin

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

        #print("Admin Info:", admin) #Testing Output


    #UNIT TEST - #3: Admin JSON
    def test_unit_03_admin_json(self):
        adminUser1 = Admin ("Star", "Light", "starpass", "star.light@gmail.com")
        
        admin_json = adminUser1.get_json()
        self.assertDictEqual({"firstName": "Star",
                              "lastName": "Light",
                              "email": "star.light@gmail.com"}, admin_json)

        #print("Admins: ", admin_json) #Testing Output
