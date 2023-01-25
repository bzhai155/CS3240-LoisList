# Create your tests here.
from django.test import TestCase, Client, RequestFactory
from list_app.models import Student, AcademicClass, Rating, ShoppingCart, Comment, CalenderModel
from list_app.views import AuthenticateAddCalender
from django.contrib.auth.models import User
class LogInTest(TestCase):
    def test_response(self):
        c = Client()
        response = c.get('')
        self.assertTrue(response.status_code==200)

    # -test everytime we use API

class StudentTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        request = self.factory.post('/', secure=True)
        request.user = User.objects.create(username="test1")
        request.user = User.objects.create(username="test2")
    
    def test_createStudent(self):
        u = User.objects.get(username="test1")
        Student.objects.create(user = u)
        f = Student.objects.get(user = u)
        self.assertEqual(Student.objects.count(), 1)
        self.assertEqual(f.user, u)
        self.assertEqual(f.user.username, "test1")
    
    def test_defaultStudent(self):
        u = User.objects.get(username="test1")
        Student.objects.create(user = u)
        f = Student.objects.get(user = u)
        self.assertEqual(Student.objects.count(), 1)
        self.assertEqual(f.user, u)
        self.assertEqual(f.username, "")
        self.assertEqual(f.first_name, "")
        self.assertEqual(f.last_name, "")
        self.assertEqual(f.email, "")
    
    def test_addFriend(self):
        u1 = User.objects.get(username="test1")
        Student.objects.create(user = u1)
        p1 = Student.objects.get(user = u1)
        u2 = User.objects.get(username="test2")
        Student.objects.create(user = u2)
        p2 = Student.objects.get(user = u2)
        
        #no friends 
        self.assertEqual(p1.friends.count(),0)
        p1.friends.add(p2)
        
        #check for differences
        self.assertEqual(Student.objects.count(), 2)
        self.assertEqual(p1.friends.count(),1)
        f = p1.friends.get(user = u2)
        
        #make sure nothing is edited
        self.assertEqual(f.user.username, "test2")
        self.assertEqual(f.user, u2)
        self.assertEqual(f.username, "")
        self.assertEqual(f.first_name, "")
        self.assertEqual(f.last_name, "")
        self.assertEqual(f.email, "")

    def test_removeFriend(self):
        u1 = User.objects.get(username="test1")
        Student.objects.create(user = u1)
        p1 = Student.objects.get(user = u1)
        u2 = User.objects.get(username="test2")
        Student.objects.create(user = u2)
        p2 = Student.objects.get(user = u2)
        
        #no friends 
        self.assertEqual(p1.friends.count(),0)
        p1.friends.add(p2)
        
        #see if its added
        self.assertEqual(Student.objects.count(), 2)
        self.assertEqual(p1.friends.count(),1)
        p1.friends.remove(p2)
        
        #make sure it was removed
        self.assertEqual(Student.objects.count(), 2)
        self.assertEqual(p1.friends.count(),0)

        #make sure nothing is edited
        self.assertEqual(p1.user.username, "test1")
        self.assertEqual(p1.user, u1)
        self.assertEqual(p1.username, "")
        self.assertEqual(p1.first_name, "")
        self.assertEqual(p1.last_name, "")
        self.assertEqual(p1.email, "")
        self.assertEqual(p2.user.username, "test2")
        self.assertEqual(p2.user, u2)
        self.assertEqual(p2.username, "")
        self.assertEqual(p2.first_name, "")
        self.assertEqual(p2.last_name, "")
        self.assertEqual(p2.email, "")


class CommentTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        request = self.factory.post('/', secure=True)
        request.user = User.objects.create(username="test1")
        request.user = User.objects.create(username="test2")
        u1 = User.objects.get(username="test1")
        Student.objects.create(user = u1)
        u2 = User.objects.get(username="test2")
        Student.objects.create(user = u2)
    
    def test_createComment(self):
        u1 = User.objects.get(username="test1")
        f1 = Student.objects.get(user = u1)
        u2 = User.objects.get(username="test2")
        f2 = Student.objects.get(user = u1)
        
        #check nothing exist yet
        self.assertEqual(Comment.objects.count(), 0)
        
        #make a comment and check
        Comment.objects.create(username = u1.username, content='testing', to_who=f1)
        self.assertEqual(Comment.objects.count(), 1)
        
        c1 = Comment.objects.get(username=u1.username)
        self.assertEqual(c1.username, u1.username)
        self.assertEqual(c1.content, 'testing')
        self.assertEqual(c1.to_who, f1)
    
    def test_defaultComment(self):
        u1 = User.objects.get(username="test1")
        f1 = Student.objects.get(user = u1)
        u2 = User.objects.get(username="test2")
        f2 = Student.objects.get(user = u1)
        
        #check nothing exist yet
        self.assertEqual(Comment.objects.count(), 0)
        
        #make a comment and check
        Comment.objects.create(to_who=f1)
        self.assertEqual(Comment.objects.count(), 1)
        
        c1 = Comment.objects.get(to_who=f1)
        self.assertEqual(c1.username, '')
        self.assertEqual(c1.content, '')
        self.assertEqual(c1.to_who, f1)
    
    

