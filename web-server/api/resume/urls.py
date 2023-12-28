from django.urls import path,include
from api.resume.resumeviews import UserResumeViewSet
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'resume', UserResumeViewSet)
urlpatterns = [
]
urlpatterns += router.urls