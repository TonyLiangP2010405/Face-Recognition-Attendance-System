from django.urls import path, include
from users import views


urlpatterns = [
    path('StudentRegister/', views.student_register, name='StudentRegister'),
    path('TeacherRegister/', views.teacher_register, name='TeacherRegister'),
    path('StudentRegister/create_student_dataset', views.create_student_dataset, name='create_student_dataset'),
    path('StudentRegister/create_student_dataset/successful', views.create_student_dataset_successful,
         name='create_student_dataset_successful'),
    path('TeacherRegister/regitser_teacher_successful', views.register_teacher_successful,
         name='teacher_register_successful'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('user_login/', views.user_login, name='user_login'),
    path('user_login/user_login_successful', views.user_login_successful, name='user_login_successful'),

]
