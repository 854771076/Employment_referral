from django.db import models
from django.contrib.auth.models import AbstractUser
import os
from datetime import date
from django.db.models.signals import post_save
from django.dispatch import receiver
from json import dumps,loads
def user_directory_path(instance, filename):
    ext = filename.split('.').pop()
    filename = 'headerpic.'+ext
    return os.path.join(str(instance), filename)  # 系统路径分隔符差异，增强代码重用性
class CommentJobs(models.Model):
    cid=models.BigAutoField(primary_key=True)
    user=models.ForeignKey('api.user', verbose_name="用户", on_delete=models.CASCADE)
    job=models.ForeignKey('api.Jobs', verbose_name="职位", on_delete=models.CASCADE)
    content=models.TextField(verbose_name='内容')
    create_time = models.DateTimeField(auto_now=False,auto_now_add=True, verbose_name='创建时间')
    class Meta:
        verbose_name = '评论列表'
        db_table = 'comment'  
class Jobs(models.Model):
    id=models.BigAutoField(primary_key=True)
    job_id = models.IntegerField(blank=True, null=True)
    jobid = models.CharField(max_length=255,blank=True, null=True)
    number = models.CharField(max_length=255,blank=True, null=True)
    name = models.CharField(max_length=255,blank=True, null=True)
    educationcode = models.IntegerField(blank=True, null=True)
    education = models.CharField(max_length=255,blank=True, null=True)
    industrycompanytags = models.CharField(max_length=255,blank=True, null=True)
    industryname = models.CharField(max_length=255,blank=True, null=True)
    jobsummary = models.TextField(blank=True, null=True)
    positionurl = models.CharField(max_length=255,blank=True, null=True)
    positionsourcetypeurl = models.CharField(max_length=255,blank=True, null=True)
    property = models.CharField(max_length=255,blank=True, null=True)
    propertycode = models.CharField(max_length=255,blank=True, null=True)
    recruitnumber = models.CharField(max_length=255,blank=True, null=True)
    salary60 = models.CharField(max_length=255,blank=True, null=True)
    salaryreal = models.CharField(max_length=255,blank=True, null=True)
    salary_min=models.IntegerField(blank=True, null=True)
    salary_max=models.IntegerField(blank=True, null=True)
    salarytype = models.CharField(max_length=255,blank=True, null=True)
    salarycounte = models.CharField(max_length=255,blank=True, null=True)
    skilllabel = models.CharField(max_length=255,blank=True, null=True)
    publishtime = models.DateTimeField(blank=True, null=True)
    cityid = models.TextField(blank=True, null=True)
    citydistrict = models.CharField(max_length=255,blank=True, null=True)
    streetid = models.TextField(blank=True, null=True)
    streetname = models.CharField(max_length=255,blank=True, null=True)
    subjobtypelevel = models.TextField(blank=True, null=True)
    subjobtypelevelname = models.CharField(max_length=255,blank=True, null=True)
    welfaretaglist = models.TextField(blank=True, null=True)
    workcity = models.TextField(blank=True, null=True)
    worktypecode = models.TextField(blank=True, null=True)
    worktype = models.CharField(max_length=255,blank=True, null=True)
    workingexpcode = models.TextField(blank=True, null=True)
    workingexp = models.CharField(max_length=255,blank=True, null=True)
    companyid = models.CharField(max_length=255,blank=True, null=True)
    companynumber = models.CharField(max_length=255,blank=True, null=True)
    companyscaletypetagsnew = models.CharField(max_length=255,blank=True, null=True)
    companyname = models.CharField(max_length=255,blank=True, null=True)
    rootcompanynumber = models.CharField(max_length=255,blank=True, null=True)
    companylogo = models.TextField(blank=True, null=True)
    companysize = models.CharField(max_length=255,blank=True, null=True)
    companyurl = models.TextField(blank=True, null=True)

    def to_dict(job,type):
        # 将模型实例转换为字典
        job_dict = {
            'type':type,
            'job_id': job.job_id,
            'jobid': job.jobid,
            'number': job.number,
            'name': job.name,
            'educationcode': job.educationcode,
            'education': job.education,
            'industrycompanytags': job.industrycompanytags,
            'industryname': job.industryname,
            'jobsummary': dumps(job.jobsummary),
            'positionurl': job.positionurl,
            'positionsourcetypeurl': job.positionsourcetypeurl,
            'property': job.property,
            'propertycode': job.propertycode,
            'recruitnumber': job.recruitnumber,
            'salary60': job.salary60,
            'salaryreal': job.salaryreal,
            'salary_min': job.salary_min,
            'salary_max': job.salary_max,
            'salarytype': job.salarytype,
            'salarycounte': job.salarycounte,
            'skilllabel': job.skilllabel,
            'publishtime': job.publishtime.isoformat(),
            'cityid': job.cityid,
            'citydistrict': job.citydistrict,
            'streetid': job.streetid,
            'streetname': job.streetname,
            'subjobtypelevel': job.subjobtypelevel,
            'subjobtypelevelname': job.subjobtypelevelname,
            'welfaretaglist': job.welfaretaglist,
            'workcity': job.workcity,
            'worktypecode': job.worktypecode,
            'worktype': job.worktype,
            'workingexpcode': job.workingexpcode,
            'workingexp': job.workingexp,
            'companyid': job.companyid,
            'companynumber': job.companynumber,
            'companyscaletypetagsnew': job.companyscaletypetagsnew,
            'companyname': job.companyname,
            'rootcompanynumber': job.rootcompanynumber,
            'companylogo': job.companylogo,
            'companysize': job.companysize,
            'companyurl': job.companyurl,
        }
        # 将字典转换为JSON字符串并返回
        return job_dict
    class Meta:
        # managed = False
        verbose_name = '职位列表'
        db_table = 'jobs'
