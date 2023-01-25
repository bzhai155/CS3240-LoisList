from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.models import User
import datetime
import requests
from .models import Student, AcademicClass, ShoppingCart, RatingForm, Rating, CalenderModel, Comment
import json

# Create your views here.


def index(request):
     """
     if request.method == 'POST':
        t = request.POST.get('te')
        d = request.POST.get('de')
        deepthought.objects.create(title_text=t, text_text=d)
        return HttpResponseRedirect('list/')
    return render(request, "polls/createthought.html")

     """
     return render(request, 'index.html')

def homepage(request):
     if request.method == "POST":
          updateClasses()
          return render(request, 'home.html')
     if (request.user.is_authenticated):
          if (Student.objects.filter(user=request.user).count() == 0):
               p = Student.objects.create(user=request.user, username=request.user.username, first_name=request.user.first_name, last_name=request.user.last_name, email=request.user.email)
          else:
               p = Student.objects.get(user=request.user)
          return render(request, 'home.html')
     return render(request, 'home.html')

def call_api(request, whichDept):
     whichDept = whichDept.upper()
     popup = 0
     # response = requests.get("http://luthers-list.herokuapp.com/api/")
     # api = response.json()
     # deptlist = requests.get(api["deptlist"]).json()
     classlist = requests.get(f"http://luthers-list.herokuapp.com/api/dept/{whichDept}/").json()
     mymap = {}
     for sec in classlist:
          sec['catalog_number'] += ":"
          sec['days'] = sec['meetings'][0]['days']
          sec['start_time'] = sec['meetings'][0]['start_time'][:5]
          sec['end_time'] = sec['meetings'][0]['end_time'][:5]
          sec['start_time'] = sec['start_time'].replace('.', ':')
          sec['end_time'] = sec['end_time'].replace('.', ':')
          sec['facility_description'] = sec['meetings'][0]['facility_description']
          if sec['description'] not in mymap:
               mymap[sec['description']] = 1
          else:
               sec['subject'] = " "
               sec['description'] = " "
     # http://luthers-list.herokuapp.com/api/dept/APMA/

     #add class to shopping cart
     if request.method == "POST":
          #figure out which button was pressed
          addclass = None
          SCaddclass = None
          for key in request.POST.keys():
               if key.startswith('class:'):
                    addclass = key[6:]
                    break
               elif key.startswith('Calender:'):
                    SCaddclass = key[9:]
                    break
          if addclass != None:
               #no shopping cart
               if (ShoppingCart.objects.filter(user= request.user).count() == 0):
                    s = ShoppingCart.objects.create(user=request.user)
                    c = AcademicClass.objects.get(course_number = addclass)
                    s.classes.add(c)
                    s.save()
               #shopping cart exist
               else:
                    s = ShoppingCart.objects.get(user= request.user)
                    c = AcademicClass.objects.get(course_number = addclass)
                    s.classes.add(c)
                    s.save()
          else:
               #no calender
               if (CalenderModel.objects.filter(user= request.user).count() == 0):
                    ca = CalenderModel.objects.create(user=request.user)
                    c = AcademicClass.objects.get(course_number = SCaddclass)
                    ca.classes.add(c)
                    ca.save()
               #calender exist
               else:
                    ca = CalenderModel.objects.get(user= request.user)
                    popup = AuthenticateAddCalender(request.user, SCaddclass)
                    if(popup == 0):
                         ac = AcademicClass.objects.get(course_number = SCaddclass)
                         ca.classes.add(ac)
                         ca.save()
          return render(request,'classes.html',{
               'data':classlist,
               'popup':popup
          })
     return render(request,'classes.html',{
          'data':classlist,
          'popup':popup
     })

