from django.urls import path,include
from api.company.companyviews import CompanyViewSet
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'company', CompanyViewSet)
urlpatterns = [
]
urlpatterns += router.urls