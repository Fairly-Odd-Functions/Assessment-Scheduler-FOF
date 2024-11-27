import os, tempfile, pytest, logging, unittest

from App.main import create_app
from App.database import db, create_db
#from App.views.auth import login
from App.models import User 
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
        user = create_user("Hope", "Ice", "hopepass", "hope.ice@gmail.com", "staff" )
        assert user.email == "hope.ice@gmail.com"

        #print("User Info:", user) #Testing Output
    

    #UNIT TEST - #20: Get All Admin Users
    def test_unit_20_get_all_admin_users(self):
        user = create_user("Jake", "Kim", "jakepass", "jake.kim@gmail.com", "admin")
        assert user.email == "jake.kim@gmail.com"

        user = create_user("Laim", "Mike", "liampass", "liam.mike@gmail.com", "admin" )
        assert user.email == "liam.mike@gmail.com"

        admins = get_all_admin_users()    

        #Testing Output
        '''
        print("Admin Users: ", admins)

        assert len(admins) == 2
        assert admins[0].email == "jake.kim@gmail.com"
        assert admins[1].email == "liam.mike@gmail.com"
        '''

    
    #UNIT TEST - #21: Get All Staff Users
    def test_unit_21_get_all_staff_users(self):
        user = create_user("Nate", "Open", "natepass", "nate.open@gmail.com", "staff")
        assert user.email == "nate.open@gmail.com"

        user = create_user("Peter", "Quick", "peterpass", "peter.quick@gmail.com", "staff" )
        assert user.email == "peter.quick@gmail.com"

        staff = get_all_staff_users()

        #Testing Output
        '''
        print("Admin Users: ", staff)

        assert len(staff) == 2
        assert staff[0].email == "nate.open@gmail.com"
        assert staff[1].email == "peter.quick@gmail.com"
        '''   

    #UNIT TEST - #22: Get All Admin Users JSON
    def test_unit_22_get_all_admin_users_json(self):
        user = create_user("Rese", "Tim", "resepass", "rese.tim@gmail.com", "admin")
        assert user.email == "rese.tim@gmail.com"

        user = create_user("Uma", "Vick", "umapass", "uma.vick@gmail.com", "admin" )
        assert user.email == "uma.vick@gmail.com"

        admins = get_all_admin_users_json()    

        #Testing Output
        '''
        print("Admin Users: ", admins)

        assert len(admins) == 2
        assert admins[0]['email'] == "rese.tim@gmail.com"
        assert admins[1]['email'] == "uma.vick@gmail.com"
        '''

    #UNIT TEST - #23: Get All Staff Users JSON
    def test_unit_23_get_all_staff_users_json(self):
        user = create_user("Willow", "Xym", "willowpass", "willow.xym@gmail.com", "staff")
        assert user.email == "willow.xym@gmail.com"

        user = create_user("Yahem", "Zim", "yahempass", "yahem.zim@gmail.com", "staff" )
        assert user.email == "yahem.zim@gmail.com"

        staff = get_all_staff_users_json()

        #Testing Output
        '''
        print("Admin Users: ", staff)

        assert len(staff) == 2
        assert staff[0]['email'] == "willow.xym@gmail.com"
        assert staff[1]['email'] == "yahem.zim@gmail.com"
        '''  


    #UNIT TEST - #24: Validate Staff Users
    def test_unit_24_validate_Staff(self):
        user = create_user("Mark", "Sandy", "markpass", "mark.sandy@gmail.com", "staff")
        assert user.email == "mark.sandy@gmail.com"

        staff = validate_Staff("mark.sandy@gmail.com", "markpass")

        #print("Valid Staff : ", staff) #Testing Output

    
    #UNIT TEST - #25: Validate Admin Users
    def test_unit_25_validate_Admin(self):
        user = create_user("Sammy", "Dan", "sammypass", "sammy.dan@gmail.com", "admin")
        assert user.email == "sammy.dan@gmail.com"

        staff = validate_Admin("sammy.dan@gmail.com", "sammypass")

        #print("Valid Admin : ", staff) #Testing Output