class RatingTest(TestCase):
    def test_create_question(self): # default question
        rate = Rating.objects.create()
        rate.save()
        self.assertEqual(Rating.objects.count(), 1)
        self.assertEqual(rate.GPA, 3.0)
        self.assertEqual(rate.rating, 0)

    def test_specify_whichClass(self):
        class1 = "CS 3240"
        rate = Rating.objects.create(whichClass = class1)
        rate.save()
        self.assertEqual(rate.whichClass, class1)
        rate1 = Rating.objects.get(whichClass=class1)
        self.assertEqual(rate, rate1)

    def test_filter_classes(self):
        class1 = "CS 3240"
        rate2 = Rating.objects.create(rating=2, whichClass=class1)
        rate2.save()
        ratings = Rating.objects.filter(whichClass=class1)
        for r in ratings:
            self.assertEqual(r.whichClass, class1)

class AcademicClassTest(TestCase):
    def setUp(self):
        AcademicClass.objects.create(instructor_name = "teacher", course_number = 99999, 
        semester_code = 9999, course_section = "001", 
        subject = "TC", catalog_number = "9999", description = "Testcase1",
        units = "3", component = "LEC", class_capacity = 99, wait_list = 0,
        enrollment_total = 0, enrollment_available = 99,
        days = "MoWeFr", start_time = "17.00.00.000000-05:00", end_time = "18.15.00.000000-05:00",
        facility_description = "Olsson Hall 009")
        
        
    def test_create_AcademicClass(self):
        t2 = AcademicClass.objects.get(course_number = 99999)
        t2.course_number = 00000
        t2.save()
        f = AcademicClass.objects.get(course_number=00000)
        #check if a new object is made
        self.assertEqual(AcademicClass.objects.count(), 2)
        self.assertEqual(f.course_number, 00000)
        
    def test_update_AcademicClass(self):
        t1 = AcademicClass.objects.get(course_number = 99999)
        t1.semester_code = '0'
        t1.save()
        f = AcademicClass.objects.get(course_number=99999)
        #make sure a new object isnt made
        self.assertEqual(AcademicClass.objects.count(), 1)
        #make sure nothing is changed
        self.assertEqual(f.course_number, 99999)
        self.assertEqual(f.semester_code, '0')
    
    def test_create_emptyclass(self):
        AcademicClass.objects.create()
        #check if a obejct was made
        self.assertEqual(AcademicClass.objects.count(), 2)
        #should be set to defaults
        f = AcademicClass.objects.get(course_number='00000')
        self.assertEqual(f.instructor_name, 'D')
        self.assertEqual(f.instructor_email, 'D')
        self.assertEqual(f.course_number, 0)
        self.assertEqual(f.semester_code, '0000')
        self.assertEqual(f.course_section, '0000')
        self.assertEqual(f.subject, '0000')
        self.assertEqual(f.catalog_number,'0000' )
        self.assertEqual(f.description, '0000')
        self.assertEqual(f.units, '0000')
        self.assertEqual(f.component, '0000')
        self.assertEqual(f.class_capacity, 0)
        self.assertEqual(f.wait_list, 0)
        self.assertEqual(f.wait_cap, 0)
        self.assertEqual(f.enrollment_total, 0)
        self.assertEqual(f.enrollment_available, 0)
        self.assertEqual(f.topic, '')
        self.assertEqual(f.days, '')
        self.assertEqual(f.start_time, '')
        self.assertEqual(f.end_time, '')
        self.assertEqual(f.facility_description, '')


class ShoppingCartTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        request = self.factory.post('/', secure=True)
        request.user = User.objects.create(username="test1")
        request.user = User.objects.create(username="test2")
        AcademicClass.objects.create(instructor_name = "teacher", instructor_email = "teacher@gmail.com", course_number = 99999, 
        semester_code = 9999, course_section = "001", 
        subject = "TC", catalog_number = "9999", description = "Testcase1",
        units = "3", component = "LEC", class_capacity = 99, wait_list = 0, wait_cap = 0,
        enrollment_total = 0, enrollment_available = 99,
        days = "MoWeFr", start_time = "17.00.00.000000-05:00", end_time = "18.15.00.000000-05:00",
        facility_description = "Olsson Hall 009")
        
        AcademicClass.objects.create(instructor_name = "teacher1", instructor_email = "teacher1@gmail.com", course_number = 99998, 
        semester_code = 9999, course_section = "001", 
        subject = "TC", catalog_number = "9998", description = "Testcase2",
        units = "3", component = "LEC", class_capacity = 99, wait_list = 0, wait_cap = 0,
        enrollment_total = 0, enrollment_available = 99,
        days = "TuTh", start_time = "17.00.00.000000-05:00", end_time = "18.15.00.000000-05:00",
        facility_description = "Olsson Hall 009")
        AcademicClass.objects.create()
    
    def test_createShoppingCart(self):
        #check for empty
        self.assertEqual(CalenderModel.objects.count(), 0)
        
        #create
        u = User.objects.get(username="test1")
        ShoppingCart.objects.create(user = u)
        f = ShoppingCart.objects.get(user = u)
        self.assertEqual(ShoppingCart.objects.count(), 1)
        self.assertEqual(f.user, u)
        self.assertEqual(f.user.username, "test1")
    
    def test_addClass(self):
        u = User.objects.get(username="test1")
        ShoppingCart.objects.create(user = u)
        t1 = ShoppingCart.objects.get(user = u)
        c = AcademicClass.objects.get(course_number = 0)
        t1.classes.add(c)
        self.assertEqual(ShoppingCart.objects.count(), 1)
        self.assertEqual(t1.classes.count(),1)
        f = t1.classes.get(course_number = 0)
        #make sure nothing is edited
        self.assertEqual(f.instructor_name, 'D')
        self.assertEqual(f.instructor_email, 'D')
        self.assertEqual(f.course_number, 0)
        self.assertEqual(f.semester_code, '0000')
        self.assertEqual(f.course_section, '0000')
        self.assertEqual(f.subject, '0000')
        self.assertEqual(f.catalog_number,'0000' )
        self.assertEqual(f.description, '0000')
        self.assertEqual(f.units, '0000')
        self.assertEqual(f.component, '0000')
        self.assertEqual(f.class_capacity, 0)
        self.assertEqual(f.wait_list, 0)
        self.assertEqual(f.wait_cap, 0)
        self.assertEqual(f.enrollment_total, 0)
        self.assertEqual(f.enrollment_available, 0)
        self.assertEqual(f.topic, '')
        self.assertEqual(f.days, '')
        self.assertEqual(f.start_time, '')
        self.assertEqual(f.end_time, '')
        self.assertEqual(f.facility_description, '')
        
    def test_removeClass(self):
        u = User.objects.get(username="test1")
        ShoppingCart.objects.create(user = u)
        t1 = ShoppingCart.objects.get(user = u)
        c = AcademicClass.objects.get(course_number = 0)
        #check for empty
        self.assertEqual(t1.classes.count(),0)
        #add
        t1.classes.add(c)
        self.assertEqual(ShoppingCart.objects.count(), 1)
        self.assertEqual(t1.classes.count(),1)
        f = t1.classes.get(course_number = 0)
        
        #remove
        t1.classes.remove(f)
        self.assertEqual(t1.classes.count(),0)
        
        #make sure nothing is edited
        self.assertEqual(f.instructor_name, 'D')
        self.assertEqual(f.instructor_email, 'D')
        self.assertEqual(f.course_number, 0)
        self.assertEqual(f.semester_code, '0000')
        self.assertEqual(f.course_section, '0000')
        self.assertEqual(f.subject, '0000')
        self.assertEqual(f.catalog_number,'0000' )
        self.assertEqual(f.description, '0000')
        self.assertEqual(f.units, '0000')
        self.assertEqual(f.component, '0000')
        self.assertEqual(f.class_capacity, 0)
        self.assertEqual(f.wait_list, 0)
        self.assertEqual(f.wait_cap, 0)
        self.assertEqual(f.enrollment_total, 0)
        self.assertEqual(f.enrollment_available, 0)
        self.assertEqual(f.topic, '')
        self.assertEqual(f.days, '')
        self.assertEqual(f.start_time, '')
        self.assertEqual(f.end_time, '')
        self.assertEqual(f.facility_description, '')
        
    def test_add2Class(self):
        u = User.objects.get(username="test1")
        ShoppingCart.objects.create(user = u)
        t1 = ShoppingCart.objects.get(user = u)
        c1 = AcademicClass.objects.get(course_number = 99999)
        #check for empty
        self.assertEqual(t1.classes.count(),0)
        #add
        t1.classes.add(c1)
        self.assertEqual(ShoppingCart.objects.count(), 1)
        self.assertEqual(t1.classes.count(),1)
        f = t1.classes.get(course_number = 99999)
        
        c2 = AcademicClass.objects.get(course_number = 99998)
        #check for only 1
        self.assertEqual(t1.classes.count(),1)
        t1.classes.add(c2)
        self.assertEqual(ShoppingCart.objects.count(), 1)
        self.assertEqual(t1.classes.count(),2)
        f1 = t1.classes.get(course_number = 99998)
        
        #make sure nothing is edited
        self.assertEqual(f.instructor_name, 'teacher')
        self.assertEqual(f.instructor_email, 'teacher@gmail.com')
        self.assertEqual(f.course_number, 99999)
        self.assertEqual(f.semester_code, '9999')
        self.assertEqual(f.course_section, '001')
        self.assertEqual(f.subject, 'TC')
        self.assertEqual(f.catalog_number,'9999' )
        self.assertEqual(f.description, 'Testcase1')
        self.assertEqual(f.units, '3')
        self.assertEqual(f.component, 'LEC')
        self.assertEqual(f.class_capacity, 99)
        self.assertEqual(f.wait_list, 0)
        self.assertEqual(f.wait_cap, 0)
        self.assertEqual(f.enrollment_total, 0)
        self.assertEqual(f.enrollment_available, 99)
        self.assertEqual(f.topic, '')
        self.assertEqual(f.days, 'MoWeFr')
        self.assertEqual(f.start_time, '17.00.00.000000-05:00')
        self.assertEqual(f.end_time, '18.15.00.000000-05:00')
        self.assertEqual(f.facility_description, 'Olsson Hall 009')
        
        
        self.assertEqual(f1.instructor_name, 'teacher1')
        self.assertEqual(f1.instructor_email, 'teacher1@gmail.com')
        self.assertEqual(f1.course_number, 99998)
        self.assertEqual(f1.semester_code, '9999')
        self.assertEqual(f1.course_section, '001')
        self.assertEqual(f1.subject, 'TC')
        self.assertEqual(f1.catalog_number,'9998')
        self.assertEqual(f1.description, 'Testcase2')
        self.assertEqual(f1.units, '3')
        self.assertEqual(f1.component, 'LEC')
        self.assertEqual(f1.class_capacity, 99)
        self.assertEqual(f1.wait_list, 0)
        self.assertEqual(f1.wait_cap, 0)
        self.assertEqual(f1.enrollment_total, 0)
        self.assertEqual(f1.enrollment_available, 99)
        self.assertEqual(f1.topic, '')
        self.assertEqual(f1.days, 'TuTh')
        self.assertEqual(f1.start_time, '17.00.00.000000-05:00')
        self.assertEqual(f1.end_time, '18.15.00.000000-05:00')
        self.assertEqual(f1.facility_description, 'Olsson Hall 009')
        
        
        
class CalenderTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        request = self.factory.post('/', secure=True)
        request.user = User.objects.create(username="test1")
        request.user = User.objects.create(username="test2")
        AcademicClass.objects.create(instructor_name = "teacher", instructor_email = "teacher@gmail.com", course_number = 99999, 
        semester_code = 9999, course_section = "001", 
        subject = "TC", catalog_number = "9999", description = "Testcase1",
        units = "3", component = "LEC", class_capacity = 99, wait_list = 0, wait_cap = 0,
        enrollment_total = 0, enrollment_available = 99,
        days = "MoWeFr", start_time = "17.00.00.000000-05:00", end_time = "18.15.00.000000-05:00",
        facility_description = "Olsson Hall 009")
        
        #no conflicts
        AcademicClass.objects.create(instructor_name = "teacher1", instructor_email = "teacher1@gmail.com", course_number = 99998, 
        semester_code = 9999, course_section = "001", 
        subject = "TC", catalog_number = "9998", description = "Testcase2",
        units = "3", component = "LEC", class_capacity = 99, wait_list = 0, wait_cap = 0,
        enrollment_total = 0, enrollment_available = 99,
        days = "TuTh", start_time = "17.00.00.000000-05:00", end_time = "18.15.00.000000-05:00",
        facility_description = "Olsson Hall 009")
        
        #conflicting time (overlapping time) 
        AcademicClass.objects.create(instructor_name = "teacher2", instructor_email = "teacher2@gmail.com", course_number = 99997, 
        semester_code = 9999, course_section = "001", 
        subject = "TC", catalog_number = "9997", description = "Testcase2",
        units = "3", component = "LEC", class_capacity = 99, wait_list = 0, wait_cap = 0,
        enrollment_total = 0, enrollment_available = 99,
        days = "MoWeFr", start_time = "17.00.00.000000-05:00", end_time = "18.15.00.000000-05:00",
        facility_description = "Olsson Hall 009")
        
        #same course (course number same)
        AcademicClass.objects.create(instructor_name = "teacher3", instructor_email = "teacher3@gmail.com", course_number = 99996, 
        semester_code = 9999, course_section = "002", 
        subject = "TC", catalog_number = "9999", description = "Testcase3",
        units = "3", component = "LEC", class_capacity = 99, wait_list = 0, wait_cap = 0,
        enrollment_total = 0, enrollment_available = 99,
        days = "TuTh", start_time = "17.00.00.000000-05:00", end_time = "18.15.00.000000-05:00",
        facility_description = "Olsson Hall 009")
        
        
        AcademicClass.objects.create()
    
    def test_createCalender(self):
         #check for empty
        self.assertEqual(CalenderModel.objects.count(), 0)
        
        #create
        u = User.objects.get(username="test1")
        CalenderModel.objects.create(user = u)
        f = CalenderModel.objects.get(user = u)
        self.assertEqual(CalenderModel.objects.count(), 1)
        self.assertEqual(f.user, u)
        self.assertEqual(f.user.username, "test1")
    
    def test_addClass(self):
        u = User.objects.get(username="test1")
        CalenderModel.objects.create(user = u)
        t1 = CalenderModel.objects.get(user = u)
        c = AcademicClass.objects.get(course_number = 0)
        
        #check for empty
        self.assertEqual(t1.classes.count(),0)
        
        #add
        t1.classes.add(c)
        self.assertEqual(CalenderModel.objects.count(), 1)
        self.assertEqual(t1.classes.count(),1)
        f = t1.classes.get(course_number = 0)
        #make sure nothing is edited
        self.assertEqual(f.instructor_name, 'D')
        self.assertEqual(f.instructor_email, 'D')
        self.assertEqual(f.course_number, 0)
        self.assertEqual(f.semester_code, '0000')
        self.assertEqual(f.course_section, '0000')
        self.assertEqual(f.subject, '0000')
        self.assertEqual(f.catalog_number,'0000' )
        self.assertEqual(f.description, '0000')
        self.assertEqual(f.units, '0000')
        self.assertEqual(f.component, '0000')
        self.assertEqual(f.class_capacity, 0)
        self.assertEqual(f.wait_list, 0)
        self.assertEqual(f.wait_cap, 0)
        self.assertEqual(f.enrollment_total, 0)
        self.assertEqual(f.enrollment_available, 0)
        self.assertEqual(f.topic, '')
        self.assertEqual(f.days, '')
        self.assertEqual(f.start_time, '')
        self.assertEqual(f.end_time, '')
        self.assertEqual(f.facility_description, '')
        
    def test_removeClass(self):
        u = User.objects.get(username="test1")
        CalenderModel.objects.create(user = u)
        t1 = CalenderModel.objects.get(user = u)
        c = AcademicClass.objects.get(course_number = 0)
        #check for empty
        self.assertEqual(t1.classes.count(),0)
        #add
        t1.classes.add(c)
        self.assertEqual(CalenderModel.objects.count(), 1)
        self.assertEqual(t1.classes.count(),1)
        f = t1.classes.get(course_number = 0)
        
        #remove
        t1.classes.remove(f)
        self.assertEqual(t1.classes.count(),0)
        
        #make sure nothing is edited
        self.assertEqual(f.instructor_name, 'D')
        self.assertEqual(f.instructor_email, 'D')
        self.assertEqual(f.course_number, 0)
        self.assertEqual(f.semester_code, '0000')
        self.assertEqual(f.course_section, '0000')
        self.assertEqual(f.subject, '0000')
        self.assertEqual(f.catalog_number,'0000' )
        self.assertEqual(f.description, '0000')
        self.assertEqual(f.units, '0000')
        self.assertEqual(f.component, '0000')
        self.assertEqual(f.class_capacity, 0)
        self.assertEqual(f.wait_list, 0)
        self.assertEqual(f.wait_cap, 0)
        self.assertEqual(f.enrollment_total, 0)
        self.assertEqual(f.enrollment_available, 0)
        self.assertEqual(f.topic, '')
        self.assertEqual(f.days, '')
        self.assertEqual(f.start_time, '')
        self.assertEqual(f.end_time, '')
        self.assertEqual(f.facility_description, '')
        
