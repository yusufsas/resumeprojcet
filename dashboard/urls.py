from django.contrib import admin
from django.urls import path

from .views import appliedjobs, jobdetail,user_login,dashboard,upload_image,pdf_view,delete_account


urlpatterns=[
    path('detail/<int:id>',jobdetail,name='jobdetail'),
    path('user_login/', user_login, name='user_login'),
    path('',dashboard,name='dashboard'),
    path('pdf/', pdf_view, name='pdf_view'),
    path('delete_account/<int:id>/', delete_account, name='delete_account'),
    path('appliedjobs/', appliedjobs, name='appliedjobs'),

    # path('upload_image', upload_image, name='upload_image'),

]