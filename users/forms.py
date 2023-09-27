from django.core.exceptions import ValidationError
from django import forms
from users.models import Teacher, Student, Course


# Teacher Register Form
class TeaRegForm(forms.Form):
    name = forms.CharField(label='username', min_length=6,
                           widget=forms.widgets.TextInput(
                               attrs={'class': 'form-control', 'placeholder': 'please input name'}),
                           error_messages={'required': 'username cannot be empty',
                                           'min_length': 'the length of username at least is 6 digit'})
    age = forms.DateField(label='age', widget=forms.widgets.DateInput(
        attrs={'class': 'form-control', 'placeholder': 'please input age'}),
                          )
    password = forms.CharField(label="password", max_length=500,
                               widget=forms.widgets.PasswordInput(
                                   render_value=True,
                                   attrs={"class": "form-control"},
                               ),
                               error_messages={'max_length': 'the max length of password is 500 digit',
                                               'required': 'password cannot be empty', })
    re_password = forms.CharField(label="re_password", max_length=500,
                                  widget=forms.widgets.PasswordInput(
                                      attrs={"class": "form-control"}, render_value=True),
                                  error_messages={
                                      'max_length': 'the max length of password is 10 digit',
                                      'required': 'password cannot be empty',
                                      'min_length': 'the length of password at least is 6 digit'})
    teac_email = forms.CharField(label='teac_email', min_length=4, max_length=500, widget=forms.widgets.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'please input teacher email address'}),
                                 error_messages={
                                     'min_length': 'the length of email at least is 6 digit',
                                     'max_length': 'the max length of email is 64'})
    gender = forms.ChoiceField(choices=Teacher.gender_choice)

    # check if the teacher's name is repetitive

    # check if the password is equal to re_password and check the format of password
    def clean(self):
        password = self.cleaned_data.get("password", "")
        re_password = self.cleaned_data.get("re_password", "")
        if len(password) < 6:
            self.add_error("re_password", ValidationError("The password should at least 6 digital "))
        if len(re_password) < 6:
            self.add_error("re_password", ValidationError("The re_password should at least 6 digital "))
        if not any(char.isupper() for char in password):
            self.add_error("password", ValidationError(
                'This password must contain at least 1 uppercase character'))
        if not any(char.isdigit() for char in password):
            self.add_error("password", ValidationError(
                'This password must contain at least 1 digit'))
        if password != re_password:
            # raise forms.ValidationError("The two passwords are different")
            self.add_error("re_password", ValidationError("The two passwords are different"))

    # check if the teacher email is repetitive
    def clean_email(self):
        new_email = self.cleaned_data.get("teac_email")
        teachers = Teacher.objects.all()
        for teacher in teachers:
            if teacher.teac_email == new_email:
                self.add_error("teac_email", ValidationError("the teacher email address has existed"))


# Register Student Form
class StudRegForm(forms.Form):
    name = forms.CharField(label='name', min_length=6,
                           widget=forms.widgets.TextInput(
                               attrs={'class': 'form-control', 'placeholder': 'please input name'}),
                           error_messages={'required': 'username cannot be empty',
                                           'min_length': 'the length of username at least is 6 digit'})

    StudentID = forms.CharField(label='StudentID', min_length=8,
                                widget=forms.widgets.TextInput(
                                    attrs={'class': 'form-control', 'placeholder': 'please input student ID'}),
                                error_messages={'required': 'The student ID cannot be empty',
                                                'min_length': 'the length of studentID at least is 8 digit'})

    age = forms.DateField(label='age', widget=forms.widgets.DateInput(
        attrs={'class': 'form-control', 'placeholder': 'please input age'}),
                          )
    password = forms.CharField(label="password", max_length=500,
                               widget=forms.widgets.PasswordInput(
                                   render_value=True,
                                   attrs={"class": "form-control"},
                               ),
                               error_messages={'max_length': 'the max length of password is 500 digit',
                                               'required': 'password cannot be empty', })

    re_password = forms.CharField(label="re_password", max_length=500,
                                  widget=forms.widgets.PasswordInput(
                                      attrs={"class": "form-control"}, render_value=True),
                                  error_messages={
                                      'max_length': 'the max length of password is 10 digit',
                                      'required': 'password cannot be empty',
                                      'min_length': 'the length of password at least is 6 digit'})

    stud_email = forms.CharField(label='stud_email', min_length=4, max_length=500, widget=forms.widgets.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'please input email address'}),
                                 error_messages={
                                     'min_length': 'the length of email at least is 6 digit',
                                     'max_length': 'the max length of email is 64'})

    stud_image = forms.ImageField()

    address = forms.TextInput(attrs={
        "class": "form-control"
    })

    gender = forms.ChoiceField(choices=Student.gender_choice)

    # check if the student's name is repetitive
    def clean_name(self):
        new_name = self.cleaned_data.get("name", "")
        students = Student.objects.all()
        for student in students:
            if student.name == new_name:
                self.add_error("name", ValidationError("the name has been existed"))

    # check if the password is equal to re_password and check the format of password
    def clean(self):
        password = self.cleaned_data.get("password", "")
        re_password = self.cleaned_data.get("re_password", "")
        if len(password) < 6:
            self.add_error("re_password", ValidationError("The password should at least 6 digital "))
        if len(re_password) < 6:
            self.add_error("re_password", ValidationError("The re_password should at least 6 digital "))
        if not any(char.isupper() for char in password):
            self.add_error("password", ValidationError(
                'This password must contain at least 1 uppercase character'))
        if not any(char.isdigit() for char in password):
            self.add_error("password", ValidationError(
                'This password must contain at least 1 digit'))
        if password != re_password:
            # raise forms.ValidationError("The two passwords are different")
            self.add_error("re_password", ValidationError("The two passwords are different"))

    # check if the teacher email is repetitive
    def clean_email(self):
        new_email = self.cleaned_data.get("stud_email")
        students = Student.objects.all()
        for student in students:
            if student.stud_email == new_email:
                self.add_error("stud_email", ValidationError("the student email address has existed"))


