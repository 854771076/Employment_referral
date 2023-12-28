from django.contrib import admin
from django.urls import path,include
from api.auth.authviews import *
urlpatterns = [
    path('login/', LoginView.as_view()),
    path('signup/', SignupView.as_view()),
    path('foreget/', ForegetPSWView.as_view()),
    path('userinfo/', UserInfoView.as_view()),
]
