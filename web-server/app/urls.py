from django.contrib import admin
from django.urls import path,include,re_path
from rest_framework_simplejwt.views import TokenRefreshView
from app.views import *
urlpatterns = [
    path('', VueAppView.as_view(), name='vue_app'),
    path('login', VueAppView.as_view()),
    path('recommend', VueAppView.as_view()),
    path('job', VueAppView.as_view()),
    path('company', VueAppView.as_view()),
    path('login', VueAppView.as_view()),
    path('star', VueAppView.as_view()),
    path('history', VueAppView.as_view()),
    path('mine', VueAppView.as_view()),
    path('bigview', VueAppView.as_view()),
    path('resume', VueAppView.as_view()),
    re_path('job/detail/*', VueAppView.as_view()),
    re_path('company/detail/*', VueAppView.as_view()),

    
    

]
'''
        { path: '/', name:'首页',component: Home },
    { path: '/recommend', name:'推荐',component: Home },
    { path: '/job', name:'职位',component: Home },
    { path: '/company', name:'公司',component: Home },
    { path: '/login', name:'登录',component: Login },
    { path: '/resume', name:'简历',component: Resume },
    { path: '/job/detail/:number', name:'职位详细',component: JobDetail  },
    { path: '/company/detail/:number', name:'企业详细',component:CompanyDetail },
    '''