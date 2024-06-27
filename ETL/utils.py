
import datetime, sys,time
from typing import *
import threading
import subprocess
from sys import stderr
from logging import getLogger, StreamHandler, Formatter, INFO, DEBUG, ERROR, FileHandler, WARNING,Logger,basicConfig

from pyspark.sql import SparkSession,DataFrame
from pyspark.sql import functions as F
from pyspark.sql.types import *
import pymysql
import pandas as pd
from datetime import datetime,date,timedelta
from copy import deepcopy
import concurrent.futures
import multiprocessing
import functools
import os
def get_thread_id():
    # 获取当前线程的 ID
    thread_id = threading.get_ident()
    return thread_id
def getHiveData(ssc:SparkSession,params: Mapping[str,str])->"DataFrame":
    '''
    使用spark读取hive数据
    params={
    "source_db"
    "source_table"
    }
    '''
    df = ssc.sql(f'select * from {params["source_db"]}.{params["source_tb"]} ')
    return df
def getMySQLData(ssc:SparkSession,params: Mapping[str,Union[str,int]],sync_date:bool=True)->"DataFrame":
    '''
    使用spark读取mysql数据
    params={
    "host"
    "port"
    "db"
    "table"
    "user"
    "password"
    }
    添加同步时间
    sync_date=True
    '''
    if sync_date:
        df = ssc.read.format('jdbc') \
            .option('url',
                    f"jdbc:mysql://{params.get('host')}:{params.get('port')}/{params.get('db')}?useSSL=false&useUnicode=true") \
            .option('dbtable', params.get('table')) \
            .option('user', params.get('user')) \
            .option('driver', 'com.mysql.jdbc.Driver') \
            .option('password', params.get('password')) \
            .load().withColumn('cdc_sync_date', F.current_timestamp())
    else:
        df=ssc.read.format('jdbc') \
            .option('url',
                    f"jdbc:mysql://{params.get('host')}:{params.get('port')}/{params.get('db')}?useSSL=false&useUnicode=true") \
            .option('table', params.get('table')) \
            .option('user', params.get('user')) \
            .option('driver', 'com.mysql.jdbc.Driver') \
            .option('password', params.get('password')) \
            .load()
    return df
def getLog(Name:Optional[str])->"Logger":
    '''
    获得日志对象
    
    '''
    
    logger = getLogger(f'log_{datetime.now()}')
    logger.setLevel(INFO)
    rf_handler = StreamHandler(stderr)  # 默认是sys.stderr
    rf_handler.setLevel(DEBUG)
    # f2_handler = FileHandler(Name+'.info')
    # f2_handler.setLevel(INFO)
    # f2_handler.setFormatter(Formatter(
    #     "%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))
    # f4_handler = FileHandler(Name+'.warn')
    # f4_handler.setLevel(WARNING)
    # f4_handler.setFormatter(Formatter(
    #     "%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))
    # f3_handler = FileHandler(Name+'.error')
    # f3_handler.setLevel(ERROR)
    # f3_handler.setFormatter(Formatter(
    #     "%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))
    logger.addHandler(rf_handler)
    # logger.addHandler(f2_handler)
    # logger.addHandler(f3_handler)
    # logger.addHandler(f4_handler)
    return logger
