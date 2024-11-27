import os, tempfile, pytest, logging, unittest

from App.main import create_app
from App.database import db, create_db
#from App.views.auth import login
from App.models import Staff
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
    
    '''
    #UNIT TEST - #9: Register Staff ISSUE- TWO FUNCTIONS HAVE THE SAME NAME
    def test_unit_09_add_course_staff(self):
        staff = Staff ("Iris", "Jack", "irispass", "iris.jack@gmail.com")
        newCourseStaff = add_course_staff("greg.holder@gmail.com", "COMP 100")

        #print("New Course Staff Info:" , newCourseStaff)
    '''

    #UINIT TEST -#10: add_multiple_courses_to_staff - I
    def test_unit_10_add_multiple_courses_to_staff(self):
        newStaff = Staff("Klim", "Lane", "kilmpass", "klim.lane@gmail.com")
        db.session.add(newStaff)
        db.session.commit()
        assert newStaff.email == "klim.lane@gmail.com"

        addCourses = add_multiple_courses_to_staff("klim.lane@gmail.com",["COMP 200", "COMP 300"])


        print("Staff Info:" , addCourses) #Testing Output