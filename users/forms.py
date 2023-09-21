from django.core.exceptions import ValidationError
from django import forms
from users.models import Teacher, Student


# Teacher Register Form
class TeaRegForm(forms.Form):
    name = forms.CharField(label='username', min_length=6,
                           widget=forms.widgets.TextInput(
                               attrs={'class': 'form-control', 'placeholder': 'please input name'}),
                           error_messages={'required': 'username cannot be empty',
                                           'min_length': 'the length of username at least is 6 digit'})
    age = forms.DateField(label='age',widget=forms.widgets.DateInput(
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
    def clean_name(self):
        new_name = self.cleaned_data.get("name", "")
        teachers = Teacher.objects.all()
        for teacher in teachers:
            if teacher.name == new_name:
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
        new_email = self.cleaned_data.get("teac_email")
        teachers = Teacher.objects.all()
        for teacher in teachers:
            if teacher.teac_email == new_email:
                self.add_error("teac_email", ValidationError("the teacher email address has existed"))


# Register Student Form
class StudRegForm(forms.Form):
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