class MysqlDB:
    '''
    mysql操作类
    params={
    "host"
    "port"
    "db"
    "table"
    "user"
    "password"
    }
    '''
    def __init__(self, params:Mapping[str,Union[str,int]])->None:
        self.params=params
    def getconn(self)->"pymysql.connections.Connection":
        try:
            conn = pymysql.connect(**self.params)
        except pymysql.err.OperationalError:
            # 如果没有数据库则创建数据库
            db = self.params.pop('db')
            conn = pymysql.connect(**self.params)
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE {db}")
            cursor.close()
            conn.close()
            self.params['db'] = db
            conn = pymysql.connect(**self.params)
        return conn
    @staticmethod
    def is_alive(params:Mapping[str,Union[str,int]])->bool:
        '''
        判断mysql连接是否存活

        '''
        try:
            # 执行一个简单的查询
            conn = pymysql.connect(**params)
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1")
            # 检查查询结果
            result = cursor.fetchone()
            if result[0] == 1:
                return True
            else:
                return False
        except:
            return False
    @classmethod
    def create_table(self,conn, table_name: str, columns: list, types: list)->bool:
        '''
        根据表名、字段、字段类型建表
        '''
        columns_str = ''
        id_str = '`id` INT AUTO_INCREMENT PRIMARY KEY,\n'
        for i, j in enumerate(columns):
            if j == 'id':
                id_str = ''
            columns_str += f'`{j}` {types[i]},\n'
        columns_str = columns_str.strip("\n").strip(",")
        sql = f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            {id_str}
            {columns_str}
        )ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
        '''
        try:
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            raise ValueError(f'创建表{table_name}失败-error{e}-sql:{sql}')
    def get_types(self, data: list)->List:
        '''
        根据数据的类型转换为mysql中字段类型
        '''
        # 获取一行数据
        data = data[0]
        def getType(column):
            if isinstance(column, str):
                return 'TEXT'
            elif isinstance(column, datetime):
                return 'datetime'
            elif isinstance(column, int):
                return 'int'
            elif isinstance(column, float):
                return 'double'
            elif isinstance(column, bool):
                return 'bool'
            elif isinstance(column, None):
                return 'String'
            else:
                raise ValueError(f'不支持字段类型:{type(column)}')
        types = []
        for i in data:
            types.append(getType(i))
        return types
    @classmethod
    def check_table_exists(self,conn, table_name:str)->bool:
        '''
        查询表是否存在
        '''
        try:
            # 创建游标对象
            cursor = conn.cursor()
            # 执行SHOW TABLES查询
            cursor.execute("SHOW TABLES")
            # 获取返回的所有表名
            tables = cursor.fetchall()
            # 检查目标表是否在返回的结果中存在
            if (table_name,) in tables:
                return True
            else:
                return False
        except:
            return False
    def save(self, data: list, table_name: str, method: str = 'append')->"pd.DataFrame":
        '''
        简单便捷的保存方法
        自动建库建表
        支持append、replace模式
        '''
        assert len(data) > 0, 'data不能为空'
        df = pd.DataFrame(data)
        conn=self.getconn()
        cur = conn.cursor()
        data = df.values.tolist()
        columns = df.columns.tolist()
        columns_str = ','.join([f'`{i}`' for i in columns])
        s_str = ','.join(['%s' for i in range(len(columns))])
        sql = f'insert into {table_name}({columns_str}) values ({s_str})'
        if self.check_table_exists(conn,table_name):
            if method == 'append':
                pass
            else:
                cur.execute(f'drop table {table_name}')
                conn.commit()
                types = self.get_types(data)
                self.create_table(conn,table_name, columns, types)
        else:
            types = self.get_types(data)
            self.create_table(conn,table_name, columns, types)
        try:
            cur.executemany(sql, data)
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise ValueError(f'保存失败-error:{e}-sql:{sql}')
def saveMySQLData(df:"DataFrame", params:Mapping[str,Union[str,int]],method:Optional[str]='append'):
    '''
    使用spark读取mysql数据
    params={
    "host"
    "port"
    "db"
    "table"
    "user"
    "password"
    }

    method:
    append overwrite
    '''
    df.write.format('jdbc') \
        .mode(method) \
        .option('url',
                f"jdbc:mysql://{params.get('host')}:{params.get('port')}/{params.get('db')}?useSSL=false&useUnicode=true") \
        .option('dbtable', params.get('table')) \
        .option('user', params.get('user')) \
        .option('driver', 'com.mysql.jdbc.Driver') \
        .option('password', params.get('password')) \
        .save()
def getHiveDataOnSQL(ssc:SparkSession,sql:Optional[str],partition_column:Optional[str])->"DataFrame":
    '''
    使用spark读取hive数据
    '''
    df = ssc.sql(sql)
    if partition_column:
        df =df.drop(partition_column)
    return df