def test_add2Class(self):
        u = User.objects.get(username="test1")
        CalenderModel.objects.create(user = u)
        t1 = CalenderModel.objects.get(user = u)
        c1 = AcademicClass.objects.get(course_number = 99999)
        #check for empty
        self.assertEqual(t1.classes.count(),0)
        #add
        t1.classes.add(c1)
        self.assertEqual(CalenderModel.objects.count(), 1)
        self.assertEqual(t1.classes.count(),1)
        f = t1.classes.get(course_number = 99999)
        
        c2 = AcademicClass.objects.get(course_number = 99998)
        #check for only 1
        self.assertEqual(t1.classes.count(),1)
        
        #check to make sure validator works
        self.assertEqual(AuthenticateAddCalender(u, c2.course_number),0)
        
        t1.classes.add(c2)
        self.assertEqual(CalenderModel.objects.count(), 1)
        self.assertEqual(t1.classes.count(),2)
        f1 = t1.classes.get(course_number = 99998)
        
        #make sure nothing is edited
        self.assertEqual(f.instructor_name, 'teacher')
        self.assertEqual(f.instructor_email, 'teacher@gmail.com')
        self.assertEqual(f.course_number, 99999)
        self.assertEqual(f.semester_code, '9999')
        self.assertEqual(f.course_section, '001')
        self.assertEqual(f.subject, 'TC')
        self.assertEqual(f.catalog_number,'9999' )
        self.assertEqual(f.description, 'Testcase1')
        self.assertEqual(f.units, '3')
        self.assertEqual(f.component, 'LEC')
        self.assertEqual(f.class_capacity, 99)
        self.assertEqual(f.wait_list, 0)
        self.assertEqual(f.wait_cap, 0)
        self.assertEqual(f.enrollment_total, 0)
        self.assertEqual(f.enrollment_available, 99)
        self.assertEqual(f.topic, '')
        self.assertEqual(f.days, 'MoWeFr')
        self.assertEqual(f.start_time, '17.00.00.000000-05:00')
        self.assertEqual(f.end_time, '18.15.00.000000-05:00')
        self.assertEqual(f.facility_description, 'Olsson Hall 009')
        
        self.assertEqual(f1.instructor_name, 'teacher1')
        self.assertEqual(f1.instructor_email, 'teacher1@gmail.com')
        self.assertEqual(f1.course_number, 99998)
        self.assertEqual(f1.semester_code, '9999')
        self.assertEqual(f1.course_section, '001')
        self.assertEqual(f1.subject, 'TC')
        self.assertEqual(f1.catalog_number,'9999' )
        self.assertEqual(f1.description, 'Testcase1')
        self.assertEqual(f1.units, '3')
        self.assertEqual(f1.component, 'LEC')
        self.assertEqual(f1.class_capacity, 99)
        self.assertEqual(f1.wait_list, 0)
        self.assertEqual(f1.wait_cap, 0)
        self.assertEqual(f1.enrollment_total, 0)
        self.assertEqual(f1.enrollment_available, 99)
        self.assertEqual(f1.topic, '')
        self.assertEqual(f1.days, 'TuTh')
        self.assertEqual(f1.start_time, '17.00.00.000000-05:00')
        self.assertEqual(f1.end_time, '18.15.00.000000-05:00')
        self.assertEqual(f1.facility_description, 'Olsson Hall 009')

