from django.urls import path
from .views import jobdetail, user_login, dashboard, upload_image, pdf_view, delete_account, search_jobs, SearchJobsAPI


urlpatterns = [
    path('detail/<int:id>', jobdetail, name='jobdetail'),
    path('user_login/', user_login, name='user_login'),
    path('', dashboard, name='dashboard'),
    path('pdf/', pdf_view, name='pdf_view'),
    path('delete_account/<int:id>/', delete_account, name='delete_account'),
    path('search_jobs/', search_jobs, name='search_jobs'),  # Arama sonuçları sayfası
    path('api/search_jobs/', SearchJobsAPI.as_view(), name='search_jobs_api'),  # API URL
]
