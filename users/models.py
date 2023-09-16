from django.db import models


# Create your models here.

# Create Teacher model
class Teacher(models.Model):
    TeacherID = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    teac_email = models.CharField(max_length=100)
    gender_choice = (
        (0, "0"),
        (1, "1"),
    )
    gender = models.CharField(max_length=1, choices=gender_choice)
    age = models.IntegerField()
    teac_image = models.ImageField(upload_to="teacherImage", blank=True)

    def __str__(self):
        return str(self.TeacherID) + str(self.name) + str(self.gender)

    class Meta:
        verbose_name = "teacher information"
        verbose_name_plural = "teacher_information"
        db_table = 'd_teacher'


# Create Course model
class Course(models.Model):
    CourseID = models.CharField(max_length=20)
    course_name = models.CharField(max_length=100)
    TeacherID = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    StartTime = models.TimeField()
    EndTime = models.TimeField()
    ClassID = models.CharField(max_length=20)
    classroom_no = models.CharField(max_length=10)
    course_date = models.DateField()
    course_choice = (
        (0, "0"),
        (1, "1"),
    )
    course_state = models.CharField(max_length=1, choices=course_choice)

    def __str__(self):
        return str(self.CourseID) + str(self.course_name)

    class Meta:
        verbose_name = "Course information"
        verbose_name_plural = "course_information"
        db_table = "d_course"


# Create Student model
class Student(models.Model):
    StudentID = models.CharField(max_length=8)
    name = models.CharField(max_length=20)
    address = models.TextField()
    stud_email = models.CharField(max_length=100)
    gender_choice = (
        (0, "0"),
        (1, "1"),
    )
    gender = models.CharField(max_length=1, choices=gender_choice)
    age = models.IntegerField()
    stud_image = models.ImageField(upload_to="studentImage", blank=True)

    def __str__(self):
        return str(self.StudentID) + str(self.name) + str(self.gender)

    class Meta:
        verbose_name = "student information"
        verbose_name_plural = "student_information"
        db_table = "d_student"


# Create Enrollment model
class Enrollment(models.Model):
    ID = models.IntegerField(primary_key=True)
    StudentID = models.ForeignKey(Student, on_delete=models.CASCADE)
    CourseID = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.ID) + str(self.StudentID) + str(self.CourseID)

    class Meta:
        verbose_name = "Enrollment"
        verbose_name_plural = "Enrollment"
        db_table = "d_enrollment"
