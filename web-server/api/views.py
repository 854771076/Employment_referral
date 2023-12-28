from django.shortcuts import render
# Create your views here.
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import *
from rest_framework.views import APIView
from rest_framework.response import Response
from json import loads
class baseDataView(APIView):
	# 局部认证类：无需认证即可访问此视图，优先级高于全局认证类
	authentication_classes = [JWTAuthentication]
	permission_classes =[AllowAny ]
	def get(self, request, *args, **kwargs):
		data=open('static/json/baseData.json','r',encoding='utf-8').read()
		return Response(loads(data))