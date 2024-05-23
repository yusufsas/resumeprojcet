from django.contrib import admin
from django.urls import path

from .views import jobdetail,user_login,dashboard,upload_image


urlpatterns=[
    path('detail/<int:id>',jobdetail,name='jobdetail'),
    path('user_login/', user_login, name='user_login'),
    path('',dashboard,name='dashboard'),
 
    # path('upload_image', upload_image, name='upload_image'),

]