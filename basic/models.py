from django.db import models

from users.models import Student, Course


# Create your models here.
# Create AttendanceReport model
class AttendanceReport(models.Model):
    AttendanceID = models.IntegerField(primary_key=True)
    status_choice =(
        (0, "0"),
        (1, "1"),
    )
    Present_status = models.CharField(max_length=1, choices=status_choice)
    Absent_rate = models.FloatField()
    CourseID = models.ForeignKey(Course, on_delete=models.CASCADE)
    Attendance_start_time = models.DateTimeField()

    def __str__(self):
        return str(self.AttendanceID) + str(self.Present_status) + str(self.Absent_rate)

    class Meta:
        verbose_name = "Attendance"
        verbose_name_plural = "Attendance"
        db_table = "d_attendance"


# Create StudentAttendance model
class StudentAttendance(models.Model):
    Sta_ID = models.IntegerField(primary_key=True)
    StudentID = models.ForeignKey(Student, on_delete=models.CASCADE)
    AttendanceID = models.ForeignKey(AttendanceReport, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.Sta_ID) + str(self.StudentID) + str(self.AttendanceID)

    class Meta:
        verbose_name = "student attendance"
        verbose_name_plural = "student attendance"
        db_table = "d_studentAttendance"

