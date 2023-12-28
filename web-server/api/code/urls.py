from django.contrib import admin
from django.urls import path,include
from api.code.codeviews import *
urlpatterns = [
	path('emailcode', EmailCodeView.as_view()),
	path('imgcode', CaptchaAPIView.as_view()),
]