class UserResume(models.Model):
    class Sex(models.TextChoices):
        男 = '1'
        女 = '0'
    id=models.BigAutoField(primary_key=True)
    user=models.OneToOneField('api.user', on_delete=models.CASCADE,null=True,blank=True)
    eduHighestLevel=models.IntegerField( verbose_name='教育水平编码',default=0, null=True,blank=True)
    eduHighestLevelTranslation=models.CharField(max_length=10, verbose_name='教育水平', null=True,blank=True)
    workingexpCode=models.IntegerField(verbose_name='工作经验id',default=0, null=True,blank=True)
    workingexp=models.CharField(max_length=20, verbose_name='工作经验', default='无经验',blank=True)
    worktypeCode=models.IntegerField(verbose_name='期望工作类型id', default=0,null=True,blank=True)
    worktype=models.CharField(max_length=20, verbose_name='期望工作类型', default='无经验',null=True,blank=True)
    workcity=models.IntegerField(verbose_name='期望工作城市id',default=0,null=True,blank=True)
    workcityTranslation=models.CharField(max_length=20, verbose_name='期望工作城市', null=True,blank=True)
    workcity2=models.IntegerField(verbose_name='期望工作城市2id',default=0,null=True,blank=True)
    workcity2Translation=models.CharField(max_length=20, verbose_name='期望工作城市2', null=True,blank=True)
    workcity3=models.IntegerField(verbose_name='期望工作城市3id',default=0,null=True,blank=True)
    workcity3Translation=models.CharField(max_length=20, verbose_name='期望工作城市3', null=True,blank=True)
    subjobtypelevel=models.BigIntegerField( verbose_name='期望工作类型编码',default=0, null=True,blank=True)
    subjobtypelevelname=models.CharField(max_length=20, verbose_name='期望工作类型',default=0, null=True,blank=True)
    skilllabel=models.CharField(max_length=255,verbose_name='技能标签（/隔开）', null=True,blank=True)
    propertycode=models.BigIntegerField(verbose_name='期望企业类型编码',default=0, null=True,blank=True)
    property=models.CharField(max_length=20,verbose_name='期望企业类型', null=True,blank=True)
    preferredSalaryMin=models.IntegerField(verbose_name='期望最低工资',default=0, null=True,blank=True)
    preferredSalaryMax=models.IntegerField(verbose_name='期望最高工资',default=0, null=True,blank=True)
    SelfEvaluate=models.TextField(max_length=20,verbose_name='自我介绍', null=True,blank=True)    
    # email
    # phone
    
    
    created_time = models.DateTimeField(auto_now_add=True)  # 添加创建时间字段
    last_update = models.DateTimeField(auto_now=True, verbose_name='最后修改时间')
    def to_dict(self):
        resume_data = {
            'id': self.id,
            'user_id': self.user.id,
            'name': self.user.name,
            'email':self.user.email,
            "phone":self.user.phone,
            'photo':'/media/'+str(self.user.photo),
            'birth': self.user.birth.strftime('%Y-%m-%d') if self.user.birth else '',
            'genderCode': str(self.user.genderCode).replace("None",""),
            'genderTranslation': self.user.genderTranslation,
            'currentIdentity': self.user.currentIdentity,
            'currentCity': str(self.user.currentCity).replace("None",""),
            'currentCityTranslation': self.user.currentCityTranslation,
            'currentCityDistrictId': str(self.user.currentCityDistrictId).replace("None",""),
            'currentCityDistrictIdTranslation': self.user.currentCityDistrictIdTranslation,
            'currentProvince': str(self.user.currentProvince).replace("None",""),
            'currentProvinceTranslation': self.user.currentProvinceTranslation,
            'eduHighestLevel': str(self.eduHighestLevel).replace("None",""),
            'eduHighestLevelTranslation': self.eduHighestLevelTranslation,
            'politicalAffiliation': self.user.politicalAffiliation,
            'workingexpCode':str(self.workingexpCode).replace("None",""),
            'workingexp': self.workingexp,
            'worktypeCode':str(self.worktypeCode).replace("None",""),
            'worktype': self.worktype,
            'workcityTranslation': self.workcityTranslation,
            'workcity2Translation': self.workcity2Translation,
            'workcity3Translation': self.workcity3Translation,
            'workcity': str(self.workcity).replace("None",""),
            'workcity2': str(self.workcity2).replace("None",""),
            'workcity3': str(self.workcity3).replace("None",""),
            'subjobtypelevel': str(self.subjobtypelevel).replace("None",""),
            'subjobtypelevelname': self.subjobtypelevelname,
            'skilllabel': self.skilllabel,
            'propertycode': str(self.propertycode).replace("None",""),
            'property': self.property,
            'preferredSalaryMin': self.preferredSalaryMin,
            'preferredSalaryMax': self.preferredSalaryMax,
            'SelfEvaluate': self.SelfEvaluate,
            'created_time': self.created_time.strftime('%Y-%m-%d %H:%M:%S'),
            'last_update': self.last_update.strftime('%Y-%m-%d %H:%M:%S'),
        }

        return resume_data
    class Meta:
        verbose_name = '用户简历信息'
        db_table = 'resume'
        verbose_name_plural = verbose_name
        
