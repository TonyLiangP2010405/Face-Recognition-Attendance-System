from django.urls import path, include
from basic import views


urlpatterns = [
    path("", views.HomePage, name='HomePage'),

]
