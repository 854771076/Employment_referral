from rest_framework import viewsets
from .serializers import *
from rest_framework.permissions import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from django_filters import rest_framework as filters
from django.http import HttpResponse
from rest_framework.decorators import action
import csv
from rest_framework.response import Response
from api.models import user,Logs,UserResume
from django.db.models import  *
from django.db.models.functions import *
from rest_framework import permissions

class CustomPermission(permissions.BasePermission):
	def has_permission(self, request, view):
		# 在这里编写权限逻辑，返回 True 表示有权限，返回 False 表示没有权限
		
		if request.method=='DELETE':
			return False
		else:
			return request.user.is_authenticated
	def has_object_permission(self, request, view, obj):
		# 在这里编写对象级别的权限逻辑，返回 True 表示有权限，返回 False 表示没有权限
		return obj.user == request.user
class UserResumeViewSet(viewsets.ModelViewSet):
	authentication_classes = [JWTAuthentication]
	# 搜索
	# filter_backends = [DjangoFilterBackend,SearchFilter, OrderingFilter]
	# search_fields = ('id',)
	# # 排序
	# ordering_fields = ('create_time', 'last_update')
	permission_classes = [CustomPermission]
	queryset = UserResume.objects
	serializer_class =UserResumeSerializer
	def perform_create(self, serializer):
		# Add a log entry for creating an order
		# 获取访问用户的ID
		u=user.objects.get(id=self.request.user.id)
		serializer.validated_data['user']=u
		instance=serializer.save()
		
		Logs.objects.create(user=u,active='新增简历',content=instance.to_json())
	def perform_update(self, serializer):
		# Add a log entry for updating an order
		
		instance = self.get_object()
		serializer.save()
		user = self.request.user
		Logs.objects.create(user=user,active='更新简历',content=instance.to_json())
	@action(detail=False, methods=['POST'])
	def uploadPhoto(self,request):
		data={
			'code':'200',
			'data':None,
			'msg':'ok',
		}
		try:
			serializer=PhotoSerializer(data=request.data)
			if serializer.is_valid():
				serializer.update(request.user,serializer.validated_data)
			else:
				data['code']=-1
				data['msg']='文件为空'
		except Exception as e:
			data['code']=-1
			data['msg']=str(e)
		return Response(data)
	@action(detail=False, methods=['POST'])
	def changebaseinfo(self,request):
		data={
			'code':'200',
			'data':None,
			'msg':'ok',
		}
		try:
			serializer=baseinfoSerializer(data=request.data)
			if serializer.is_valid():
				serializer.update(request.user,serializer.validated_data)

			else:
				data['code']=-1
				data['msg']=f'{serializer.errors}'
		except Exception as e:
			data['code']=-1
			data['msg']=str(e)
		return Response(data)
	@action(detail=False, methods=['POST'])
	def changeresumeinfo(self,request):
		data={
			'code':'200',
			'data':None,
			'msg':'ok',
		}
		try:
			serializer=resumeinfoSerializer(data=request.data)
			OBJ=UserResume.objects.filter(user=request.user).first()
			if serializer.is_valid():
				serializer.update(OBJ,serializer.validated_data)

			else:
				data['code']=-1
				data['msg']=f'{serializer.errors}'
		except Exception as e:
			data['code']=-1
			data['msg']=str(e)
		return Response(data)
	@action(detail=False, methods=['POST'])
	def changereadme(self,request):
		data={
			'code':'200',
			'data':None,
			'msg':'ok',
		}
		try:
			serializer=readmeSerializer(data=request.data)
			OBJ=UserResume.objects.filter(user=request.user).first()
			if serializer.is_valid():
				serializer.update(OBJ,serializer.validated_data)

			else:
				data['code']=-1
				data['msg']=f'{serializer.errors}'
		except Exception as e:
			data['code']=-1
			data['msg']=str(e)
		return Response(data)
	@action(detail=False, methods=['GET'])
	def resumeinfo(self,request):
		data={
			'code':'200',
			'data':None,
			'msg':'ok',
		}
		try:
			data['data']=self.get_queryset().filter(user=request.user).first().to_dict()
		except Exception as e:
			data['code']=-1
			data['msg']=str(e)
		return Response(data)
