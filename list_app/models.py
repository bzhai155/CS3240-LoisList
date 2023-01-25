from django.db import models
from django.utils import timezone
from django import forms
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    username = models.CharField(max_length=50, default='', blank=True, null=True)
    first_name = models.CharField(max_length=50, default='', blank=True, null=True)
    last_name = models.CharField(max_length=50, default='', blank=True, null=True)
    email = models.CharField(max_length=100, default='', blank=True, null=True)
    friends = models.ManyToManyField('self')
    
    def __str__(self):
        return self.username
    
class Comment(models.Model):
    username = models.CharField(max_length=50, default='', blank=True, null=True)
    content = models.TextField(default='')
    to_who = models.ForeignKey(Student, on_delete=models.CASCADE)

class Rating(models.Model):
    rating = models.IntegerField(default=0)
    GPA = models.FloatField(default=3.0)
    thoughts = models.TextField(default='')

    whichClass = models.CharField(max_length=10, default='A')
    professor = models.CharField(max_length=50, default='A')
    pub_date = models.DateTimeField('date published', default=timezone.now)

class RatingForm(forms.ModelForm):
    rating = forms.IntegerField(min_value=0, max_value=5)
    GPA = forms.FloatField(min_value=0.0, max_value=4.0)

    class Meta:
        model = Rating
        exclude = ['pub_date']

class AcademicClass(models.Model):
    instructor_name = models.CharField(max_length=100, default='D', blank=True, null=True)
    instructor_email = models.EmailField(max_length=100, default='D', blank=True, null=True)
    course_number = models.IntegerField(primary_key=True, default='00000', blank=True, null=False)
    semester_code = models.CharField(max_length=10, default='0000', blank=True, null=True)
    course_section = models.CharField(max_length=10, default='0000', blank=True, null=True)
    subject = models.CharField(max_length=10, default='0000', blank=True, null=True)
    catalog_number = models.CharField(max_length=10, default='0000', blank=True, null=True)
    description = models.CharField(max_length= 200, default='0000', blank=True, null=True)
    units= models.CharField(max_length=10, default='0000', blank=True, null=True)
    component = models.CharField(max_length=10, default='0000', blank=True, null=True)
    class_capacity = models.IntegerField(default='0', blank=True, null=False)
    wait_list = models.IntegerField(default='0', blank=True, null=False)
    wait_cap = models.IntegerField(default='0', blank=True, null=False)
    enrollment_total = models.IntegerField(default='0', blank=True, null=False)
    enrollment_available = models.IntegerField(default='0', blank=True, null=False)
    topic = models.CharField(max_length= 200, default='', blank=True, null=True)
    days = models.CharField(max_length= 200, default='', blank=True, null=True)
    start_time = models.CharField(max_length= 20, default='', blank=True, null=True)
    end_time = models.CharField(max_length= 20, default='', blank=True, null=True)
    facility_description = models.CharField(max_length= 100, default='', blank=True, null=True)

    def __str__(self):
        return str(self.course_number)


class ShoppingCart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    classes = models.ManyToManyField(AcademicClass)
    
    def __str__(self):
        return self.user.username

class CalenderModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    classes = models.ManyToManyField(AcademicClass)
    
    def __str__(self):
        return self.user.username
