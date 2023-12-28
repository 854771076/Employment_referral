# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
# from scrapy.conf import settings
from scrapy.utils.project import get_project_settings
from datetime import datetime
settings = get_project_settings()
class MysqlDB():
    def __init__(self,user=settings.get('MYSQL_USER'),password=settings.get('MYSQL_PASSWD'),host=settings.get('MYSQL_HOST'),port=settings.get('MYSQL_PORT'),charset='utf8',db=settings.get('MYSQL_DBNAME'),**params):
        '''
        user='spider',password='Rb7snZyNsf3mS6GR',host='124.223.62.222',port=3306,charset='utf8',db='spider'
        '''
        from sqlalchemy import create_engine
        self.conn=create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{db}?charset={charset}',echo=False)
    def save(self,val,table:str,columns=None,method:str='append'):
        '''
        method append,replace
        '''
        import pandas as pd
        if columns!=None:
            df=pd.DataFrame(val,columns=columns)
        else:
            df=pd.DataFrame(val)
        
        df.to_sql(table,self.conn,if_exists=method,index=False)
        return df
    def read2df(self,table:str):
        import pandas as pd
        df=pd.read_sql_table(con=self.conn,table_name=table)
        return df 
    def showtables(self):
        return self.conn.table_names()
    def getconn(self):
        return self.conn
class ZhilianPipeline(object):

    def open_spider(self,spider):
        # 建立连接
        self.conn = MysqlDB()
 
    def process_item(self,item,spider):
        #把多数据结构的字段转json
        try:
            item.pop('positionURL')
            try:
                item.pop('industryTags')
            except:
                pass
            item.pop('collected')
            item.pop('uuid')

            item.pop('selected')
            

        except Exception as e:
            spider.logger.error(e)
        # 获取当前日期和时间
        now = datetime.now()

        
        
        for k,v in item.items():
            if not isinstance(item[k],int) or  not isinstance(item[k],datetime):
                item[k]=json.dumps(v,ensure_ascii=False)
        item['local_row_update_time']=now
        try:
            self.conn.save((item,),'jobs')
        except Exception as e:
            spider.logger.warning(e)
    def close_spider(self,spider):
        pass