class company(models.Model):
   
    companyid=models.CharField(max_length=255)
    rootcompanynumber=models.CharField(max_length=255,null=True)
    companynumber=models.CharField(max_length=255,primary_key=True)
    companyscaletypetagsnew=models.CharField(max_length=255,null=True,verbose_name='标签')
    companyname=models.CharField(max_length=255,null=True)
    companylogo=models.TextField(null=True)
    industryCompanyTags=models.CharField(max_length=255,null=True)
    propertycode=models.CharField(max_length=255,null=True)
    property=models.CharField(max_length=255,null=True)
    industryName=models.CharField(max_length=255,null=True)
    companysize=models.CharField(max_length=255,null=True)
    companyurl=models.TextField(null=True)
    job_num= models.IntegerField(  default=0, null=True)
    class Meta:
        verbose_name = '企业基本信息'
        db_table = 'company'
        managed = False
        verbose_name_plural = verbose_name
    def to_dict(self):
        return {
            'id': self.id,
            'companyid': self.companyid,
            'rootcompanynumber': self.rootcompanynumber,
            'companynumber': self.companynumber,
            'companyscaletypetagsnew': self.companyscaletypetagsnew,
            'companyname': self.companyname,
            'companylogo': self.companylogo,
            'industryCompanyTags':self.industryCompanyTags,
            'industryName':self.industryName,
            'propertycode':self.propertycode,
            'property':self.property,
            'companysize': self.companysize,
            'companyurl': self.companyurl,
            'job_num': self.job_num,
        }
    
