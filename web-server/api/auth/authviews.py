from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import user,UserResume

from api.auth.serializers import *
from rest_framework.permissions import *
from rest_framework.throttling import *
from django.contrib.auth.hashers import make_password,check_password
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from api.utils.redis import getRedisConnection

def authenticate(username=None, password=None, **kwargs):
	try:
		u = user.objects.get(phone=username)
	except:
		try:
			u = user.objects.get(username=username)
		except:
			try:
				u = user.objects.get(email=username)
			except:
				u = None
	if u and u.check_password(password):
		return u
def generate_tokens(user_object):
	access_token = AccessToken.for_user(user_object)
	refresh_token = RefreshToken.for_user(user_object)

	return {
		'access_token': str(access_token),
		'refresh_token': str(refresh_token),
	}

class UserInfoView(APIView):
	"""
	返回用户基本信息
	"""
	authentication_classes = [JWTAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, *args, **kwargs):
		
		Serializer = UserInfoSerializer(request.user)
		return Response({'code': 200, 'msg': "成功",'data':Serializer.data})

# 注册账号
class SignupView(APIView):
	# 局部认证类：无需认证即可访问此视图，优先级高于全局认证类
	authentication_classes = [JWTAuthentication]
	permission_classes = [AllowAny]
	def post(self, request, *args, **kwargs):
		
		Serializer = UserRegisterSerializer(data=request.data)
		if Serializer.is_valid():
			Serializer.save()
			return Response({'code': 200, 'msg': "注册成功"})
			
		else:
			errors={
				'non_field_errors':501,
				'name':502,
				'email':503,
				'password':504,
				'checkpassword':505,
				'code':506
			}
			for i in Serializer.errors.keys():
				return Response({'code': errors.get(i,507), 'error': Serializer.errors.get(i)[0]})

class LoginView(APIView):
	# 局部认证类：无需认证即可访问此视图，优先级高于全局认证类
	authentication_classes = [JWTAuthentication]
	permission_classes = [AllowAny]
	def post(self, request, *args, **kwargs):
		Serializer = UserLoginSerializer(data=request.data)
		code=request.data.get('code')
		rel_code=request.COOKIES.get('captcha')

		if not rel_code or not code or not check_password(code.lower(),rel_code):
			resp=Response({'code': 501, 'error': "验证码错误!"})
			resp.delete_cookie('captcha')
			return resp
		if Serializer.is_valid():
			
			account=Serializer.data['account']
			password=Serializer.data['pwd']
			user_object=authenticate(username=account,password=password)
			
			# 若账号不在账号表中，即未搜索到user_post对应的username的对象
			if not user_object:
				# 返回字符串： return Response("用户不存在")
				resp=Response({'code': 502, 'error': "用户名或密码不正确"})
				resp.delete_cookie('captcha')
				return resp
			elif not user_object.is_active:
				resp=Response({'code': 503, 'error': "账号禁用"})
				resp.delete_cookie('captcha')
				return resp
			Serializer.update(user_object,Serializer.validated_data)
			resp=Response({'code': 200, 'tokens': generate_tokens(user_object)})
			resp.delete_cookie('captcha')
			return resp

		else:
			errors={
				'non_field_errors':504,
				'pwd':505,
				'account':506
			}
			for i in Serializer.errors.keys():
				resp=Response({'code': errors.get(i,507), 'error': Serializer.errors.get(i)[0]})
				resp.delete_cookie('captcha')
				return resp

	



class ForegetPSWView(APIView):
	authentication_classes = [JWTAuthentication]
	permission_classes = [AllowAny]
	def post(self, request, *args, **kwargs):
		Serializer = UserForegetSerializer(data=request.data)
		if Serializer.is_valid():
			u=user.objects.get(email=Serializer.validated_data.get('email'))
			Serializer.update(u,Serializer.validated_data)
			return Response({'code': 200,'msg': '修改成功！'})         
		else:
			errors={
				'non_field_errors':501,
				'email':502,
				'password':503,
				'checkpassword':504,
				'code':505,
			}
			for i in Serializer.errors.keys():
				return Response({'code': errors.get(i,506), 'error': Serializer.errors.get(i)[0]})
