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
import calendar
from rest_framework import generics
from django.db.models import Q

class SimilarJobsList(generics.ListAPIView):
	serializer_class = JobsSerializer

	def get_queryset(self):
		number = self.kwargs.get('number')
		job = Jobs.objects.get(number=number)

		query = (
			Q(industryname=job.industryname) &
			Q(education=job.education) &
			Q(worktype=job.worktype) &
			Q(workcity=job.workcity) &
			Q(educationcode__gte=job.educationcode) & 
			Q(salary_min__lte=job.salary_min) &
			Q(salary_max__gte=job.salary_max)
		)

		similar_jobs = Jobs.objects.filter(query).exclude(number=number)
		return similar_jobs

def get_random_objects(queryset, num_objects):
	random_objects = []
	total_objects = queryset.count()
	if num_objects >= total_objects:
		return list(queryset)
	while len(random_objects) < num_objects:
		random_index = random.randint(0, total_objects - 1)
		random_object = queryset[random_index]
		if random_object not in random_objects:
			random_objects.append(random_object)
	return random_objects
class CustomPermission(permissions.BasePermission):
	def has_permission(self, request, view):
		# 在这里编写权限逻辑，返回 True 表示有权限，返回 False 表示没有权限
		if request.method=='GET' or (  request.method=='POST' ):
			return True
		else:
			
			return False
	def has_object_permission(self, request, view, obj):
		# 在这里编写对象级别的权限逻辑，返回 True 表示有权限，返回 False 表示没有权限
		return True


class JobsFilter(filters.FilterSet):
	# jobid = filters.CharFilter(lookup_expr='exact')
	number = filters.CharFilter(lookup_expr='exact')
	# name = filters.CharFilter(lookup_expr='exact')
	educationcode = filters.CharFilter(lookup_expr='exact')
	# industrycompanytags = filters.CharFilter(lookup_expr='exact')
	# industryname = filters.CharFilter(lookup_expr='icontains')
	# jobsummary = filters.CharFilter(lookup_expr='exact')
	# positionurl = filters.CharFilter(lookup_expr='exact')
	# positionsourcetypeurl = filters.CharFilter(lookup_expr='exact')
	# property = filters.CharFilter(lookup_expr='exact')
	propertycode = filters.CharFilter(lookup_expr='exact')
	# recruitnumber = filters.CharFilter(lookup_expr='exact')
	# salary60 = filters.CharFilter(lookup_expr='exact')
	# salaryreal = filters.CharFilter(lookup_expr='exact')
	# salarytype = filters.CharFilter(lookup_expr='exact')
	# salarycounte = filters.CharFilter(lookup_expr='exact')
	salary=filters.NumberFilter(field_name='salary_min', lookup_expr='gte')
	salary2=filters.NumberFilter(field_name='salary_max', lookup_expr='lte')
	# skilllabel = filters.CharFilter(lookup_expr='icontains')
	publishtime = filters.DateFromToRangeFilter()
	cityid = filters.CharFilter(lookup_expr='icontains')
	citydistrict = filters.CharFilter(lookup_expr='exact')
	# streetid = filters.CharFilter(lookup_expr='icontains')
	# streetname = filters.CharFilter(lookup_expr='exact')
	subjobtypelevel = filters.CharFilter(lookup_expr='exact')
	# subjobtypelevelname = filters.CharFilter(lookup_expr='icontains')
	#待遇
	# welfaretaglist = filters.CharFilter(lookup_expr='icontains')
	# workcity = filters.CharFilter(lookup_expr='exact')
	#兼职全职..
	worktypecode = filters.NumberFilter(lookup_expr='exact')
	#工作经验
	workingexpcode = filters.NumberFilter(lookup_expr='exact')
	# companyid = filters.CharFilter(lookup_expr='exact')
	# companynumber = filters.CharFilter(lookup_expr='exact')
	# companyscaletypetagsnew = filters.CharFilter(lookup_expr='exact')
	# companyname = filters.CharFilter(lookup_expr='exact')
	# rootcompanynumber = filters.CharFilter(lookup_expr='exact')
	# companylogo = filters.CharFilter(lookup_expr='exact')
	# companysize = filters.CharFilter(lookup_expr='exact')
	# companyurl = filters.CharFilter(lookup_expr='exact')

	class Meta:
		model = Jobs
		fields = '__all__'
