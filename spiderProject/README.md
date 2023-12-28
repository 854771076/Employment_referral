[toc]

## 爬虫模块部署

### 1.环境

**硬件：**Linux or Windows

**软件：** MySQL，python3.8(requirements.txt)，Anaconda3,Redis

* **创建虚拟环境spider**

  ```
  conda create -n spider python==3.85
  ```
* **安装所需第三方库**
     ```
     pip install -r requirements.txt
     ```
* **安装MySQL，Redis数据库**
* **配置spider/tutorial/setting.py**
	```python
  # REDIS
	REDIS_HOST="127.0.0.1"
	REDIS_PORT=6379
	REDIS_PWD=''
	REDIS_DB='0'
	#MYSQL
	MYSQL_HOST = '10.8.16.83'
	MYSQL_PORT = 3306
	MYSQL_DBNAME = 'spider'
	MYSQL_USER = 'root'
	MYSQL_PASSWD = 'fiang123'
	```

### 2.Spiderweb运行

* **点击spder-start.bat**

* **scrapyd `127.0.0.1:6800`**

* **gerapy `127.0.0.1:8000`**