class user(AbstractUser):

    name=models.CharField(max_length=10, verbose_name='姓名',null=True)
    birth=models.DateField(verbose_name='生日',null=True)
    genderCode= models.IntegerField(  default='1', verbose_name='性别id 男 1 女 0',null=True)
    genderTranslation= models.CharField(max_length=2, default='男', verbose_name='性别',null=True)

    currentIdentity=models.CharField(max_length=10, verbose_name='求职者身份',null=True)
    currentCity=models.IntegerField(verbose_name='城市id',null=True)
    currentCityTranslation=models.CharField(max_length=20, verbose_name='城市',null=True)
    currentCityDistrictId=models.IntegerField(verbose_name='区域id',null=True)
    currentCityDistrictIdTranslation=models.CharField(max_length=20, verbose_name='区域',null=True)
    currentProvince=models.IntegerField(verbose_name='省id',null=True)
    currentProvinceTranslation=models.CharField(max_length=10, verbose_name='省',null=True)
    politicalAffiliation=models.CharField(max_length=10, verbose_name='政治面貌',null=True)
    phone = models.CharField(max_length=11, verbose_name='手机号', null=False)
    photo = models.ImageField('头像', upload_to=user_directory_path, blank=True, null=True,default='default/user.jpg')
    last_update = models.DateTimeField(auto_now=True, verbose_name='最后修改时间')    
    def __str__(self):
        return f'{self.username}'
    class Meta:
        verbose_name = '用户信息'
        db_table = 'user'
        verbose_name_plural = verbose_name


class Logs(models.Model):
    lid=models.BigAutoField(primary_key=True)
    user=models.ForeignKey(user, verbose_name="用户", on_delete=models.DO_NOTHING,null=True)
    active=models.TextField(verbose_name='行为')
    content=models.TextField(verbose_name='内容')
    create_time = models.DateTimeField(auto_now=False,auto_now_add=True, verbose_name='创建时间')
    class Meta:
        verbose_name = '操作日志'
        db_table = 'logs'
        verbose_name_plural = verbose_name
        
class Recommendforallusers(models.Model):
    user_id = models.IntegerField(primary_key=True)
    recommendations = models.TextField(blank=True, null=True)
    @property
    def recommend_job_list(self):
        
        return [i.get('job_id') for i in loads(self.recommendations)]
    class Meta:
        verbose_name = '用户推荐列表'
        managed = False
        db_table = 'recommendforallusers'
        
class StarJobs(models.Model):
    sid=models.BigAutoField(primary_key=True)
    user=models.ForeignKey('api.user', verbose_name="用户", on_delete=models.CASCADE)
    job=models.ForeignKey('api.Jobs', verbose_name="岗位", on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now=False,auto_now_add=True, verbose_name='创建时间')
    class Meta:
        verbose_name = '职位收藏列表'
        db_table = 'starjobs'
        
class ClickJobs(models.Model):
    cid=models.BigAutoField(primary_key=True)
    user=models.ForeignKey('api.user', verbose_name="用户", on_delete=models.CASCADE)
    job=models.ForeignKey('api.Jobs', verbose_name="岗位", on_delete=models.CASCADE)
    count=models.IntegerField(default=1)
    create_time = models.DateTimeField(auto_now=False,auto_now_add=True, verbose_name='创建时间')
    last_update = models.DateTimeField(auto_now=True,auto_now_add=False, verbose_name='最后修改时间')
    class Meta:
        verbose_name = '职位浏览列表'
        db_table = 'clickjobs'
class hotjobs_TOP20(models.Model):
    job_id=models.IntegerField(primary_key=True)
    weight=models.IntegerField(null=True)
    class Meta:
        managed = False
        verbose_name = '职位热门列表'
        db_table = 'hotjobs_top20'
@receiver(post_save, sender=user)
def createResume(sender, instance, **kwargs):
    resume=UserResume.objects.filter(user=instance)
    if not resume.exists():
        r=UserResume.objects.create(user=instance)