def list_classes(request):
     deptlist = requests.get(f"http://luthers-list.herokuapp.com/api/deptlist/").json()
     asDeptList = [["AMST", "ANTH", "ARAB", "ARAD", "ARAH", "ARTH", "ARTR", "ARTS", "ASTR", "BIOL"], ["CHEM", "CHIN",
                   "CHTR", "CLAS", "CREO", "DANC", "DRAM", "EAST", "ECON", "ENCW"], ["ENGL", "ENWR", "EVAT", "EVEC",
                   "EVGE", "EVSC", "FREN", "GERM", "GETR", "GREE"], ["HBIO", "HEBR", "HIAF", "HIEA", "HIEU", "HILA",
                   "HIME", "HIND", "HISA", "HIST"], ["HIUS", "ITAL", "ITTR", "JAPN", "JPTR", "KICH", "KOR", "LATI",
                   "LNGS", "MATH"], ["MESA", "MDST", "MESA", "MSP", "MUEN", "MUPF", "MUSI", "PERS", "PETR", "PHIL"],
                   ["PHS", "PHYS", "PLAD", "PLAN", "PLAP", "PLCP", "PLIR", "PLPT", "POL", "PORT"], ["PSYC", "RELA",
                   "RELB", "RELC", "RELG", "RELH", "RELI", "RELJ", "RELS", "RUSS"], ["RUTR", "SANS", "SAST", "SATR",
                   "SLAV", "SOC", "SPAN", "STAT", "TURK", "URDU"], ["WGS"]]
     esDeptList = [["APMA", "CPE", "ECE", "BME", "MSE", "CHE", "MAE", "CE", "STS", "CS"], ["SYS", "ENGR"]]
     otherList = [["ACCT", "AIRS", "ALAR", "ARCH", "ARCY", "ARH", "ASL", "BIMS", "BIOC", "BIOP"], ["BUS", "CASS", "CELL",
                  "COGS", "COLA", "COMM", "CONC", "DEM", "DH", "DS"], ["EALC", "EDHS", "EDIS", "EDLF", "EDNC", "EGMT",
                  "ELA", "ENTP", "ESL", "ETP"], ["EURS", "EVHY", "GBAC", "GBUS", "GCCS", "GCNL", "GCOM", "GDS", "GHSS",
                  "GNUR"], ["GSAS", "GSCI", "GSGS", "GSMS", "GSSJ", "GSVS", "HHE", "HR", "HSCI", "IMP"], ["INST", "ISBU",
                  "ISHU", "ISIN", "ISLS", "ISSS", "IT", "KINE", "KLPA", "LAR"], ["LASE", "LAST", "LAW", "LING", "LPPA",
                  "LPPL", "LPPP", "LPPS", "MED", "MICR"], ["MISC", "MUBD", "NASC", "NCPR", "NESC", "NUCO", "NUIP", "NURS",
                  "PATH", "PC"], ["PHAR", "PHY", "PLAC", "POTR", "PPL", "PSHM", "PSLP", "PSPA", "PSPM", "PSPS"], ["PST",
                  "SARC", "SEC", "SLTR", "SWAH", "UD", "UNST", "USEM"]]
     return render(request,'listclass.html',{
          'deptlist':deptlist,
          'aslist':asDeptList,
          'eslist':esDeptList,
          'otherlist':otherList
     })
     

def user(request):
     return render(request, 'index.html')

def rateSpecificClass(request, pk):
     context = {}
     theClass = get_object_or_404(AcademicClass, course_number=pk)
     whichClass = f"{theClass.subject} {theClass.catalog_number}"

     post = request.POST.copy()  # to make it mutable
     post['whichClass'] = whichClass
     request.POST = post

     form = RatingForm(request.POST or None, request.FILES or None)
     if form.is_valid():
          form.save()
          return redirect('specificClass', pk=pk)
     context['form'] = form
     context['whichClass'] = whichClass
     return render(request, "rate.html", context)

def specificClass(request, pk):
    theClass = get_object_or_404(AcademicClass, course_number=pk)
    print(theClass.course_number)
    whichClass = f"{theClass.subject} {theClass.catalog_number}"

    reviews = Rating.objects.order_by('-pub_date').filter(whichClass=whichClass)
    average = 0
    totalRatings = 0
    for r in Rating.objects.order_by('-pub_date').filter(whichClass=whichClass):
        average += float(r.rating)
        totalRatings += 1
    if totalRatings != 0:
         average /= float(totalRatings)
    else:
         average = "No Ratings Yet"

    return render(request, "specific-class.html", {
        "class": theClass,
        "rating": average,
        "reviews": reviews
    })


