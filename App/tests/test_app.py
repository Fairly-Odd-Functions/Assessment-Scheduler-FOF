from datetime import date
from App.main import create_app
import pytest, logging, unittest
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
    Written by Katoya Ottley (stu-dent101)
    Task 08.1.1. Admin Unit Tests Implementation
    Task 08.1.2. Staff Unit Tests Implementation
    Task 08.1.3. User Unit Tests Implementation
    Task 08.1.4. Course Unit Tests Implementation
    Task 08.1.5. Semester Unit Tests Implementation
    Task 08.1.6. Program Unit Tests Implementation
>>>>>>> origin/08.1.6-Program-Unit-Tests-Implementation
'''

class AdminUnitTest(unittest.TestCase):
    
    # UNIT TEST - #1: Create Admin
    def test_unit_01_create_admin(self):
        admin = Admin("Jane", "Doe", "janepass", "jane.doe@gmail.com")
        assert admin.email == "jane.doe@gmail.com"

    # UNIT TEST - #2: Admin JSON
    def test_unit_02_admin_json(self):
        adminUser1 = Admin ("Star", "Light", "starpass", "star.light@gmail.com")
        admin_json = adminUser1.get_json()
        self.assertDictEqual({"firstName": "Star",
                              "lastName": "Light",
                              "email": "star.light@gmail.com"}, admin_json)

class StaffUnitTest(unittest.TestCase):

    # UNIT TEST - #3: Register Staff
    def test_unit_03_register_staff(self):
        newStaff = Staff("Greg", "Holder", "gregpass", "greg.holder@gmail.com")
        assert newStaff.email == "greg.holder@gmail.com"

    # UNIT TEST - #4: Staff JSON
    def test_unit_04_staff_json(self):
        newStaff = Staff ("Sam", "Jane", "sampass", "sam.jane@gmail.com")
        staff_json = newStaff.get_json()
        self.assertDictEqual({"first_name": "Sam",
                              "last_name": "Jane",
                              "email": "sam.jane@gmail.com"}, staff_json)

class UserUnitTest(unittest.TestCase):

    # UNIT TEST - #5: Create User
    def test_unit_5_create_user(self):
        user = User("Hope", "Ice", "hopepass", "hope.ice@gmail.com", "staff" )
        assert user.email == "hope.ice@gmail.com"
    
    # UNIT TEST - #6: Set Password
    def test_unit_6_set_password(self):
        password = "sampass"
        staff = User("Sam", "Smit", "sampass", "sam.smith@gmail.com", "staff")
        assert staff.password != password

    # UNIT TEST - #7: Check Password
    def test_unit_7_check_password(self):
        password = "janepass"
        staff = User("Jane", "Doe", "janepass", "jane.doeh@gmail.com", "staff")
        assert staff.check_password(password)

class CourseUnitTest(unittest.TestCase):

    # UNIT TEST - #8: Create Course
    def test_unit_08_create_course(self):
        newCourse = Course("COMP 1601", "Computer Programming I", 3 , "A level one programming course", 1)
        assert newCourse.courseCode == "COMP 1601"

    # UNIT TEST - #9: Course JSON
    def test_unit_09_course_json(self):
        newCourse = Course("COMP 1602", "Computer Programming II", 3 , "A level one programming course", 1)
        course_json = newCourse.get_json()
        self.assertDictEqual({"courseCode": "COMP 1602",
                              "courseTitle": "Computer Programming II",
                              "courseCredits": 3,
                              "courseDescription": "A level one programming course",
                              "courseLevel" : 1}, course_json)

#UNIT TEST 8 & 9
#UNIT TEST 10 & 11

class ProgrammeUnitTest(unittest.TestCase):

    # UNIT TEST - #12: Create Programme
    def test_unit_12_create_programme(self):
        newProgramme = Programme("Mathematics", "Learn all about numbers")
        assert newProgramme.programmeTitle == "Mathematics"

    # UNIT TEST - #13: Programme JSON
    def test_unit_13_programme_json(self):
        newProgramme = Programme("Finance", "Learn all about money")
        programme_json = newProgramme.get_json()
        self.assertDictEqual({"programmeID": newProgramme.programmeID,
                              "programmeTitle": "Finance",
                              "programmeDescription": "Learn all about money"}, programme_json)

'''
    Integration Tests
    Written by Daniel Young (DaNJO-Y)
    Task 08.2.1. User Integration Tests Implementation
    Task 08.2.2. Staff Integration Tests Implementation
    Task 08.2.3. Admin Integration Tests Implementation
    Task 08.2.4. Course Integration Tests Implementation
    Task 08.2.5. Semester Integration Tests Implementation
