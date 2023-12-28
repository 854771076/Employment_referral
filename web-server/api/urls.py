from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *
urlpatterns = [
    path('auth/', include('api.auth.urls')),
    path('code/', include('api.code.urls')),
    path('data/', include('api.resume.urls')),
    path('data/', include('api.job.urls')),
    path('data/', include('api.company.urls')),
    path('data/baseData', baseDataView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
]