def updateClasses():
     deptlist = requests.get(f"http://luthers-list.herokuapp.com/api/deptlist/").json()
     for i in deptlist:
          classlist = requests.get(f"http://luthers-list.herokuapp.com/api/dept/" + i.get("subject") + "/").json()
          for j in classlist:
               if AcademicClass.objects.filter(course_number=j.get("course_number")):
                    c = AcademicClass.objects.get(course_number=j.get("course_number"))
                    c.class_capacity = j.get("class_capacity")
                    c.wait_list = j.get("wait_list")
                    c.enrollment_total = j.get("enrollment_total")
                    c.enrollment_available = j.get("enrollment_available")
                    #checks for empty array for meetings
                    if j.get("meetings"):
                         c.days = j.get("meetings")[0].get("days")
                         c.start_time =  j.get("meetings")[0].get("start_time")[0:5]
                         c.end_time = j.get("meetings")[0].get("end_time")[0:5]
                         c.facility_description = j.get("meetings")[0].get("facility_description")
                    c.save()
               else:
                    c = AcademicClass()
                    c.instructor_name = j.get("instructor").get("name")
                    c.instructor_email = j.get("instructor").get("email")
                    c.course_number = j.get("course_number")
                    c.semester_code = j.get("semester_code")
                    c.course_section = j.get("course_section")
                    c.subject = j.get("subject")
                    c.catalog_number = j.get("catalog_number")
                    c.description = j.get("description")
                    c.units = j.get("units")
                    c.component = j.get("component")
                    c.class_capacity = j.get("class_capacity")
                    c.wait_list = j.get("wait_list")
                    c.enrollment_total = j.get("enrollment_total")
                    c.enrollment_available = j.get("enrollment_available")
                    #checks for empty array for meetings
                    if j.get("meetings"):
                         c.days = j.get("meetings")[0].get("days")
                         c.start_time =  j.get("meetings")[0].get("start_time")[0:5]
                         c.end_time = j.get("meetings")[0].get("end_time")[0:5]
                         c.facility_description = j.get("meetings")[0].get("facility_description")
                    c.save()
# We want to delete this as some point for security reasons. I'm told we will get points off --Alison
def list_users(request):
     my_gdata =User.objects.all()
     data =[]
     for x in my_gdata:
      #  rlist.append(x.username  + ' (' + (x.email if len(x.email) >0 else "no email") + ')  Last Login at ' + x.last_login.strftime("%A, %d. %B %Y %I:%M%p") + '  ' + ('Active user' if x.is_active==bool('True') else 'No-Active user') )
        data.append({
           'UserName': x.username,
           'Email': x.email,
           'Status': 'Active' if x.is_active==bool('True') else 'Non-Active',
           'LastLogin': x.last_login.strftime("%A, %d. %B %Y %I:%M%p") if isinstance(x.last_login, datetime.datetime) else ''
           #'LastLogin': x.last_login.strftime("%A, %d. %B %Y %I:%M%p")
            })
     return render(request,'users.html',{
         'google_logins':data
     })

def shoppingcart(request):
     popup = 0
     if (request.user.is_authenticated):
          #make a cart if none exist for the user
          if (ShoppingCart.objects.filter(user=request.user).count() == 0):
               s = ShoppingCart.objects.create(user=request.user)
          else:
               s = ShoppingCart.objects.get(user= request.user)
          cart = s.classes.all()
          #add class to shopping cart
          if request.method == "POST": 
               #figure out which button was pressed
               Removeclass = None
               SCaddclass = None
               for key in request.POST.keys():
                    if key.startswith('Remove:'):
                         Removeclass = key[7:]
                         break
                    elif key.startswith('Schedule:'):
                         SCaddclass = key[9:]
                         break
               if Removeclass != None:
                    ac = AcademicClass.objects.get(course_number = Removeclass)
                    s.classes.remove(ac)
               else:
                    #calender doesnt exist
                    if (CalenderModel.objects.filter(user= request.user).count() == 0):
                         ca = CalenderModel.objects.create(user=request.user)
                         ac = AcademicClass.objects.get(course_number = SCaddclass)
                         ca.classes.add(ac)
                         ca.save()
                    #calender exist
                    else:
                         ca = CalenderModel.objects.get(user= request.user)
                         popup = AuthenticateAddCalender(request.user, SCaddclass)
                         if(popup == 0):
                              ac = AcademicClass.objects.get(course_number = SCaddclass)
                              ca.classes.add(ac)
                              ca.save()
          return render(request,'shoppingcart.html',{
               'cart':cart,
               'popup':popup
          })
     return render(request,'shoppingcart.html',{
          'cart':cart,
          'popup':popup
     })

def Calender(request):
     
     if (request.user.is_authenticated):
          #make a cart if none exist for the user
          mond = []
          tues = []
          wend = []
          thur = []
          frid = []
          if (CalenderModel.objects.filter(user=request.user).count() == 0):
               c = CalenderModel.objects.create(user=request.user)
          else:
               c = CalenderModel.objects.get(user= request.user)
          #add class to shopping cart
          if request.method == "POST":
          #figure out which button was pressed
               Removeclass = None
               for key in request.POST.keys():
                    if key.startswith('Remove:'):
                         Removeclass = key[7:]
                         break
               if Removeclass != None:
                    ac = AcademicClass.objects.get(course_number = Removeclass)
                    c.classes.remove(ac)
          classes = c.classes.all().order_by('start_time').values()
          for indclass in classes:
               st = indclass.get('days')
               print(st)
               if st.find('Mo') != -1:
                    mond.append(indclass)
               if st.find('Tu') != -1:
                    tues.append(indclass)
               if st.find('We') != -1:
                    wend.append(indclass)
               if st.find('Th') != -1:
                    thur.append(indclass)
               if st.find('Fr') != -1:
                    frid.append(indclass)
          return render(request,'calender.html',{
               'classes':classes,
               'mond' : mond,
               'tues' : tues,
               'wend' : wend,
               'thur' : thur,
               'frid' : frid
          })
     return render(request,'calender.html',{
          'classes':classes,
               'mond' : mond,
               'tues' : tues,
               'wend' : wend,
               'Thur' : thur,
               'Frid' : frid
     })



