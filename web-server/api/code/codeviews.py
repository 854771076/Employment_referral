from rest_framework.throttling import *
# 导入所需的模块和库
from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework.permissions import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from api.utils.redis import getRedisConnection
from django.http import HttpResponse
from django.conf import settings
from PIL import Image, ImageDraw,ImageFont
from io import BytesIO
from django.contrib.auth.hashers import make_password
import random
# 生成验证码
def generate_verification_code():
	# 这里你可以使用任何适合你的验证码生成方法
	# 比如生成一个6位随机数
	import random
	return str(random.randint(100000, 999999))

# 发送邮件
def send_verification_email(email,code,action):
	# 构建邮件内容
	subject = '验证码'
	message = f'您的验证码是：{code}'
	email_from = f'safe <{settings.DEFAULT_FROM_EMAIL}>'  # 发件人邮箱
	recipient_list = [email]  # 收件人邮箱
	template_name = 'verification_email.html'  # 模板文件路径
	context = {'verification_code': code,'action':action,'email':email}
	html_message = render_to_string(template_name, context)
	send_mail(subject, message, email_from, recipient_list, html_message=html_message)
class CaptchaRateThrottle(AnonRateThrottle):
	rate='10000/m'
class CaptchaAPIView(APIView):
	authentication_classes = [JWTAuthentication]
	permission_classes = [AllowAny]
	throttle_classes=[CaptchaRateThrottle]
	def get(self, request):
		# 生成四位随机验证码
		length=int(request.GET.get('length',4))
		if length<2:
			length=2
		if length>6:
			length=6
		captcha = ''.join(random.choices('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', k=length))
		# 创建图片对象，设置字体和字体大小
		img = Image.new('RGB', (150, 50), color=(255, 255, 255))
		draw = ImageDraw.Draw(img)
		font = ImageFont.truetype("api/code/ARIALI.TTF", 35)
		# 在图片上绘制验证码
		draw.text((10, 10), captcha, font=font, fill=(random.randint(0,150), random.randint(0,255), random.randint(0,255)))
		# 绘制干扰线
		for _ in range(10):
			x1 = random.randint(0, 150)
			y1 = random.randint(0, 50)
			x2 = random.randint(0, 150)
			y2 = random.randint(0, 50)
			draw.line((x1, y1, x2, y2), fill=(0, 0, 0))
		buffer = BytesIO()
		img.save(buffer, format='PNG')
		# 把验证码存储在session中，以便后续验证
		data = buffer.getvalue()
		# 输出图片
		response = HttpResponse(data,content_type="image/png")
		response.set_cookie('captcha',make_password(captcha.lower()))
		return response	
class EmailCodeThrottle(UserRateThrottle):
	rate = '10/m'
	
class EmailCodeView(APIView):
	authentication_classes = [JWTAuthentication]
	permission_classes = [AllowAny]
	throttle_classes=[EmailCodeThrottle]
	def post(self, request, *args, **kwargs):
		try:
			email=request.data.get('email')
   			#后期通过该数据分隔各个功能验证码
			action=request.data.get('action')
			code=generate_verification_code()
			send_verification_email(email,code,action)
			r = getRedisConnection()
			r.set(email, code)
			r.expire(email, 180)
			return Response({'code': 200,'msg': '发送成功！'})  
		except Exception as e:	
	  		return Response({'code': 501,'msg': '发送失败！','error':str(e)})  