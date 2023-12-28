from rest_framework import viewsets
from .serializers import *
from api.models import *
from rest_framework.permissions import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from django_filters import rest_framework as filters
from rest_framework.decorators import action
import csv
from django.db.models import  *
from django.db.models.functions import *
from rest_framework import permissions
from rest_framework.response import Response
import random

class CustomPermission(permissions.BasePermission):
	def has_permission(self, request, view):
		# 在这里编写权限逻辑，返回 True 表示有权限，返回 False 表示没有权限
		if request.method=='GET':
			return True
		else:
			
			return False
	def has_object_permission(self, request, view, obj):
		# 在这里编写对象级别的权限逻辑，返回 True 表示有权限，返回 False 表示没有权限
		return True

class CompanyFilter(filters.FilterSet):
	# jobid = filters.CharFilter(lookup_expr='exact')
	companynumber = filters.CharFilter(lookup_expr='exact')
	industryCompanyTags= filters.CharFilter(lookup_expr='exact')
	job_num=filters.NumberFilter(field_name='job_num', lookup_expr='gte')
	companyname=filters.CharFilter(lookup_expr='icontains')
	propertycode=filters.CharFilter(lookup_expr='exact')
	property=filters.CharFilter(lookup_expr='exact')
	class Meta:
		model = company
		fields = '__all__'
class CompanyViewSet(viewsets.ModelViewSet):
	authentication_classes = [JWTAuthentication]
	# 搜索
	filter_backends = [DjangoFilterBackend,SearchFilter, OrderingFilter]
	search_fields = ('companyname',)
	# 排序
	ordering_fields = ('job_num',)
	filterset_class =CompanyFilter
	permission_classes = [CustomPermission]
	queryset = company.objects
	serializer_class =companySerializer
	