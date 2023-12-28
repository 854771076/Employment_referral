from django.urls import path,include
from api.job.jobviews import *
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'jobs', JobsViewSet)
urlpatterns = [
    path('similar-jobs/<str:number>/', SimilarJobsList.as_view()),
]
urlpatterns += router.urls