'''

class UserIntegrationTests(unittest.TestCase):
    # def test_integration_01_authenticate_user_valid(self):
    #     new_user = create_user("Robert", "Watson", "robpass", "rob22@email.com", "staff")
    #     response = login_user(new_user)
    #     assert response is not None

    def test_integration_02_get_user_invalid(self):
        create_user("Lily", "Daisy", "daisypass", "daisy35@email.com", "staff")
        new_user = get_user("daisy35@email.com","notdaisypass")
        assert new_user is None

class StaffIntegrationTests(unittest.TestCase):
    def test_integration_03_add_staff(self):
        new_staff = register_staff("Richard", "Maxwell", "maxpass", "max23@email.com")
        second_new_staff = register_staff("Terry", "Frey", "terrypass", "terry45@email.com")
        assert new_staff.email == "max23@email.com"
        assert second_new_staff.email == "terry45@email.com"

    def test_integration_04_get_staff_users_json(self):
        register_staff("Richard", "Maxwell", "maxpass", "max23@email.com")
        register_staff("Terry", "Frey", "terrypass", "terry45@email.com")
        register_staff("Hailey", "Vogue", "voguepass", "vogue87@email.com")
        staff = get_all_staff_users_json()
        self.assertListEqual([{"first_name": "Richard",
                                "last_name": "Maxwell",
                                "email": "max23@email.com"},

                            {"first_name": "Terry",
                                "last_name": "Frey",
                                "email": "terry45@email.com"},

                            {"first_name": "Hailey",
                                "last_name": "Vogue",
                                "email": "vogue87@email.com"}], staff)

class AdminIntegrationTests(unittest.TestCase):
    def test_integration_05_create_admin(self):
        admin = create_admin("Jill", "Hillington", "jillpass", "jillandhills@email.com")
        assert admin.email == "jillandhills@email.com"

    def test_integration_06_get_all_admin_users_json(self):
        create_admin("Jill", "Hillington", "jillpass", "jillandhills@email.com")
        create_admin("David", "Johnson", "davepass", "davesquare@email.com")
        admin_users = get_all_admin_users_json()
        self.assertListEqual([{"firstName" : "Jill",
                            "lastName" : "Hillington",
                            "email" : "jillandhills@email.com"},

                            {"firstName" : "David",
                            "lastName" : "Johnson",
                            "email" : "davesquare@email.com"}], admin_users)

class CourseIntegrationTests(unittest.TestCase):
    def test_integration_07_add_course(self):
        add_course("12345","Theory of Maths",3,"Introduction to the nature of numbers, functions and proofs fo University",1)
        course = get_course("12345")
        self.assertDictEqual({"courseCode" : "12345",
                            "courseTitle" : "Theory of Maths",
                            "courseCredits" : 3,
                            "courseDescription" : "Introduction to the nature of numbers, functions and proofs fo University",
                            "courseLevel" : 1}, course)

    def test_integration_08_list_courses(self):
        add_course("12345","Theory of Maths",3,"Introduction to the nature of numbers, functions and proofs fo University",1)
        add_course("12300","Governance and Technology",4,"Welcome to the harmony of technology in the field of Government arts",2)
        courses = list_courses()
        self.assertListEqual([{"courseCode" : "12345",
                            "courseTitle" : "Theory of Maths",
                            "courseCredits" : 3,
                            "courseDescription" : "Introduction to the nature of numbers, functions and proofs fo University",
                            "courseLevel" : 1},
                            
                            {"courseCode" : "12300",
                            "courseTitle" : "Governance and Technology",
                            "courseCredits" : 4,
                            "courseDescription" : "Welcome to the harmony of technology in the field of Government arts",
                            "courseLevel" : 2}], courses)

    def test_integration_09_add_course_assessment(self):
        add_course("12310","Governance and Culture",4,"Welcome to the study of cultural influence in the Government",3)
        assessment = Assessment("Governance and Culture Course Work Exam 1", "Course Work Exam", None, None)
        db.session.add(assessment)
        db.session.commit()
        message = add_course_assessment("12310", 1, None, None)
        assert message["Message"] == "Course and Assessment successfully associated"
        assert message["CourseAssessment"] == {"courseAssessmentID": 1,
                                "courseCode": "12310",
                                 "assessmentID": assessment.assessmentID,
                                 "startDate": None,
                                 "dueDate": None}
    
    def test_integration_10_list_course_assessment(self):
        add_course("12310","Governance and Culture",4,"Welcome to the study of cultural influence in the Government",3)
        assessment1 = Assessment("Governance and Culture Course Work Exam 1", "Course Work Exam", None, None)
        assessment2 = Assessment("Governance and Culture Course Work Exam 2", "Course Work Exam", None, None)
        db.session.add(assessment1)
        db.session.add(assessment2)
        db.session.commit()
        add_course_assessment(courseCode="12310", assessmentID=1, startDate=None, dueDate=None)
        add_course_assessment(courseCode="12310", assessmentID=2, startDate=None, dueDate=None)
        message = list_course_assessments("12310")
        print(message)
        assert message["CourseAssessments"] == [{"courseAssessmentID": 1,
                                "courseCode": "12310",
                                 "assessmentID": 1,
                                 "startDate": None,
                                 "dueDate": None},

                                 {"courseAssessmentID": 2,
                                "courseCode": "12310",
                                 "assessmentID": 2,
                                 "startDate": None,
                                 "dueDate": None}]

    def test_integration_11_add_course_offering(self):
        add_course("13542","Database Design",3,"Welcome to the study of designing databases",2)
        add_semester("Semester 1", "2024-2025", date(2024, 9, 4), date(2024, 12, 20))
        message = add_course_offering("13542","Semester 1","2024-2025",0)
        assert message["Message"] == "Course offering added successfully"
        assert message["CourseOffering"] == {"offeringID": 1,
                                             "courseCode": "13542",
                                             "semesterID": 1,
                                             "semester": {"semester_name":"Semester 1",
                                                          "academicYear": "2024-2025",
                                                          "startDate": date(2024, 9, 4),
                                                          "endDate": date(2024, 12, 20)},
                                             "totalStudentsEnrolled": 0}

    """
    NB: The courseStaff Model & Controller Has An Update 
    So When That's Approved This'll Be Refactored - JaleneA

    def test_integration_12_add_course_staff(self):
        add_course("13512","UI Fundamentals", 3, "Learn the basics of User Interface in Society",3)
        add_semester("Semester 1", "2024-2025", date(2024, 9, 4), date(2024, 12, 20))
        new_staff = register_staff("John", "Williams", "johnpass", "john22@email.com")
        message = add_course_staff("13512", "Semester 1", "2024-2025", new_staff.staffID)
        assert message["Message"] == "Staff successfully assigned to the course"
        assert message["CourseStaff"] == {"courseCode": "13512",
                                          "staffID": new_staff.staffID,
                                          "staffEmail": new_staff.email}
    """

    def test_integration_13_add_course_to_programme(self):
        add_course("20001","UI Fundamentals 2", 6, "Learn the basics of User Interface in Society and beyound",4)
        programme = Programme("Bsc. Information Technology", "4 year degree to allow students to be introduced to the sector of information technology")
        db.session.add(programme)
        db.session.commit()
        message = add_course_to_programme("20001", 1)
        assert message["Message"] == "Course successfully added to the programme"
        assert message["CourseProgramme"] == {'courseProgrammeID': 1,
                                              'programmeID': programme.programmeID,
                                              'courseCode': "20001"}

class SemesterIntegrationTests(unittest.TestCase):
    def test_integration_14_add_semester(self):
        message = add_semester("Semester 2", "2024-2025", date(2024, 9, 4), date(2024, 12, 20))
        assert message["New Semester Added"] == {"semesterID" : 1, "semesterName" : "Semester 2"}

    def test_integration_15_get_semester(self):
       add_semester("Semester 3", "2024-2025", date(2024, 5, 15), date(2024, 7, 20))
       semester = get_semester("Semester 3", "2024-2025")
       self.assertDictEqual({"semester_name":"Semester 3",
                             "academicYear": "2024-2025",
                             "startDate": date(2024, 5, 15),
                             "endDate":date(2024, 7, 20)}, semester)