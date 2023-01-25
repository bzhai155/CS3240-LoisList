from django.contrib import admin

from .models import Student, AcademicClass, ShoppingCart, CalenderModel, Comment, Rating, RatingForm

class StudentAdmin(admin.ModelAdmin):
    
    fieldsets = [
        (None,               {'fields': ['user']}),
        (None,               {'fields': ['username']}),
        (None,               {'fields': ['first_name']}),
        (None,               {'fields': ['last_name']}),
        (None,               {'fields': ['email']}),
        (None,               {'fields': ['friends']}),
    ]

admin.site.register(Student, StudentAdmin)  



class CommentAdmin(admin.ModelAdmin):
    
    fieldsets = [
        (None,               {'fields': ['username']}),
        (None,               {'fields': ['content']}),
        (None,               {'fields': ['to_who']}),
    ]

admin.site.register(Comment, CommentAdmin)  



class RatingAdmin(admin.ModelAdmin):
    
    fieldsets = [
        (None,               {'fields': ['rating']}),
        (None,               {'fields': ['GPA']}),
        (None,               {'fields': ['thoughts']}),
        (None,               {'fields': ['whichClass']}),
        (None,               {'fields': ['professor']}),
        (None,               {'fields': ['pub_date']}),
    ]

admin.site.register(Rating, RatingAdmin)  



# class RatingFormAdmin(admin.ModelAdmin):
    
#     fieldsets = [
#         (None,               {'fields': ['rating']}),
#         (None,               {'fields': ['GPA']}),
#     ]


# admin.site.register(RatingForm, RatingFormAdmin)  



class AcademicClassAdmin(admin.ModelAdmin):
    
    fieldsets = [
        (None,               {'fields': ['instructor_name']}),
        (None,               {'fields': ['instructor_email']}),
        (None,               {'fields': ['course_number']}),
        (None,               {'fields': ['semester_code']}),
        (None,               {'fields': ['course_section']}),
        (None,               {'fields': ['subject']}),
        (None,               {'fields': ['catalog_number']}),
        (None,               {'fields': ['description']}),
        (None,               {'fields': ['units']}),
        (None,               {'fields': ['component']}),
        (None,               {'fields': ['class_capacity']}),
        (None,               {'fields': ['wait_list']}),
        (None,               {'fields': ['wait_cap']}),
        (None,               {'fields': ['enrollment_total']}),
        (None,               {'fields': ['enrollment_available']}),
        (None,               {'fields': ['topic']}),
        (None,               {'fields': ['days']}),
        (None,               {'fields': ['start_time']}),
        (None,               {'fields': ['end_time']}),
        (None,               {'fields': ['facility_description']}),
    ]
    
admin.site.register(AcademicClass, AcademicClassAdmin)



class ShoppingCartAdmin(admin.ModelAdmin):
    
    fieldsets = [
        (None,               {'fields': ['user']}),
        (None,               {'fields': ['classes']}),
    ]

admin.site.register(ShoppingCart, ShoppingCartAdmin)  



class CalenderAdmin(admin.ModelAdmin):
    
    fieldsets = [
        (None,               {'fields': ['user']}),
        (None,               {'fields': ['classes']}),
    ]

admin.site.register(CalenderModel, CalenderAdmin)  

