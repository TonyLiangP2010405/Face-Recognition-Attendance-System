from django.contrib import admin
from basic.models import *


# Register your models here.

# Register AttendanceReport model
@admin.register(AttendanceReport)
class AttendanceReportAdmin(admin.ModelAdmin):
    admin.site.site_title = "Face Recognition Attendance System Admin"
    admin.site.site_header = "Face Recognition Attendance System Admin"
    admin.site.index_title = "Face Recognition Attendance Management"

    # the attributes of showing in list
    list_display = ['AttendanceID', 'Present_status', 'Attendance_start_time', 'CourseID']
    # search
    search_fields = ['AttendanceID']
    # filtration
    list_filter = ['AttendanceID', 'CourseID']
    # Set the date selector
    date_hierarchy = 'Attendance_start_time'
    # Set the amount of data displayed per page
    list_per_page = 10
    # Set the sort
    ordering = ['AttendanceID']


# Register StudentAttendance model
@admin.register(StudentAttendance)
class SAdmin(admin.ModelAdmin):
    admin.site.site_title = "Face Recognition Attendance System Admin"
    admin.site.site_header = "Face Recognition Attendance System Admin"
    admin.site.index_title = "Face Recognition Attendance Management"

    # the attributes of showing in list
    list_display = ['Sta_ID', 'StudentID', 'AttendanceID']
    # search
    search_fields = ['Sta_ID', 'StudentID', 'AttendanceID']
    # filtration
    list_filter = ['Sta_ID', 'StudentID', 'AttendanceID']
    # Set the amount of data displayed per page
    list_per_page = 10
    # Set the sort
    ordering = ['Sta_ID']