import os, tempfile, pytest, logging, unittest

from App.main import create_app
from App.database import db, create_db
#from App.views.auth import login
from App.models import Admin, Staff, User 
from App.controllers import ( #Admin Controller
    create_admin,
    get_all_admin_users,
    get_all_admin_users_json,
    update_admin,
    delete_admin,
    get_admin_by_email,
    get_all_admins,
)
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
from App.controllers import ( #User Controller
    create_user,
    get_all_admin_users,
    get_all_staff_users,
    get_all_admin_users_json,
    get_all_staff_users_json,
    validate_Staff,
    validate_Admin,
    get_user,
    get_userID,
)

LOGGER = logging.getLogger(__name__)

@pytest.fixture(autouse=True, scope="function") #was "module" changed to "function"
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.session.remove() #new line
    db.drop_all()

'''
    Unit Tests
'''

class AdminUnitTest(unittest.TestCase):
    
    #UNIT TEST - #1: Create Admin
    def test_unit_01_create_admin(self):
        admin = Admin ("Jane", "Doe", "janepass", "jane.doe@gmail.com")
        assert admin.email == "jane.doe@gmail.com"

        #print("Admin Info:", admin) #Testing Output

    
    #UNIT TEST - #2: Get All Admin Users
    def test_unit_02_get_all_admin_users(self):
        adminUser1 = Admin ("John", "Doe", "johnpass", "john.doe@gmail.com")
        adminUser2 = Admin ("Katie", "White", "katiepass", "katie.white@gmail.com")

        '''Testing Output
        db.session.add(adminUser1)
        db.session.add(adminUser2)
        db.session.commit()
        '''

        admins = get_all_admin_users()    

        '''Testing Output
        print("Admins: ", admins)

        assert len(admins) == 2
        assert admins[0].email == "john.doe@gmail.com"
        assert admins[1].email == "katie.white@gmail.com"
        '''


    #UNIT TEST - #3: Get All Admin Users
    def test_unit_03_get_all_admin_users_json(self):
        adminUser1 = Admin ("Star", "Light", "starpass", "star.light@gmail.com")
        adminUser2 = Admin ("Sunflower", "Rose", "sunflowerpass", "sunflower.rose@gmail.com")

        #Testing Output
        '''
        db.session.add(adminUser1)
        db.session.add(adminUser2)
        db.session.commit()
        '''
        
        admin_json = get_all_admin_users_json()

        #Testing Output
        '''
        print("Admins: ", admin_json)

        assert len(admin_json) == 2
        assert admin_json[0]['email'] == "star.light@gmail.com"
        assert admin_json[1]['email'] == "sunflower.rose@gmail.com"
        '''
    

    #UNIT TEST - #4: Get All Admin Users
    def test_unit_04_update_admin(self):
        admin = Admin ("Bill", "John", "billpass", "bill.john@gmail.com")
        db.session.add(admin)
        db.session.commit()
        
        assert admin.email == "bill.john@gmail.com"
        
        updateAdmin = update_admin("bill.john@gmail.com", "James", "Smith", "jamespass", "james.smith@gmail.com")
        assert updateAdmin.email == "james.smith@gmail.com"

        #print("Updated Admin Info:", updateAdmin) #Testing Output


    #UNIT TEST - #5: Delete an Admin
    def test_unit_05_delete_admin(self):
        admin = Admin ("Mario", "Blue", "mariopass", "mario.blue@gmail.com")
        db.session.add(admin)
        db.session.commit()

        assert admin.email == "mario.blue@gmail.com"

        deleteAdmin = delete_admin("mario.blue@gmail.com")

        #print("Deleted Admin Info:", deleteAdmin) #Testing Output

    #UNIT TEST - #6: Get Admin by Email
    def test_unit_06_get_admin_by_email(self):
        admin = Admin ("Sam", "Yellow", "sampass", "sam.yellow@gmail.com")
        db.session.add(admin)
        db.session.commit()
        assert admin.email == "sam.yellow@gmail.com"

        getAdmin = get_admin_by_email("sam.yellow@gmail.com")

        #print("Found Admin Info:", getAdmin) #Testing Output

    #UNIT TEST - #7: Get All Admins
    def test_unit_07_get_all_admins(self):
        adminUser1 = Admin ("Adam", "Bane", "adampass", "adam.bane@gmail.com")
        adminUser2 = Admin ("Carly", "Due", "carlypass", "carly.due@gmail.com")
        adminUser3 = Admin ("Ella", "Fisher", "ellapass", "ella.fisher@gmail.com")
        db.session.add(adminUser1)
        db.session.add(adminUser2)
        db.session.add(adminUser3)
        db.session.commit()
  
        admins = get_all_admins() 

        #Testing Output
        #print("All Admins: ", admins)

        assert len(admins) == 3
        assert admins[0].email == "adam.bane@gmail.com"
        assert admins[1].email == "carly.due@gmail.com"
        assert admins[2].email == "ella.fisher@gmail.com"
        