def test_2TimeConflictClass(self):
        u = User.objects.get(username="test1")
        CalenderModel.objects.create(user = u)
        t1 = CalenderModel.objects.get(user = u)
        c1 = AcademicClass.objects.get(course_number = 99999)
        #check for empty
        self.assertEqual(t1.classes.count(),0)
        #add
        t1.classes.add(c1)
        self.assertEqual(CalenderModel.objects.count(), 1)
        self.assertEqual(t1.classes.count(),1)
        f = t1.classes.get(course_number = 99999)
        
        c2 = AcademicClass.objects.get(course_number = 99997)
        #check for only 1
        self.assertEqual(t1.classes.count(),1)
        
        #check to make sure validator works
        self.assertEqual(AuthenticateAddCalender(u, c2.course_number),1)
        
        f1 = t1.classes.get(course_number = 99998)
        #make sure nothing is edited
        self.assertEqual(f.instructor_name, 'teacher')
        self.assertEqual(f.instructor_email, 'teacher@gmail.com')
        self.assertEqual(f.course_number, 99999)
        self.assertEqual(f.semester_code, '9999')
        self.assertEqual(f.course_section, '001')
        self.assertEqual(f.subject, 'TC')
        self.assertEqual(f.catalog_number,'9999' )
        self.assertEqual(f.description, 'Testcase1')
        self.assertEqual(f.units, '3')
        self.assertEqual(f.component, 'LEC')
        self.assertEqual(f.class_capacity, 99)
        self.assertEqual(f.wait_list, 0)
        self.assertEqual(f.wait_cap, 0)
        self.assertEqual(f.enrollment_total, 0)
        self.assertEqual(f.enrollment_available, 99)
        self.assertEqual(f.topic, '')
        self.assertEqual(f.days, 'MoWeFr')
        self.assertEqual(f.start_time, '17.00.00.000000-05:00')
        self.assertEqual(f.end_time, '18.15.00.000000-05:00')
        self.assertEqual(f.facility_description, 'Olsson Hall 009')
        
        self.assertEqual(f1.instructor_name, 'teacher2')
        self.assertEqual(f1.instructor_email, 'teacher2@gmail.com')
        self.assertEqual(f1.course_number, 99997)
        self.assertEqual(f1.semester_code, '9999')
        self.assertEqual(f1.course_section, '001')
        self.assertEqual(f1.subject, 'TC')
        self.assertEqual(f1.catalog_number,'9997' )
        self.assertEqual(f1.description, 'Testcase2')
        self.assertEqual(f1.units, '3')
        self.assertEqual(f1.component, 'LEC')
        self.assertEqual(f1.class_capacity, 99)
        self.assertEqual(f1.wait_list, 0)
        self.assertEqual(f1.wait_cap, 0)
        self.assertEqual(f1.enrollment_total, 0)
        self.assertEqual(f1.enrollment_available, 99)
        self.assertEqual(f1.topic, '')
        self.assertEqual(f1.days, 'MoWeFr')
        self.assertEqual(f1.start_time, '17.00.00.000000-05:00')
        self.assertEqual(f1.end_time, '18.15.00.000000-05:00')
        self.assertEqual(f1.facility_description, 'Olsson Hall 009')
        
        

