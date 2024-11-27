import os, tempfile, pytest, logging, unittest

from App.main import create_app
from App.database import db, create_db
#from App.views.auth import login
from App.models import Staff

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

class StaffUnitTest(unittest.TestCase):

    #UNIT TEST - #8: Register Staff
    def test_unit_08_register_staff(self):
        newStaff = Staff("Greg", "Holder", "gregpass", "greg.holder@gmail.com")
        assert newStaff.email == "greg.holder@gmail.com"

        #print("Staff Info:" , newStaff) #Testing Output

    #UNIT TEST - #9: Staff JSON
    def test_unit_09_staff_json(self):
        newStaff = Staff ("Sam", "Jane", "sampass", "sam.jane@gmail.com")

        staff_json = newStaff.get_json()
        self.assertDictEqual({"first_name": "Sam",
                              "last_name": "Jane",
                              "email": "sam.jane@gmail.com"}, staff_json)
        
        #print("Staff Info: ", staff_json)

    