#0 good
#1 same time
#2 same course diff section
#3 already added
def AuthenticateAddCalender(user, classID):
     c = CalenderModel.objects.get(user = user)
     classes = c.classes.all()
     ac = AcademicClass.objects.get(course_number = classID)
     #need to compare
     if ac.start_time:
          for check in classes:
               #class has a meeting
               if ac == check:
                    return 3
               if ac.subject == check.subject and ac.catalog_number == check.catalog_number:
                    return 2
               if check.start_time: 
                    #time intersect      
                    if (float(check.start_time[0:5]) <= float(ac.start_time[0:5]) and float(ac.start_time[0:5]) <= float(check.end_time[0:5])) or (float(check.start_time[0:5]) <= float(ac.end_time[0:5]) and float(ac.end_time[0:5]) <= float(check.end_time[0:5])):
                         #days intersect
                         daylist = [ac.days[idx:idx + 2] for idx in range(0, len(ac.days), 2)]
                         for day in daylist:
                              #same day
                              if check.days.find(day) != -1:
                                   return 1
     return 0

def user_page(request, username):
     DStudent = get_object_or_404(Student, username=username)
     s = Student.objects.get(user=request.user)
     ownpage = False
     isfriend = False
     comments = None
     #check if its their own
     if (request.user.is_authenticated):
          if request.user == DStudent.user:
               ownpage = True
          if (DStudent.friends.all().filter(user=request.user).count() != 0):
               isfriend = True
          if Comment.objects.filter(to_who = DStudent).count() != 0:
               comments = Comment.objects.filter(to_who = DStudent).all()
     mond = []
     tues = []
     wend = []
     thur = []
     frid = []
     if (CalenderModel.objects.filter(user=DStudent.user).count() == 0):
          c = CalenderModel.objects.create(user=DStudent.user)
     else:
          c = CalenderModel.objects.get(user= DStudent.user)
     classes = c.classes.all().order_by('start_time').values()
     for indclass in classes:
          st = indclass.get('days')
          if st.find('Mo') != -1:
               mond.append(indclass)
          if st.find('Tu') != -1:
               tues.append(indclass)
          if st.find('We') != -1:
               wend.append(indclass)
          if st.find('Th') != -1:
               thur.append(indclass)
          if st.find('Fr') != -1:
               frid.append(indclass)
          #add class to shopping cart
     if request.method == "POST":
          #figure out which button was pressed
          for key in request.POST.keys():
               if key.startswith('Remove Friend'):
                    s.friends.remove(DStudent)
               if key.startswith('Add Friend'):
                    s.friends.add(DStudent)
                    s.save()
               if key.startswith('Add comment'):
                    cont = request.POST.get('comment')
                    if cont:
                         com = Comment.objects.create(username = request.user.username, content=cont, to_who=DStudent)

                         
               
     return render(request,'userpage.html',{
          'classes':classes,
          'mond' : mond,
          'tues' : tues,
          'wend' : wend,
          'thur' : thur,
          'frid' : frid,
          'ownpage' : ownpage,
          'username' : username,
          'isfriend' : isfriend,
          'comments' : comments
     })
     
def user_page_base(request):
     return render(request,'calender.html')


def Friends(request):
     listfs = None
     listuser = None
     if (request.user.is_authenticated):
          s = Student.objects.get(user=request.user)
          listfs = s.friends.all()
          listuser = Student.objects.all().filter(~Q(first_name='')).order_by('first_name')
          #add class to shopping cart
          if request.method == "POST":
          #figure out which button was pressed
               for key in request.POST.keys():
                    if key.startswith('removefriend:'):
                         Removef = key[13:]
                         Removes = Student.objects.get(email=Removef)
                         s.friends.remove(Removes)
                    if key.startswith('search'):
                         name = request.POST.get('friendsearch')
                         listuser = Student.objects.filter(Q(first_name__contains = name) | Q(last_name__contains = name)).all().filter(~Q(first_name='')).order_by('first_name')
          return render(request,'friends.html',{
               'listfs' : listfs,
               'listuser': listuser
          })
     return render(request,'friends.html',{
          'listfs' : listfs,
          'listuser': listuser
     })
