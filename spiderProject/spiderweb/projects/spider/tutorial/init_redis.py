import  redis
from scrapy.utils.project import get_project_settings
settings = get_project_settings()
#初始化redis
def init_redis_zhilian(delete=False):
    db=settings.get('REDIS_DB')
    host=settings.get('REDIS_HOST')
    pool = redis.ConnectionPool(host=settings.get('REDIS_HOST'),port=settings.get('REDIS_PORT'),password=settings.get('REDIS_PWD'),db=db)   #实现一个连接池
    r = redis.Redis(connection_pool=pool)
    r.set('zhilian_city',0)
    r.set('zhilian_current_page',0)
    if  delete:
        for i in r.smembers('positionIds_zhilian'):
            r.srem('positionIds_zhilian', i)
    print('ok')
def init_redis_zhilian2(delete=False):
    db=settings.get('REDIS_DB')
    host=settings.get('REDIS_HOST')
    pool = redis.ConnectionPool(host=settings.get('REDIS_HOST'),port=settings.get('REDIS_PORT'),password=settings.get('REDIS_PWD'),db=db)   #实现一个连接池
    r = redis.Redis(connection_pool=pool)
    r.set('zhilian2_city',0)
    r.set('zhilian2_jobtype',0)
    r.set('zhilian2_current_page',1)
    if  delete:
        for i in r.smembers('positionIds_zhilian2'):
            r.srem('positionIds_zhilian2', i)
    print('ok')
if __name__ == '__main__':
    # init_redis_zhilian(1)
    
    init_redis_zhilian2(1)