def test_2CourseConflictClass(self):
        u = User.objects.get(username="test1")
        CalenderModel.objects.create(user = u)
        t1 = CalenderModel.objects.get(user = u)
        c1 = AcademicClass.objects.get(course_number = 99999)
        #check for empty
        self.assertEqual(t1.classes.count(),0)
        #add
        t1.classes.add(c1)
        self.assertEqual(CalenderModel.objects.count(), 1)
        self.assertEqual(t1.classes.count(),1)
        f = t1.classes.get(course_number = 99999)
        
        c2 = AcademicClass.objects.get(course_number = 99996)
        #check for only 1
        self.assertEqual(t1.classes.count(),1)
        
        #check to make sure validator works
        self.assertEqual(AuthenticateAddCalender(u, c2.course_number),2)
        
        f1 = t1.classes.get(course_number = 99996)
        #make sure nothing is edited
        self.assertEqual(f.instructor_name, 'teacher')
        self.assertEqual(f.instructor_email, 'teacher@gmail.com')
        self.assertEqual(f.course_number, 99999)
        self.assertEqual(f.semester_code, '9999')
        self.assertEqual(f.course_section, '001')
        self.assertEqual(f.subject, 'TC')
        self.assertEqual(f.catalog_number,'9999' )
        self.assertEqual(f.description, 'Testcase1')
        self.assertEqual(f.units, '3')
        self.assertEqual(f.component, 'LEC')
        self.assertEqual(f.class_capacity, 99)
        self.assertEqual(f.wait_list, 0)
        self.assertEqual(f.wait_cap, 0)
        self.assertEqual(f.enrollment_total, 0)
        self.assertEqual(f.enrollment_available, 99)
        self.assertEqual(f.topic, '')
        self.assertEqual(f.days, 'MoWeFr')
        self.assertEqual(f.start_time, '17.00.00.000000-05:00')
        self.assertEqual(f.end_time, '18.15.00.000000-05:00')
        self.assertEqual(f.facility_description, 'Olsson Hall 009')
        
        self.assertEqual(f1.instructor_name, 'teacher3')
        self.assertEqual(f1.instructor_email, 'teacher3@gmail.com')
        self.assertEqual(f1.course_number, 99996)
        self.assertEqual(f1.semester_code, '9999')
        self.assertEqual(f1.course_section, '002')
        self.assertEqual(f1.subject, 'TC')
        self.assertEqual(f1.catalog_number,'9999' )
        self.assertEqual(f1.description, 'Testcase3')
        self.assertEqual(f1.units, '3')
        self.assertEqual(f1.component, 'LEC')
        self.assertEqual(f1.class_capacity, 99)
        self.assertEqual(f1.wait_list, 0)
        self.assertEqual(f1.wait_cap, 0)
        self.assertEqual(f1.enrollment_total, 0)
        self.assertEqual(f1.enrollment_available, 99)
        self.assertEqual(f1.topic, '')
        self.assertEqual(f1.days, 'TuTh')
        self.assertEqual(f1.start_time, '17.00.00.000000-05:00')
        self.assertEqual(f1.end_time, '18.15.00.000000-05:00')
        self.assertEqual(f1.facility_description, 'Olsson Hall 009')
        
        
