from django.contrib import admin
from django.urls import path


from .views import jobdetail,user_login,dashboard

urlpatterns=[
    path('detail/<int:id>',jobdetail,name='jobdetail'),
    path('user_login/', user_login, name='user_login'),
    path('',dashboard,name='dashboard'),
 


]