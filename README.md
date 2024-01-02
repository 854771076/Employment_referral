# JobFree

### 一、项目部署

### 1.1 docker-compose部署(暂时不能用，有懂的可以帮忙完善)

```sh
# docker build
cd 项目目录/
docker build -f ./docker_env/django/DockerfileBuild -t django_docker_img:v1 .
# 镜像保存
docker save -o django_docker_img.tar django_docker_img:v1

# docker build
# 进项目目录
cd project/
docker build -f ./docker_env/web/DockerfileBuild -t vue_web_img:v1 .
# 镜像保存
docker save -o vue_web_img.tar vue_web_img:v1
# 加载离线镜像
docker load -i django_docker_img.tar
docker load -i vue_web_img.tar
 
 
# docker-compose 创建并启动相应服务
cd 项目目录/
docker-compose up -d
```

### 1.2 环境初始化

#### 1.2.1 快捷脚本(Windows)

* 下载Anaconda
* 运行env-init.bat
* 注意控制台信息，需要输入两个y

#### 1.2.2 正常流程

* 下载Anaconda

* 创建虚拟环境

  * 爬虫环境

  ```cmd
  conda create -n jobfreeSpider python=3.8
  
  pip install -r .\spiderProject\requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
  ```

  * Web环境

  ```cmd
  conda create -n jobfree python=3.8
  
  pip install -r .\web-server\requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
  ```

* 下载MySQL和Redis数据库

### 1.3 项目启动

#### 1.3.1 爬虫程序

##### windows一键启动

> 双击spder-start.bat

##### 正常启动

* 切换至 jobfreeSpider环境

  ```cmd
  conda activate jobfreeSpider
  ```

* 启动scrapyd进程

  ```cmd
  scrapyd
  # 控制台输入
  # windows输入 scrapyd 后收后台挂起，新建cmd执行后续
  # Linux输入nohup scrapyd > scrapyd.log & + ctrl+D挂起
  ```

* 启动Gerapy

  ```cmd
  gerapy runserver 0.0.0.0:5000
  # 控制台输入
  # windows输入 gerapy runserver 0.0.0.0:5000 后收后台挂起
  # Linux输入nohup gerapy runserver 0.0.0.0:5000 > gerapy.log & + ctrl+D挂起
  ```

* 浏览器打开`http://127.0.0.1`进入Gerapy，用户名密码`admin/admin`

* 点击项目管理-编辑

  ![1](img\1.png)

* 找到settings.py,修改redis和mysql为自己的配置，不用建表，自动建

  ![2](img\2.png)

* 修改完不用保存（自动保存），点击项目管理-部署

  ![](img\3.png)

* 点击重新打包后，再点击部署即可（如果报错99%是你的数据库配置有问题，因为部署时会执行检查代码，连接不上就报错）

  ![4](img\4.png)

* 如果部署失败，查看scrapyd进程/日志

##### 

#### 1.3.2 Web程序

##### 配置settings.py

```python
# web-server\DRF\settings.py
# SMTP邮箱设置,怎么申请请自行网上学习
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = ''  # 邮箱SMTP服务器地址
EMAIL_HOST_USER = ''  # 邮箱用户名
EMAIL_HOST_PASSWORD = ''  # 邮箱密码
# EMAIL_USE_TLS = True  # 使用TLS加密
DEFAULT_FROM_EMAIL = ''  # 默认发件人邮箱
#redis
REDIS_HOST='127.0.0.1'
REDIS_PORT=6379
REDIS_PSW=''
REDIS_DB=1
#MySQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'jobfree',  
        'USER': 'root',  
        'PASSWORD': 'root',  
        'HOST': '127.0.0.1',
        'PORT': 3306,
        'OPTIONS': {'charset': 'utf8mb4'},
    },

}
```

##### 迁移数据库

```cmd
conda activate jobfree
cd web-server
python manage.py migrate
```

##### 导入测试数据

> ETL\test_data.sql，然后完成ETL模块再进行下一步运行

##### windows一键启动

> 双击web-start.bat

##### 正常启动

```cmd
cd web-server
conda activate jobfree
python manage.py runserver
```

#### 1.3.3 ETL模块

##### 环境搭建

> 有集群则跳过

[Windows下使用hadoop+hive+sparkSQL-CSDN博客](https://blog.csdn.net/qq_41631913/article/details/134804263)

##### 初始化hive数据库

> ETL\init.sql

##### 安装python库

```cmd
pip install findspark
```

##### 执行ETL脚本

> ETL\xxx目录下的py文件

##### 模型训练

> model\ALS.py