def test_SameCourseTwice(self):
        u = User.objects.get(username="test1")
        CalenderModel.objects.create(user = u)
        t1 = CalenderModel.objects.get(user = u)
        c1 = AcademicClass.objects.get(course_number = 99999)
        #check for empty
        self.assertEqual(t1.classes.count(),0)
        #add
        t1.classes.add(c1)
        self.assertEqual(CalenderModel.objects.count(), 1)
        self.assertEqual(t1.classes.count(),1)
        f = t1.classes.get(course_number = 99999)
        
        c2 = AcademicClass.objects.get(course_number = 99999)
        #check for only 1
        self.assertEqual(t1.classes.count(),1)
        
        #check to make sure validator works
        self.assertEqual(AuthenticateAddCalender(u, c2.course_number),3)
        
        f1 = t1.classes.get(course_number = 99999)
        #make sure nothing is edited
        self.assertEqual(f.instructor_name, 'teacher')
        self.assertEqual(f.instructor_email, 'teacher@gmail.com')
        self.assertEqual(f.course_number, 99999)
        self.assertEqual(f.semester_code, '9999')
        self.assertEqual(f.course_section, '001')
        self.assertEqual(f.subject, 'TC')
        self.assertEqual(f.catalog_number,'9999' )
        self.assertEqual(f.description, 'Testcase1')
        self.assertEqual(f.units, '3')
        self.assertEqual(f.component, 'LEC')
        self.assertEqual(f.class_capacity, 99)
        self.assertEqual(f.wait_list, 0)
        self.assertEqual(f.wait_cap, 0)
        self.assertEqual(f.enrollment_total, 0)
        self.assertEqual(f.enrollment_available, 99)
        self.assertEqual(f.topic, '')
        self.assertEqual(f.days, 'MoWeFr')
        self.assertEqual(f.start_time, '17.00.00.000000-05:00')
        self.assertEqual(f.end_time, '18.15.00.000000-05:00')
        self.assertEqual(f.facility_description, 'Olsson Hall 009')
        
        self.assertEqual(f1.instructor_name, 'teacher')
        self.assertEqual(f1.instructor_email, 'teacher@gmail.com')
        self.assertEqual(f1.course_number, 99999)
        self.assertEqual(f1.semester_code, '9999')
        self.assertEqual(f1.course_section, '001')
        self.assertEqual(f1.subject, 'TC')
        self.assertEqual(f1.catalog_number,'9999' )
        self.assertEqual(f1.description, 'Testcase1')
        self.assertEqual(f1.units, '3')
        self.assertEqual(f1.component, 'LEC')
        self.assertEqual(f1.class_capacity, 99)
        self.assertEqual(f1.wait_list, 0)
        self.assertEqual(f1.wait_cap, 0)
        self.assertEqual(f1.enrollment_total, 0)
        self.assertEqual(f1.enrollment_available, 99)
        self.assertEqual(f1.topic, '')
        self.assertEqual(f1.days, 'MoWeFr')
        self.assertEqual(f1.start_time, '17.00.00.000000-05:00')
        self.assertEqual(f1.end_time, '18.15.00.000000-05:00')
        self.assertEqual(f1.facility_description, 'Olsson Hall 009')