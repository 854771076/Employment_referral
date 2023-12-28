

import datetime, sys, threading,time
from sys import stderr
from logging import getLogger, StreamHandler, Formatter, INFO, DEBUG, ERROR, FileHandler, WARNING

'''
spark.sql.shuffle.partitions Local模式下调小，一般为CPU核心数2-10倍
'''
import findspark

findspark.init()
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import *

# hdfs:///user/cdh/jars/mysql-connector-java-5.1.49.jar为传入的mysql-connector包
spark = SparkSession.builder \
    .appName("mysql_to_ods加工") \
    .master('yarn') \
    .config('spark.sql.shuffle.partitions', '1000') \
    .config('spark.jars', 'hdfs:///user/cdh/jars/mysql-connector-java-5.1.49.jar') \
    .getOrCreate()
# 配置参数
class settings:

    # 日志信息存储的mysql
    MYSQL_CONNECT = {
        'host': '10.8.16.83',
        'port': 3306,
        'user': 'root',
        'password': 'fiang123',
        'charset': 'utf8',
        'db': 'logs'
    }
    MYSQL_PARAMS = {
        'host': '10.8.16.83',
        'port': 3306,
        'user': 'root',
        'password': 'fiang123',
    }

    TABLES = [
        {"name": "智联招聘岗位信息", "db": "spider", "table": "jobs_2023_10_13", "db_num": 0, "t_num": 0,
         'hive_db': 'ods_jobfree', 'hive_table': 'ods_jobfree_db_spider_t_jobs', "update_column": "local_row_update_time"},
        {"name": "智联招聘岗位信息", "db": "spider", "table": "jobs_2023_10_16", "db_num": 0, "t_num": 0,
         'hive_db': 'ods_jobfree', 'hive_table': 'ods_jobfree_db_spider_t_jobs', "update_column": "local_row_update_time"},
        {"name": "智联招聘岗位信息", "db": "spider", "table": "jobs_2023_10_17", "db_num": 0, "t_num": 0,
         'hive_db': 'ods_jobfree', 'hive_table': 'ods_jobfree_db_spider_t_jobs', "update_column": "local_row_update_time"},
        {"name": "智联招聘岗位信息", "db": "spider", "table": "jobs_2023_10_18", "db_num": 0, "t_num": 0,
         'hive_db': 'ods_jobfree', 'hive_table': 'ods_jobfree_db_spider_t_jobs', "update_column": "local_row_update_time"},
        {"name": "智联招聘岗位信息", "db": "spider", "table": "jobs_2023_10_20", "db_num": 0, "t_num": 0,
         'hive_db': 'ods_jobfree', 'hive_table': 'ods_jobfree_db_spider_t_jobs', "update_column": "local_row_update_time"},
        {"name": "智联招聘岗位信息", "db": "spider", "table": "jobs_2023_10_21", "db_num": 0, "t_num": 0,
         'hive_db': 'ods_jobfree', 'hive_table': 'ods_jobfree_db_spider_t_jobs', "update_column": "local_row_update_time"},
        {"name": "智联招聘岗位信息", "db": "spider", "table": "jobs_2023_10_22", "db_num": 0, "t_num": 0,
         'hive_db': 'ods_jobfree', 'hive_table': 'ods_jobfree_db_spider_t_jobs', "update_column": "local_row_update_time"},
        {"name": "用户简历信息", "db": "jobfree", "table": "resume", "db_num": 0, "t_num": 0,
         'hive_db': 'ods_jobfree', 'hive_table': 'ods_jobfree_db_jobfree_t_resume', "update_column": "last_update"},
        {"name": "用户点击浏览职位", "db": "jobfree", "table": "clickjobs", "db_num": 0, "t_num": 0,
         'hive_db': 'ods_jobfree', 'hive_table': 'ods_jobfree_db_jobfree_t_clickjobs', "update_column": "last_update"},
        {"name": "用户收藏职位", "db": "jobfree", "table": "starjobs", "db_num": 0, "t_num": 0,
         'hive_db': 'ods_jobfree', 'hive_table': 'ods_jobfree_db_jobfree_t_starjobs', "update_column": "create_time"},
    ]

    #mysql2hive--0 还是hive2mysql--1
    outType=0
    log_tb_name=f"{'mysql2hive' if outType==0 else 'hive2mysql'}_spark"
    log_name = f'{log_tb_name}.log'
    error_log_name = f'{log_tb_name}_spark.error.log'
    TYPE = 'all'
    # 日志结构
    log_data = {
        'host': MYSQL_PARAMS.get('host'),
        'port': MYSQL_PARAMS.get('port'),
        'db_name': '',
        'tb_name': '',
        'status': False,
        'hive_db_name': '',
        'hive_tb_name': '',
        'outType':outType,
        'msg': '',
        'num': 0,
        'executed_way': TYPE,
        'local_row_update_time_start': '',
        'local_row_update_time_end': '',
        'partition_date':'',
        'exec_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    #是否删除已有分区
    is_del=False
    
def getHiveData(table: dict):
    '''
    使用spark读取hive数据
    '''
    df = spark.sql(f'select * from {table["hive_db"]}.{table["hive_table"]} ')
    return df
def getMySQLData(params: dict, table: dict):
    '''
    使用spark读取mysql数据
    '''
    df = spark.read.format('jdbc') \
        .option('url',
                f"jdbc:mysql://{params.get('host')}:{params.get('port')}/{table.get('db')}?useSSL=false&useUnicode=true") \
        .option('dbtable', table.get('table')) \
        .option('user', params.get('user')) \
        .option('driver', 'com.mysql.jdbc.Driver') \
        .option('password', params.get('password')) \
        .load().withColumn('cdc_sync_date', F.current_timestamp())
    return df

# 日志
def getLog():
    '''
    获得日志对象
    '''
    logger = getLogger(f'log_{datetime.datetime.now()}')
    logger.setLevel(INFO)
    rf_handler = StreamHandler(stderr)  # 默认是sys.stderr
    rf_handler.setLevel(DEBUG)
    f2_handler = FileHandler(settings.log_name)
    f2_handler.setLevel(INFO)
    f2_handler.setFormatter(Formatter(
        "%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))
    f3_handler = FileHandler(settings.error_log_name)
    f3_handler.setLevel(ERROR)
    f3_handler.setFormatter(Formatter(
        "%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))
    logger.addHandler(rf_handler)
    logger.addHandler(f2_handler)
    logger.addHandler(f3_handler)
    return logger


class MysqlDB:
    '''
    mysql操作类
    '''

    def __init__(self, params):
        self.params=params
    
    def getconn(self):
        import pymysql
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
    def is_alive(params):
        '''
        判断mysql连接是否存活
        '''
        import pymysql
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
    def create_table(self,conn, table_name: str, columns: list, types: list):
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

    def get_types(self, data: list):
        '''
        根据数据的类型转换为mysql中字段类型
        '''
        from datetime import datetime
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
            else:
                raise ValueError(f'不支持字段类型:{type(column)}')

        types = []
        for i in data:
            types.append(getType(i))
        return types
    @classmethod
    def check_table_exists(self,conn, table_name):
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

    def save(self, data: list, table_name: str, method: str = 'append'):
        '''
        简单便捷的保存方法
        自动建库建表
        支持append、replace模式
        '''
        import pandas as pd
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


class myThread(threading.Thread):
    def __init__(self, name, log_data, table, Type):
        super().__init__()
        self.name = name
        self.log_data = log_data.copy()
        self.table = table.copy()
        self.Type = Type

    def run(self):
        
        if settings.outType==0:
            run_res = mysql_to_hive(self.name, self.log_data, self.table, self.Type)
        else:
            run_res = hive_to_mysql(self.name, self.log_data, self.table, self.Type)


def hive_to_mysql(name, log_data: dict, table: dict, Type):
    '''
    调用spark将mysql数据导入hive，并记录日志
    '''
    logger.info(f"Thread {table['hive_db']}.{table['hive_table']}->{table['db']}.{table['table']}执行开始")
    params = settings.MYSQL_PARAMS.copy()
    try:
        log_data['db_name'] = table.get('db')
        log_data['tb_name'] = table.get('table')
        df = getHiveData(table)
        
        # 导入数据到mysql
        if TYPE == 'all':

            df = df.where(f"{table['update_column']}<'{today_time.strftime('%Y-%m-%d 23:59:59')}'")

        elif TYPE == 'update':
            df = df.where(
                f"{table['update_column']} between '{today_time.strftime('%Y-%m-%d 00:00:00')}' and '{today_time.strftime('%Y-%m-%d 23:59:59')}'")

        elif TYPE == 'other':
            df = df.where(f"{table['update_column']} between '{start_time}' and '{end_time}'")
        # 查询为空
        if df.rdd.isEmpty():
            log_data['status'] = True
            log_data['num'] = 0
            logger.info(f"表{table['hive_db']}.{table['hive_table']}无更新---num:0")
            log_data['msg'] = f"表{table['hive_db']}.{table['hive_table']}无更新"
            return
        num = df.count()
        df.write.format('jdbc') \
        .mode('append') \
        .option('url',
                f"jdbc:mysql://{params.get('host')}:{params.get('port')}/{table.get('db')}?useSSL=false&useUnicode=true") \
        .option('dbtable', table.get('table')) \
        .option('user', params.get('user')) \
        .option('driver', 'com.mysql.jdbc.Driver') \
        .option('password', params.get('password')) \
        .save()

        logger.info(f"Thread {table['hive_db']}.{table['hive_table']}->{table['db']}.{table['table']}执行成功---num:{num}")
        log_data['status'] = True
        log_data['num'] = num
        log_data['msg'] = f"导入{table['hive_db']}.{table['hive_table']}数据到{table['db']}.{table['table']}mysql表成功"
    except Exception as e:
        logger.error(f"{table['db']}.{table['table']}->{table['hive_db']}.{table['hive_table']}执行失败----error:{e}")
        log_data['msg'] = f"导入表{table['db']}.{table['table']}失败----error:{e}"
    finally:
        Log_db.save([log_data],settings.log_tb_name, 'append')
def mysql_to_hive(name, log_data: dict, table: dict, Type):
    '''
    调用spark将mysql数据导入hive，并记录日志
    '''
    logger.info(f"Thread {table['db']}.{table['table']}->{table['hive_db']}.{table['hive_table']}执行开始")
    params = settings.MYSQL_PARAMS.copy()
    try:
        log_data['db_name'] = table.get('db')
        log_data['tb_name'] = table.get('table')
        df = getMySQLData(params, table)
        # 删除partition_date分区已有数据
        try:
            if settings.is_del:
                spark.sql(
                    f'ALTER TABLE {table["hive_db"]}.{table["hive_table"]} DROP PARTITION (partition_date="{partition_date}")')
        except:
            pass
        # 导入数据到hive
        if TYPE == 'all':

            df = df.where(f"{table['update_column']}<'{today_time.strftime('%Y-%m-%d 23:59:59')}'")

        elif TYPE == 'update':
            df = df.where(
                f"{table['update_column']} between '{today_time.strftime('%Y-%m-%d 00:00:00')}' and '{today_time.strftime('%Y-%m-%d 23:59:59')}'")

        elif TYPE == 'other':
            df = df.where(f"{table['update_column']} between '{start_time}' and '{end_time}'")
        # 查询为空
        if df.rdd.isEmpty():
            log_data['status'] = True
            log_data['num'] = 0
            logger.info(f"表{table['db']}.{table['table']}无更新---num:0")
            log_data['msg'] = f"表{table['db']}.{table['table']}无更新"
            return
        num = df.count()
        df.createOrReplaceTempView(f"mysql_to_hive_{name}")
        spark.sql(
            f"INSERT INTO {table['hive_db']}.{table['hive_table']} PARTITION(partition_date={partition_date}) SELECT * FROM mysql_to_hive_{name}")

        logger.info(f"Thread {table['db']}.{table['table']}->{table['hive_db']}.{table['hive_table']}执行成功---num:{num}")
        log_data['status'] = True
        log_data['num'] = num
        log_data['msg'] = f"导入{table['db']}.{table['table']}数据到hive表{table['hive_db']}.{table['hive_table']}成功"
    except Exception as e:
        logger.error(f"{table['db']}.{table['table']}->{table['hive_db']}.{table['hive_table']}执行失败----error:{e}")
        log_data['msg'] = f"导入表{table['db']}.{table['table']}失败----error:{e}"
    finally:
        Log_db.save([log_data], settings.log_tb_name, 'append')


def insertData(table: dict):
    '''
    导入
    '''
    table = table.copy()
    log_data = settings.log_data.copy()
    log_data['hive_db_name'] = table.get('hive_db')
    log_data['hive_tb_name'] = table.get('hive_table')
    log_data['exec_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 创建多个线程
    threads = []
    # 单库单表
    if table['db_num'] == 0 and table['t_num'] == 0:
        t = myThread(f"{table['db']}_{table['table']}", log_data, table, TYPE)
        threads.append(t)
        t.start()
    ##单库多表
    elif table['db_num'] == 0 and table['t_num'] > 0:
        '''
        程序自动添加表下标并且依次遍历分表
        '''

        for i in range(table['t_num'] + 1):
            ##处理表名
            new_tb = table['table'].split('_')
            if len(new_tb) > 2:
                new_tb.pop()
                table['table'] = '_'.join(new_tb) + f'_{i}'
            else:
                table['table'] = table['table'] + f'_{i}'
            t = myThread(f"{table['db']}_{table['table']}", log_data, table, TYPE)
            threads.append(t)
            t.start()
    #     ##多库多表
    elif table['db_num'] > 0 and table['t_num'] > 0:
        '''
        程序自动添加库和表下标并且依次遍历分表
        '''
        for i in range(table['db_num'] + 1):
            ##处理库名
            new_db = table['db'].split('_')
            if len(new_db) > 2:
                new_db.pop()
                table['db'] = '_'.join(new_db) + f'_{i}'

            else:
                table['db'] = table['db'] + f'_{i}'
            for j in range(table['t_num'] + 1):
                ##处理表名
                new_tb = table['table'].split('_')
                if len(new_tb) > 2:
                    new_tb.pop()
                    table['table'] = '_'.join(new_tb) + f'_{j}'
                else:
                    table['table'] = table['table'] + f'_{j}'

                t = myThread(f"{table['db']}_{table['table']}", log_data, table, TYPE)
                threads.append(t)
                t.start()
    ##不能识别类型
    else:
        raise ValueError('db_num or t_num ValueError')
    for t in threads:
        t.join()


if __name__ == '__main__':
    logger = getLog()
    Log_db = MysqlDB(settings.MYSQL_CONNECT)
    today_time = datetime.date.today()
#     yesterday_time = today_time + datetime.timedelta(-1)
    partition_date = today_time.strftime("%Y%m%d")
    try:
        TYPE = sys.argv[1]
        if TYPE not in ['all','update','other']:
            TYPE = settings.TYPE
    except:
        TYPE = settings.TYPE
    tables = settings.TABLES
    logger.info(f'导入开始--type:{TYPE}')
    start=time.time()
    ##1 全量  截止运行时间零点
    if settings.outType==0:
        logger.info('mysql_to_hive start')
    else:
        logger.info('hive_to_mysql start')
    if TYPE == 'all':
        settings.log_data['executed_way'] = TYPE
        settings.log_data['partition_date'] = partition_date
        settings.log_data['local_row_update_time_start'] = today_time.strftime("%Y-%m-%d %H:%M:%S")
        settings.log_data['local_row_update_time_end'] = today_time.strftime("%Y-%m-%d %H:%M:%S")

    elif TYPE == 'update':
        settings.log_data['executed_way'] = TYPE
        settings.log_data['partition_date'] = partition_date
        settings.log_data['local_row_update_time_start'] = today_time.strftime("%Y-%m-%d %H:%M:%S")
        settings.log_data['local_row_update_time_end'] = today_time.strftime("%Y-%m-%d %H:%M:%S")

    ##3 指定时间段 追加放入昨天分区/指定分区里
    elif TYPE == 'other':
        start_time = sys.argv[2]
        end_time = sys.argv[3]
        # start_time = "2022-08-11 00:00:00"
        # end_time   = "2022-08-12 00:00:00"
        partition_date = sys.argv[4] if len(sys.argv) > 4 else partition_date
        where_str = "{} between '%s' and '%s' " % (start_time, end_time)
        is_merge_small_file = True
        settings.log_data['partition_date'] = partition_date
        settings.log_data['executed_way'] = TYPE
        settings.log_data['local_row_update_time_start'] = start_time
        settings.log_data['local_row_update_time_end'] = end_time
    else:
        raise ValueError(f'不能识别类型{TYPE}')
    for table in tables:
        insertData(table)
    end=time.time()
    
    logger.info(f'导入完成---总耗时{(end-start)}秒')