# create new course
class CourseRegForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['CourseID', 'course_name', 'StartTime', 'EndTime', 'ClassID', 'classroom_no', 'course_date',
                  'course_state']
        labels = {
            "CourseID": "CourseID",
            "course_name": "course_name",
            "StartTime": "StartTime",
            "EndTime": "EndTime",
            "ClassID": "ClassID",
            "classroom_no": "classroom_no",
            "course_date": "course_date",
            "course_state": "course_state",
        }
        widgets = {
            "CourseID": forms.widgets.TextInput(attrs={
                "class": "form-control"
            }),
            "course_name": forms.widgets.TextInput(attrs={
                "class": "form-control"
            }),
            "StartTime": forms.widgets.TimeInput(attrs={
                "class": "form-control"
            }),
            "EndTime": forms.widgets.TimeInput(attrs={
                "class": "form-control"
            }),
            "ClassID": forms.widgets.TextInput(attrs={
                "class": "form-control"
            }),
            "classroom_no": forms.widgets.TextInput(attrs={
                "class": "form-control"
            }),
            "course_date": forms.widgets.DateInput(attrs={
                "class": "form-control"
            }),
            "course_state": forms.Select(choices=Course.course_choice),

        }
        error_messages = {
            "CourseID": {'required': 'the course ID cannot be empty',
                         'max_length': 'the max length of course ID is 20'},
            "course_name": {'required': 'the course name cannot be empty',
                            'max_length': 'the max length of course name is 100'},
            "ClassID": {'required': 'the class ID cannot be empty',
                        'max_length': 'the max length of class ID is 20'},
            "classroom_no": {'required': 'the classroom number cannot be empty',
                             'max_length': 'the max length of classroom number is 10'},
            "course_date": {'required': 'the course date cannot be empty'},
        }

    teacher_name = forms.CharField(label="teacher_name", max_length=500,
                                   widget=forms.widgets.TextInput(
                                       attrs={"class": "form-control"}),
                                   error_messages={
                                       'max_length': 'the max length of teacher is 500 digit',
                                       'required': 'teacher name cannot be empty'})


# User change password form
class UserChangePasswordForm(forms.Form):
    name = forms.CharField(label='username', min_length=6,
                           widget=forms.widgets.TextInput(
                               attrs={'class': 'form-control', 'placeholder': 'please input name'}),
                           error_messages={'required': 'username cannot be empty',
                                           'min_length': 'the length of username at least is 6 digit'})

    original_password = forms.CharField(label="original_password", max_length=10,
                                        widget=forms.widgets.PasswordInput(
                                            render_value=True,
                                            attrs={"class": "form-control"},
                                        ),
                                        error_messages={'max_length': 'the max length of original password is 10 digit',
                                                        'required': 'original password cannot be empty',
                                                        'min_length': 'the length of original password at least is 6 digit'})

    new_password = forms.CharField(label="new_password", max_length=10,
                                   widget=forms.widgets.PasswordInput(
                                       render_value=True,
                                       attrs={"class": "form-control"},
                                   ),
                                   error_messages={'max_length': 'the max length of new password is 10 digit',
                                                   'required': 'new password cannot be empty',
                                                   'min_length': 'the length of new password at least is 6 digit'})

    re_password = forms.CharField(label="re_password", max_length=10,
                                  widget=forms.widgets.PasswordInput(
                                      attrs={"class": "form-control"}, render_value=True),
                                  error_messages={
                                      'max_length': 'the max length of password is 10 digit',
                                      'required': 'password cannot be empty',
                                      'min_length': 'the length of password at least is 6 digit'})

    def clean(self):
        original_password = self.cleaned_data.get("original_password", '')
        password = self.cleaned_data.get("new_password", '')
        re_password = self.cleaned_data.get("re_password", '')
        if original_password == "":
            self.add_error("original_password", ValidationError("The original_password is empty"))
        if password == "":
            self.add_error("re_password", ValidationError("The new password is empty"))
        if re_password == "":
            self.add_error("re_password", ValidationError("The repeat new password is empty"))
        if len(password) < 6:
            self.add_error("re_password", ValidationError("The password should at least 6 digital "))
        if len(re_password) < 6:
            self.add_error("re_password", ValidationError("The re_password should at least 6 digital "))
        if password != re_password:
            # raise forms.ValidationError("The two passwords are different")
            self.add_error("re_password", ValidationError("The two passwords are different"))
        if not any(char.isupper() for char in password):
            self.add_error("re_password", ValidationError('This password must contain at least 1 uppercase character'))
        if not any(char.isdigit() for char in password):
            self.add_error("re_password",
                           ValidationError('This password must contain at least 1 digit'))
