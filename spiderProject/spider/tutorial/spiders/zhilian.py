import scrapy
from tutorial.items import TutorialItem
from scrapy.http import Request
from scrapy.spiders import CrawlSpider
# from scrapy.conf import settings
from scrapy.utils.project import get_project_settings
settings = get_project_settings()
import  json
import  time,os
from math import ceil
from ..items import *
from .getredis import *
from  tutorial.init_redis import *
#zhilian 爬虫
class TestSpider(scrapy.Spider):
    name = "zhilian"
    allowed_domains = ["m.zhaopin.com"]
    r=getRedisConnection()
    init=r.get('zhilian_init')
    if not init:
        init_redis_zhilian()
        r.set('zhilian_init','true')
    #地区码
    city_code=['530', '531', '532', '533', '534', '535', '536', '537', '538', '539', '540', '541', '542', '543', '544', '545', '546', '547', '548', '549', '550', '551', '552', '553', '554', '555', '556', '557', '558', '559', '560','562;561;563']
    current_page = int(r.get('zhilian_current_page'))
    city=int(r.get('zhilian_city'))
    if city>=30:
            r.set('zhilian_city',0)
            r.set('zhilian_current_page',0)
            city=0
    
    time=''
    start_urls = [
        f"https://xiaoyuan.zhaopin.com/api/sou?S_SOU_POSITION_SOURCE_TYPE=2&pageIndex={current_page }&S_SOU_POSITION_TYPE=2&S_SOU_WORK_CITY={city_code[city]}&S_SOU_REFRESH_DATE={time}&order=16&pageSize=90&_v=0.04618468&at=d76f0a24dcb044c98368beac70cfd2ee&rt=4afe00e73c0f4df390d3b89ba47188a7&x-zp-page-request-id=01509dc90ff040959ec1abe618c5583f-1659171749530-563316&x-zp-client-id=95f89d20-e65a-4a55-83e5-775013f626c9"
    ]
    custom_settings = {
        "ITEM_PIPELINES":{
            'tutorial.pipelines.ZhilianPipeline': 300,
        },

        "DEFAULT_REQUEST_HEADERS":{
            'Accept': 'application/json',
            'User-Agent':'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Mobile Safari/537.36',
        }
    }
    setkey = 'positionIds_zhilian'
    citylen=31
    
    def parse(self, response):
        try:
            self.logger.info(f'{self.city_code[self.city]}第{self.current_page}页开始爬取')
            items = json.loads(response.text).get('data').get('data')
            maxpage=ceil(items['count']/90)
            items = items['list']
            for index,item in enumerate(items) :
                if (self.r.sadd(self.setkey,item['number'])) == 1:
                    self.logger.info(str(item['number']))
                    yield item
                else:
                    self.logger.info('已有该数据！'+item['number'] )
            if (self.current_page==maxpage and self.city<self.citylen) or maxpage==1 or maxpage==0:
                    if self.city!=self.citylen:
                        self.city+=1
                        self.current_page=0
                        self.r.set('zhilian_city',self.city,1000*60*60*24)
                        self.r.set('zhilian_current_page',self.current_page,1000*60*60*24)
            if self.current_page<maxpage or maxpage==1:
                self.current_page+=1
                self.r.set('zhilian_current_page',self.current_page)
                yield Request(f'https://xiaoyuan.zhaopin.com/api/sou?S_SOU_POSITION_SOURCE_TYPE=2&pageIndex={self.current_page }&S_SOU_POSITION_TYPE=2&S_SOU_WORK_CITY={self.city_code[self.city]}&S_SOU_REFRESH_DATE={self.time}&order=16&pageSize=90&_v=0.04618468&at=d76f0a24dcb044c98368beac70cfd2ee&rt=4afe00e73c0f4df390d3b89ba47188a7&x-zp-page-request-id=01509dc90ff040959ec1abe618c5583f-1659171749530-563316&x-zp-client-id=95f89d20-e65a-4a55-83e5-775013f626c9',callback=self.parse,dont_filter=True)
        except Exception as e:
            self.logger.logger.warning(e)
            time.sleep(20)
            self.current_page=1
            self.city+1
            yield Request(f'https://xiaoyuan.zhaopin.com/api/sou?S_SOU_POSITION_SOURCE_TYPE=2&pageIndex={self.current_page }&S_SOU_POSITION_TYPE=2&S_SOU_WORK_CITY={self.city_code[self.city]}&S_SOU_REFRESH_DATE={self.time}&order=16&pageSize=90&_v=0.04618468&at=d76f0a24dcb044c98368beac70cfd2ee&rt=4afe00e73c0f4df390d3b89ba47188a7&x-zp-page-request-id=01509dc90ff040959ec1abe618c5583f-1659171749530-563316&x-zp-client-id=95f89d20-e65a-4a55-83e5-775013f626c9,callback=self.parse,dont_filter=True',callback=self.parse,dont_filter=True)