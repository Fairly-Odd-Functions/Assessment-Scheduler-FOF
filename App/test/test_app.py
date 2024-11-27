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

    #UNIT TEST -#10: Add Multiple Courses to a Staff 
    def test_unit_10_add_multiple_courses_to_staff(self):
        newStaff = Staff("Klim", "Lane", "kilmpass", "klim.lane@gmail.com")
        db.session.add(newStaff)
        db.session.commit()
        assert newStaff.email == "klim.lane@gmail.com"

        addCourses = add_multiple_courses_to_staff("klim.lane@gmail.com",["COMP 200", "COMP 300"])

        #print("Staff Info:" , addCourses) #Testing Output


    #UNIT TEST -#11: Get Staff Assigned Courses
    def test_unit_11_get_staff_courses(self):
        newStaff = Staff("Millie", "Nike", "milliepass", "millie.nike@gmail.com")
        db.session.add(newStaff)
        db.session.commit()
        assert newStaff.email == "millie.nike@gmail.com"

        assignStaffCourses = add_multiple_courses_to_staff("millie.nike@gmail.com",["COMP 100", "COMP 200"])

        courseStaff = get_staff_courses("millie.nike@gmail.com")

        #print("Staff Courses:" , courseStaff) #Testing Output


    #UNIT TEST -#12: Update Staff
    def test_unit_12_update_staff(self):
        newStaff = Staff("Ollie", "Pon", "olliepass", "ollie.pon@gmail.com")
        db.session.add(newStaff)
        db.session.commit()
        assert newStaff.email == "ollie.pon@gmail.com"

        updateStaff = update_staff("ollie.pon@gmail.com", "Que", "Rick", "quepass", "“que.rick@gmail.com")

        #print("Updated Staff Info:" , updateStaff) #Testing Output

    #UNIT TEST -#13: Delete Staff
    def test_unit_13_delete_staff(self):
        newStaff = Staff("Sam", "Tev", "sampass", "sam.tev@gmail.com")
        db.session.add(newStaff)
        db.session.commit()
        assert newStaff.email == "sam.tev@gmail.com"

        deleteStaff = delete_staff("sam.tev@gmail.com")

        #print("Deleted Staff:" , deleteStaff) #Testing Output


    #UNIT TEST -#14: Get Staff by Email
    def test_unit_14_get_staff_by_email(self):
        newStaff = Staff("Vincent", "Willson", "vincentpass", "vincent.willson@gmail.com")
        db.session.add(newStaff)
        db.session.commit()
        assert newStaff.email == "vincent.willson@gmail.com"

        findStaff = get_staff_by_email("vincent.willson@gmail.com")

        print("Found Staff Info:" , findStaff) #Testing Ou


