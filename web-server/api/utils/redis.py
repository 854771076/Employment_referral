from django.conf import settings
import os,redis
def getRedisConnection():
	redis_host = settings.REDIS_HOST
	redis_port = settings.REDIS_PORT
	psw=settings.REDIS_PSW
	#初始化redis
	pool= redis.ConnectionPool(host=redis_host,port=redis_port,decode_responses=True,password=psw,db=settings.REDIS_DB)
	r=redis.Redis(connection_pool=pool)
	return r