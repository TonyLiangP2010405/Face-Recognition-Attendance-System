from django.contrib import admin
from users.models import *


# Register your models here.


# Register Course model
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    admin.site.site_title = "Face Recognition Attendance System Admin"
    admin.site.site_header = "Face Recognition Attendance System Admin"
    admin.site.index_title = "Face Recognition Attendance Management"

    # the attributes of showing in list
    list_display = ['CourseID', 'course_name', 'TeacherID', 'StartTime', 'EndTime', 'ClassID', 'classroom_no',
                    'course_date', 'course_state']
    # search
    search_fields = ['CourseID', 'course_name', 'TeacherID', 'StartTime', 'EndTime', 'ClassID', 'classroom_no',
                     'course_date', 'course_state']
    # filtration
    list_filter = ['CourseID', 'TeacherID', 'ClassID']

    # Set the amount of data displayed per page
    list_per_page = 10
    # Set the sort
    ordering = ['CourseID']


# Register Student model
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    admin.site.site_title = "Face Recognition Attendance System Admin"
    admin.site.site_header = "Face Recognition Attendance System Admin"
    admin.site.index_title = "Face Recognition Attendance Management"

    # the attributes of showing in list
    list_display = ['StudentID', 'name', 'address', 'stud_email', 'gender', 'age']
    # search
    search_fields = ['StudentID', 'name']
    # filtration
    list_filter = ['StudentID', 'name', 'gender', 'age']
    # Set the amount of data displayed per page
    list_per_page = 10
    # Set the sort
    ordering = ['StudentID']


# Register Teacher model
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    admin.site.site_title = "Face Recognition Attendance System Admin"
    admin.site.site_header = "Face Recognition Attendance System Admin"
    admin.site.index_title = "Face Recognition Attendance Management"

    # the attributes of showing in list
    list_display = ['TeacherID', 'name', 'teac_email', 'gender', 'age']
    # search
    search_fields = ['TeacherID', 'name']
    # filtration
    list_filter = ['TeacherID', 'name']
    # Set the amount of data displayed per page
    list_per_page = 10
    # Set the sort
    ordering = ['TeacherID']


# Register Enrollment model
@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    admin.site.site_title = "Face Recognition Attendance System Admin"
    admin.site.site_header = "Face Recognition Attendance System Admin"
    admin.site.index_title = "Face Recognition Attendance Management"

    # the attributes of showing in list
    list_display = ['ID', 'StudentID', 'CourseID']
    # search
    search_fields = ['ID']
    # filtration
    list_filter = ['ID', 'CourseID', 'StudentID']
    # Set the amount of data displayed per page
    list_per_page = 10
    # Set the sort
    ordering = ['ID']

