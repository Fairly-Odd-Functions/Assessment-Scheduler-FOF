import os, tempfile, pytest, logging, unittest

from App.main import create_app
from App.database import db, create_db
#from App.views.auth import login
from App.models import Admin, Staff, User 
from App.controllers import ( #Staff Controller
    register_staff,
    add_course_staff,
    add_multiple_courses_to_staff,
    get_staff_courses,
    update_staff,
    delete_staff,
    get_staff_by_email,
    get_all_staff,
    remove_staff_from_course,
    is_staff_assigned_to_course,
    get_staff_with_courses,
)


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
        newStaff = register_staff("Greg", "Holder", "gregpass", "greg.holder@gmail.com")
        assert newStaff.email == "greg.holder@gmail.com"

        #print("Staff Info:" , newStaff) #Testing Output
