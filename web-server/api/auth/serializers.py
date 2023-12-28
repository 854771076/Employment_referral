from rest_framework import serializers
from api.models import user
import datetime
from django.utils.translation import ugettext_lazy as _
from api.utils.redis import getRedisConnection
from django.contrib.auth.hashers import make_password,check_password
class UserRegisterSerializer(serializers.ModelSerializer):
    username=serializers.CharField(required=False,min_length=4,max_length=100)
    password=serializers.CharField(required=True,min_length=8,max_length=16)
    checkpassword=serializers.CharField(required=True,min_length=8,max_length=16)
    email = serializers.EmailField(required=True,max_length=50)
    phone=serializers.CharField(required=True,min_length=8,max_length=11)
    code=serializers.CharField(required=True,min_length=6,max_length=6)
    class Meta:
        model=user
        fields=['username','password','checkpassword','email','phone','code']
    def create(self, validated_data):
        validated_data.pop('code')
        validated_data.pop('checkpassword')
        validated_data['username']='JF'+str(100000+user.objects.all().count())
        u = user.objects.create(**validated_data)
        return u
    def validate_email(self,data):
        try:
            user.objects.get(email=data)
        except user.DoesNotExist:
            return data
        raise serializers.ValidationError(_("邮箱已注册"))
    def validate_code(self,data):
        
        code=getRedisConnection().get(self.initial_data['email'])
        if not code:
            raise serializers.ValidationError(_("请发送验证码"))
        if data!=code:
            raise serializers.ValidationError(_("验证码错误"))
        return data
    def validate(self,data):
        
        if 'password' in data and 'checkpassword' in data:
            if data['password'] != data['checkpassword']:
                raise serializers.ValidationError(_("两次密码不一致"))
        data['password']=make_password(data['password'])
        return data           
class UserLoginSerializer(serializers.ModelSerializer):
    account=serializers.CharField(required=True,min_length=4,max_length=100)
    pwd=serializers.CharField(required=True,min_length=8,max_length=16)

    class Meta:
        model=user
        fields=['account','pwd','last_login']
   
    def validate(self,data):
        try:
            a=user.objects.get(phone=data['account'])
            data['account']=a
            # data['type']='phone'
        except user.DoesNotExist:
            try:
                a=user.objects.get(email=data['account'])
                data['account']=a
                # data['type']='email'
            except user.DoesNotExist:
                try:
                    a=user.objects.get(username=data['account'])
                    data['account']=a
                    # data['type']='username'
                except user.DoesNotExist:
                    raise serializers.ValidationError(_("账号未注册！"))
        data['last_login']=datetime.datetime.now()
        return data

class UserForegetSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(required=True,max_length=50)
    password=serializers.CharField(required=True,min_length=8,max_length=16)
    checkpassword=serializers.CharField(required=True,min_length=8,max_length=16)
    code=serializers.CharField(required=True,min_length=6,max_length=6)

    class Meta:
        model=user
        fields=['email','password','checkpassword','code']

    def validate_code(self,data):
            
        code=getRedisConnection().get(self.initial_data['email'])
        if not code:
            raise serializers.ValidationError(_("请发送验证码"))
        if data!=code:
            raise serializers.ValidationError(_("验证码错误"))
        return data
    def validate_email(self,data):
        try:
            user.objects.get(email=data)
            return data
        except user.DoesNotExist:
            raise serializers.ValidationError(_("邮箱未注册！"))
    def validate(self,data):
        U=user.objects.get(email=data['email'])
        if data['password'] != data['checkpassword']:
            raise serializers.ValidationError(_("两次密码不一致！"))
        if check_password(data['password'],U.password):
            raise serializers.ValidationError(_("新旧密码不可相同！"))
        
        data['password']=make_password(data['password'])
        return data    
class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        exclude = ['password','groups','user_permissions','first_name','last_name']