class JobsViewSet(viewsets.ModelViewSet):
	authentication_classes = [JWTAuthentication]
	# 搜索
	filter_backends = [DjangoFilterBackend,SearchFilter, OrderingFilter]
	search_fields = ('name',)
	# 排序
	ordering_fields = ('publishtime',)
	filterset_class =JobsFilter
	permission_classes = [CustomPermission]
	queryset = Jobs.objects
	serializer_class =JobsSerializer
	lookup_field ='number'


	@action(detail=False, methods=['POST'])
	def comment(self,request):
		data={
			'code':'200',
			'data':None,
			'msg':'ok',
		}
		if request.user.is_authenticated:
			try:
				serializer=CollectSerializer(data=request.data)
				content=request.data.get('content')
				if serializer.is_valid() and content:
					number=serializer.validated_data.get('number')
					job=Jobs.objects.filter(number=number).first()
					Comment=CommentJobs.objects

					Comment.create(user=request.user,job=job,content=content)
					data['data']='ok'
				else:
					# 参数有误
					data['code']='-1'
					data['msg']=serializer.errors	
			except Exception as e:
				data['code']='-1'
				data['data']=str(e)
				data['msg']='系统错误'
		else:
			data['code']=-1
			data['msg']='请登录'
		return Response(data)
	@action(detail=False, methods=['GET'])
	def commentJobs(self,request):
		data={
			'code':'200',
			'data':[],
			'msg':'ok',
		}
		if request.user.is_authenticated:
			try:
				serializer=RecommendSerializer(data=request.GET)
				number =request.GET.get('number ')
				if serializer.is_valid() and number :
					page=serializer.validated_data.get('page')
					pagesize=serializer.validated_data.get('pagesize')
					t=Jobs.objects.get(number=number )
					job_list=[{'id':i.cid,'username':i.user.username,'content':i.content,'create_time':i.create_time} for i in CommentJobs.objects.filter(job=t).order_by('-create_time')[(page-1)*pagesize:page*pagesize]]
					data['count']=CommentJobs.objects.filter(job=t).count()
					data['data']=job_list
				else:
					# 参数有误
					data['code']='-1'
					data['msg']=serializer.errors	
			except Exception as e:
				data['code']='-1'
				data['data']=str(e)
				data['msg']='系统错误'
		else:
			data['code']=-1
			data['msg']='请登录'
		return Response(data)
	@action(detail=False, methods=['POST'])
	def click(self,request):
		data={
			'code':'200',
			'data':None,
			'msg':'ok',
		}
		if request.user.is_authenticated:
			try:
				serializer=ClickSerializer(data=request.data)
				if serializer.is_valid():
					number=serializer.validated_data.get('number')
					job=Jobs.objects.filter(number=number).first()
					cli=ClickJobs.objects
					c=cli.filter(user=request.user,job=job)
					if not c.exists():
						cli.create(user=request.user,job=job)
					c.update(count=F('count')+1)
					data['data']=cli.filter(job=job).aggregate(sum=Sum('count'))
				else:
					# 参数有误
					data['code']='-1'
					data['msg']=serializer.errors	
			except Exception as e:
				data['code']='-1'
				data['data']=str(e)
				data['msg']='系统错误'
		else:
			serializer=ClickSerializer(data=request.data)
			if serializer.is_valid():
				number=serializer.validated_data.get('number')
				cli=ClickJobs.objects
				job=Jobs.objects.filter(number=number).first()
				data['data']=cli.filter(job=job).aggregate(sum=Sum('count'))
			else:
				data['code']='-1'
				data['msg']=serializer.errors
		
		return Response(data)
	@action(detail=False, methods=['POST'])
	def collect(self,request):
		data={
			'code':'200',
			'data':None,
			'msg':'ok',
		}
		if request.user.is_authenticated:
			try:
				serializer=CollectSerializer(data=request.data)
				if serializer.is_valid():
					number=serializer.validated_data.get('number')
					job=Jobs.objects.filter(number=number).first()
					star=StarJobs.objects
					if star.filter(user=request.user,job=job).exists():
						data['code']='-1'
						data['msg']='已收藏'
						return Response(data)
					star.create(user=request.user,job=job)
					data['data']=job.to_dict('收藏')
				else:
					# 参数有误
					data['code']='-1'
					data['msg']=serializer.errors	
			except Exception as e:
				data['code']='-1'
				data['data']=str(e)
				data['msg']='系统错误'
		else:
			data['code']=-1
			data['msg']='请登录'
		return Response(data)
	@action(detail=False, methods=['GET'])
	def collectjobs(self,request):
		data={
			'code':'200',
			'data':[],
			'msg':'ok',
		}
		if request.user.is_authenticated:
			try:
				serializer=RecommendSerializer(data=request.GET)
				if serializer.is_valid():
					page=serializer.validated_data.get('page')
					pagesize=serializer.validated_data.get('pagesize')
					res=StarJobs.objects.filter(user=request.user)
					job_list=[i.job.to_dict(None) for i in res[(page-1)*pagesize:page*pagesize]]
					data['count']=res.count()
					data['data']=job_list
				else:
					# 参数有误
					data['code']='-1'
					data['msg']=serializer.errors	
			except Exception as e:
				data['code']='-1'
				data['data']=str(e)
				data['msg']='系统错误'
		else:
			data['code']=-1
			data['msg']='请登录'
		return Response(data)
	@action(detail=False, methods=['GET'])
	def clickjobs(self,request):
		data={
			'code':'200',
			'data':[],
			'msg':'ok',
		}
		if request.user.is_authenticated:
			try:
				serializer=RecommendSerializer(data=request.GET)
				if serializer.is_valid():
					page=serializer.validated_data.get('page')
					pagesize=serializer.validated_data.get('pagesize')
					res=ClickJobs.objects.filter(user=request.user)
					job_list=[i.job.to_dict(None) for i in res[(page-1)*pagesize:page*pagesize]]
					data['count']=res.count()
					data['data']=job_list
				else:
					# 参数有误
					data['code']='-1'
					data['msg']=serializer.errors	
			except Exception as e:
				data['code']='-1'
				data['data']=str(e)
				data['msg']='系统错误'
		else:
			data['code']=-1
			data['msg']='请登录'
		return Response(data)
	@action(detail=False, methods=['POST'])
	def iscollected(self,request):
		data={
			'code':'200',
			'data':None,
			'msg':'ok',
		}
		if request.user.is_authenticated:
			try:
				serializer=CollectSerializer(data=request.data)
				if serializer.is_valid():
					number=serializer.validated_data.get('number')
					job=Jobs.objects.filter(number=number).first()
					star=StarJobs.objects
					if star.filter(user=request.user,job=job).exists():
						data['data']=True
						data['msg']='已收藏'
						return Response(data)
					data['data']=False
					data['msg']='未收藏'
				else:
					# 参数有误
					data['code']='-1'
					data['msg']=serializer.errors	
			except Exception as e:
				data['code']='-1'
				data['data']=str(e)
				data['msg']='系统错误'
		else:
			data['code']=-1
			data['msg']='请登录'
		return Response(data)
	@action(detail=False, methods=['POST'])
	def removecollect(self,request):
		data={
			'code':'200',
			'data':None,
			'msg':'ok',
		}
		if request.user.is_authenticated:
			try:
				serializer=CollectSerializer(data=request.data)
				if serializer.is_valid():
					number=serializer.validated_data.get('number')
					job=Jobs.objects.filter(number=number).first()
					
					star=StarJobs.objects
					if not star.filter(user=request.user,job=job).exists():
						data['code']='-1'
						data['msg']='未收藏'
						return Response(data)
					star.filter(user=request.user,job=job).delete()
					data['data']=job.to_dict('取消收藏')
				else:
					# 参数有误
					data['code']='-1'
					data['msg']=serializer.errors	
			except Exception as e:
				data['code']='-1'
				data['data']=str(e)
				data['msg']='系统错误'
		else:
			data['code']=-1
			data['msg']='请登录'
		return Response(data)
	@action(detail=False, methods=['GET'])
	def recommend(self,request):
		data={
			'code':'200',
			'data':None,
			'msg':'ok',
			'count':200
		}
		serializer=RecommendSerializer(data=request.GET)
		if serializer.is_valid():
			try:
				page=serializer.validated_data.get('page')
				pagesize=serializer.validated_data.get('pagesize')
				maxpage=10
				#最新随机列表limit
				newlimit=1000
				jobs=Jobs.objects.order_by('-id')[:newlimit]
				if request.user.is_authenticated :
					user_id=request.user.id
					if page==1:
						#首页实时推荐，根据收藏推荐
						star_job_list=[i.job for i in StarJobs.objects.filter(user_id=user_id).order_by('create_time')] 
						star_user_list=[i.user for i in StarJobs.objects.filter(job__in=star_job_list[:100]).exclude(user_id=user_id).distinct()]
						#点击
						click_job_list=[i.job for i in ClickJobs.objects.filter(user_id=user_id).order_by('create_time','count')] 
						click_user_list=[i.user for i in StarJobs.objects.filter(job__in=click_job_list[:100]).exclude(user_id=user_id).distinct()]
						similar_job_list=StarJobs.objects.values('job').filter(user__in=star_user_list[:100]).union(ClickJobs.objects.values('job').filter(user__in=click_user_list[:100]))
						job_list=[Jobs.objects.get(id=i.get('job')).to_dict('实时') for i in get_random_objects(similar_job_list,pagesize//2)]
						length=len(job_list)
						if length<pagesize:
							# 热门数据填充
							job_id_list = [i.job_id for i in hotjobs_TOP20.objects.all()]
							job_list+=[i.to_dict('热门') for i in Jobs.objects.filter(job_id__in=job_id_list[:pagesize-length])]
						#填充完还小于pagesize条，使用job数据随机填充
						length=len(job_list)
						if length<pagesize:
							job_list+=[i.to_dict('最新随机') for i in get_random_objects(jobs,pagesize-length)]
					else:
						#如果有离线推荐数据
						Rrecommend=Recommendforallusers.objects.filter(user_id=user_id)
						if Rrecommend.exists():
							job_id_list=Rrecommend.first().recommend_job_list[(page-2)*pagesize:(page-1)*pagesize]
							job_list=[i.to_dict('匹配') for i in Jobs.objects.filter(job_id__in=job_id_list)]
						else:
							# 热门数据填充
							# 获取热门的 job_list
							job_id_list = [i.job_id for i in hotjobs_TOP20.objects.all()]
							job_list=[i.to_dict('热门') for i in Jobs.objects.filter(job_id__in=job_id_list)]
							if job_list==[] or len(job_list)<pagesize:
								job_list+=[i.to_dict('最新随机') for i in get_random_objects(jobs,pagesize-len(job_list))]

				else:
					if page==1:
						# 热门数据填充
						job_id_list = [i.job_id for i in hotjobs_TOP20.objects.all()]
						job_list=[i.to_dict('热门') for i in Jobs.objects.filter(job_id__in=job_id_list)]
						#最新随机数据填充
						if job_list==[] or len(job_list)<pagesize:
								job_list+=[i.to_dict('最新随机') for i in get_random_objects(jobs,pagesize-len(job_list))]
					else:
						job_list=[i.to_dict('最新随机') for i in get_random_objects(jobs,pagesize)]
				data['data']=job_list
				data['page']=page
			except Exception as e:
				data['code']='-1'
				data['data']=str(e)
				data['msg']='系统错误'
		else:
			# 参数有误
			data['code']='-1'
			data['msg']=serializer.errors
		return Response(data)
	

	@action(detail=False, methods=['GET'])	
	def bigdata_info(self, request):
		

		queryset = self.filter_queryset(self.get_queryset())
		data={}
		data['count']=company.objects.aggregate(sum=Count('companyid')).values() 
		data['total']=queryset.aggregate(sum=Count('id')).values() 
		return Response({'msg':'OK','code':'200','data':data})
	@action(detail=False, methods=['GET'])	
	def education_info(self, request):
		


		queryset = self.filter_queryset(self.get_queryset())
		total=queryset.aggregate(sum=Avg('salary_min')).values() 
		data=queryset.filter(salary_min__gt=0).values('education').annotate(name=F('education'),sum=Avg('salary_min')).order_by('-sum')[:5]
		return Response({'msg':'OK','code':'200','data':data,'total':total})
	
	@action(detail=False, methods=['GET'])	
	def worktype_info(self, request):


		queryset = self.filter_queryset(self.get_queryset())
		data=queryset.values('worktype').annotate(name=F('worktype'),value=Count('id')).order_by('-value')[:10]
		return Response({'msg':'OK','code':'200','data':data})
	@action(detail=False, methods=['GET'])	
	def property_info(self, request):
		


		queryset = self.filter_queryset(self.get_queryset())
		total=queryset.aggregate(sum=Avg('salary_min')).values() 
		data=queryset.filter(salary_min__gt=0).values('property').annotate(name=F('property'),sum=Avg('salary_min')).order_by('-sum')[:10]
		return Response({'msg':'OK','code':'200','data':data,'total':total})
	
	@action(detail=False, methods=['GET'])	
	def workcity_info(self, request):


		queryset = self.filter_queryset(self.get_queryset())
		data=queryset.filter(salary_min__gt=0).values('workcity').annotate(name=F('workcity'),value=Sum('salary_min')).order_by('-value')[:10]
		return Response({'msg':'OK','code':'200','data':data})