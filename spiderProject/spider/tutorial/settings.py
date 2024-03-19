# -*- coding: utf-8 -*-

BOT_NAME = 'tutorial'
PORXY_API='http://zltiqu.pyhttp.taolop.com/getip?count=1&neek=42670&type=2&yys=0&port=1&sb=&mr=1&sep=0&ts=1&time=2'
SPIDER_MODULES = ['tutorial.spiders']
NEWSPIDER_MODULE = 'tutorial.spiders'

LOG_LEVEL = 'INFO'
COOKIES_ENABLED=False
# Obey robots.txt rules
ROBOTSTXT_OBEY = False
DOWNLOAD_DELAY = 3
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'application/json',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'user-agent:':'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 Edg/103.0.5060.134',
    'Referer':' https://m.lagou.com/search.html',
    'X-Requested-With':"XMLHttpRequest",
    "cookie":"user_trace_token=20180725211521-aa09c44d3ab54bf2bde9654cc6c4ab35; _ga=GA1.3.881896906.1532524522; _ga=GA1.2.881896906.1532524522; _gid=GA1.2.726017449.1532524522; LGUID=20180725211522-c92c8f9d-900c-11e8-a44e-525400f775ce; index_location_city=%E4%B8%8A%E6%B5%B7; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1532362837,1532398323,1532418933,1532572655; JSESSIONID=ABAAABAAAFDABFGC547325A2971F2AA49C9A368C145B679; _gat=1; LGSID=20180726124253-5bcf406b-908e-11e8-9ee6-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fm.lagou.com%2Fjobs%2F4741044.html; PRE_LAND=https%3A%2F%2Fm.lagou.com%2Fsearch.html; X_HTTP_TOKEN=1f8ff879c39e0209e7efb23aad68da74; LG_LOGIN_USER_ID=52613e3ab983a93b76c62f27b7f9f49934626b1999bbab20; _putrc=51AF6FA824D5BE21; login=true; unick=%E7%94%B0%E9%9B%B7; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1532580490; LGRID=20180726124809-182de556-908f-11e8-a494-525400f775ce"
}

FEED_EXPORT_ENCODING = 'utf-8'
# COOKIES_ENABLED=False
DOWNLOADER_MIDDLEWARES = {
  #'tutorial.middlewares.ProxyMiddleware': 299,
}
# REDIS
REDIS_HOST="127.0.0.1"
REDIS_PORT=6379
REDIS_PWD=''
REDIS_DB=3
#MYSQL
MYSQL_HOST = '127.0.0.1'
MYSQL_PORT = 3306
MYSQL_DBNAME = 'spider'
MYSQL_USER = 'root'
MYSQL_PASSWD = 'fiang123'
