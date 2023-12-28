import  random,requests,redis
from scrapy.utils.project import get_project_settings
settings = get_project_settings()
def getRedisConnection():
    redis_host = settings.get('REDIS_HOST')
    redis_port = settings.get('REDIS_PORT')
    psw=settings.get('REDIS_PWD')
    db=settings.get('REDIS_DB')
        #初始化redis
    pool= redis.ConnectionPool(host=redis_host,port=redis_port,decode_responses=True,password=psw,db=db)
    r=redis.Redis(connection_pool=pool)
    return r