from .utils import *
import findspark


class SparkMySQLHiveETL:
    '''
    MYSQL_PARAMS:MySQL连接配置
    params={
    "host"
    "port"
    "db"
    "table"
    "user"
    "password"
    }
    
    TYPE:[all update other]
    导数模式
    全量 增量 自定义

    DB_LOG=True
    数据库日志(MySQL)

    DB_LOG_PARAMS:MySQL连接配置
    params={
    "host"
    "port"
    "db"
    "table"
    "user"
    "password"
    }

    outType
    mysql2hive--1 还是hive2mysql--2 hive2hive--3

    log_data
    日志格式

    Task
    任务列表

    maxWorkers
    线程数

    maxProcess
    进程数
    '''

    def __init__(self,
                 appName: Optional[str] = 'ods',
                 master: Optional[str] = 'local[*]',
                 Task: Optional[Sequence[Mapping[str, Any]]] = None,
                 MYSQL_PARAMS: Mapping[str, Union[str, int]] = None,
                 TYPE: Optional[str] = "all",
                 DB_LOG: bool = True,
                 DB_LOG_PARAMS: Mapping[str, Union[str, int]] = None,
                 start_time: Optional[datetime] = None,
                 end_time: Optional[datetime] = None,
                 outType: Optional[int] = 1,
                 maxWorkers: Optional[int] = 1,
                 maxProcess: Optional[int] = 1,
                 ):
        if outType in (1, 2):
            assert MYSQL_PARAMS != None, "MYSQL_PARAMS is None"
        assert DB_LOG and DB_LOG_PARAMS != None, "DB_LOG_PARAMS is None"
        assert TYPE != 'other' or (start_time and end_time), "other method  (start_time and end_time) not allow is None"
        assert TYPE in ('all', 'update', 'other'), "TYPE not in ('all','update','other')"

        self.Task = Task
        self.maxProcess = maxProcess
        self.appName = appName
        self.maxWorkers = maxWorkers
        self.master = master
        self.MYSQL_PARAMS = MYSQL_PARAMS
        self.TYPE = TYPE
        self.today_time = date.today()
        self.yesterday_time = self.today_time + timedelta(-1)
        self.start_time = start_time
        self.end_time = end_time
        self.DB_LOG = DB_LOG
        self.DB_LOG_PARAMS = DB_LOG_PARAMS
        if self.DB_LOG:
            self.DB_LOG_CONN = MysqlDB(self.DB_LOG_PARAMS)
        self.outType = outType
        self.partition_date = self.yesterday_time.strftime("%Y%m%d")

        if outType in (1, 2):
            self.log_data = {
                'host': self.MYSQL_PARAMS.get('host'),
                'port': self.MYSQL_PARAMS.get('port'),
                'source_db': '',
                'source_tb': '',
                'status': False,
                'sink_db': '',
                'sink_tb': '',
                'outType': self.outType,
                'msg': '',
                'num': 0,
                'SQL': None,
                'executed_way': TYPE,
                'local_row_update_time_start': self.today_time.strftime("%Y-%m-%d %H:%M:%S"),
                'local_row_update_time_end': '',
                'partition_date': self.partition_date,
                'exec_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        else:
            self.log_data = {
                'host': '',
                'port': '',
                'source_db': '',
                'source_tb': '',
                'status': False,
                'sink_db': '',
                'sink_tb': '',
                'outType': self.outType,
                'msg': '',
                'num': 0,
                'SQL': None,
                'executed_way': TYPE,
                'local_row_update_time_start': self.today_time.strftime("%Y-%m-%d %H:%M:%S"),
                'local_row_update_time_end': '',
                'partition_date': self.partition_date,
                'exec_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

    def hive_to_mysql(self, spark, logger, table: Mapping[str, Any]) -> None:
        '''
        调用spark将mysql数据导入hive，并记录日志

        table={'name': 'db1',
        'source_tb': 'db_code',
        'source_tb': 't_admin_division_code',
        'sink_db': 'ods_syx_test',
        'update_column': 'local_row_update_time',
        'sink_tb': 'ods_q_db_code_t_admin_division_code'
        'is_del':True #是否覆盖
        }
        '''
        name = get_thread_id()
        logger.info(
            f"Thread-{name}:{table['source_db']}.{table['source_tb']}->{table['sink_db']}.{table['sink_tb']}执行开始")
        mysql_params = deepcopy(self.MYSQL_PARAMS)
        mysql_params['db'] = table.get('sink_db')
        mysql_params['table'] = table.get('sink_tb')
        # 日志
        log_data = deepcopy(self.log_data)
        log_data['source_db'] = table.get('source_db')
        log_data['source_tb'] = table.get('source_tb')
        log_data['sink_db'] = table.get('sink_db')
        log_data['sink_tb'] = table.get('sink_tb')
        try:
            df = getHiveData(spark, table)
            # 导入数据到mysql
            if table.get('update_column', '') != '':
                if self.TYPE == 'all':
                    df = df.where(f"{table['update_column']}<'{self.today_time.strftime('%Y-%m-%d 00:00:00')}'")

                elif self.TYPE == 'update':
                    df = df.where(
                        f"{table['update_column']} between '{self.yesterday_time.strftime('%Y-%m-%d 00:00:00')}' and '{self.today_time.strftime('%Y-%m-%d 00:00:00')}'")

                elif self.TYPE == 'other':
                    df = df.where(f"{table['update_column']} between '{self.start_time}' and '{self.end_time}'")

            # 查询为空
            if df.rdd.isEmpty():
                log_data['status'] = True
                log_data['num'] = 0
                logger.info(f"表{table['source_db']}.{table['source_tb']}无更新---num:0")
                log_data['msg'] = f"表{table['source_db']}.{table['source_tb']}无更新"
                return
            num = df.count()
            df=df.drop('cdc_sync_date')
            if table.get('is_del'):
                saveMySQLData(df, mysql_params, 'overwrite')
            else:
                saveMySQLData(df, mysql_params, 'append')
            logger.info(
                f"Thread-{name}:{table['source_db']}.{table['source_tb']}->{table['sink_db']}.{table['sink_tb']}执行成功---num:{num}")
            log_data['status'] = True
            log_data['num'] = num
            log_data[
                'msg'] = f"导入{table['source_db']}.{table['source_tb']}数据到{table['sink_db']}.{table['sink_tb']},mysql表成功"
        except Exception as e:
            logger.error(
                f"{table['source_db']}.{table['source_tb']}->{table['sink_db']}.{table['sink_tb']}执行失败----error:{e}")
            log_data[
                'msg'] = f"导入表{table['source_db']}.{table['source_tb']}->{table['sink_db']}.{table['sink_tb']}失败----error:{e}"
        finally:
            log_data['local_row_update_time_end'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if self.DB_LOG:
                self.DB_LOG_CONN.save([log_data], self.appName, 'append')

    def mysql_to_hive(self, spark, logger, table: Mapping[str, Any]) -> None:
        '''
        调用spark将mysql数据导入hive，并记录日志

        table={'name': 'db1',
        'source_tb': 'db_code',
        'source_tb': 't_admin_division_code',
        'sink_db': 'ods_syx_test',
        # 分库分表参数
        'db_start': 0,
        'db_num': 0, 
        't_start': 0, 
        't_num': 0,
        'other': False, 
        'partition_column': 'partition_date',
        'sink_tb': 'ods_q_db_code_t_admin_division_code'
        'update_column': 'local_row_update_time'
        }
        '''
        name = get_thread_id()
        logger.info(
            f"Thread-{name}:{table['source_db']}.{table['source_tb']}->{table['sink_db']}.{table['sink_tb']}执行开始")
        mysql_params = deepcopy(self.MYSQL_PARAMS)
        mysql_params['db'] = table.get('source_db')
        mysql_params['table'] = table.get('source_tb')
        # 日志
        log_data = deepcopy(self.log_data)
        log_data['source_db'] = table.get('source_db')
        log_data['source_tb'] = table.get('source_tb')
        log_data['sink_db'] = table.get('sink_db')
        log_data['sink_tb'] = table.get('sink_tb')
        try:
            df = getMySQLData(spark, mysql_params)

            # 导入数据到hive
            if table.get('update_column'):
                if self.TYPE == 'all':
                    df = df.where(f"{table['update_column']}<'{self.today_time.strftime('%Y-%m-%d 00:00:00')}'")
                elif self.TYPE == 'update':
                    df = df.where(
                        f"{table['update_column']} between '{self.yesterday_time.strftime('%Y-%m-%d 00:00:00')}' and '{self.today_time.strftime('%Y-%m-%d 00:00:00')}'")
                elif self.TYPE == 'other':
                    df = df.where(f"{table['update_column']} between '{self.start_time}' and '{self.end_time}'")
            # 查询为空
            if df.rdd.isEmpty():
                log_data['status'] = True
                log_data['num'] = 0
                logger.info(f"表{table['source_db']}.{table['source_tb']}无更新---num:0")
                log_data['msg'] = f"表{table['source_db']}.{table['source_tb']}无更新"
                return
            num = df.count()
            df.createOrReplaceTempView(f"{self.appName}_{name}")
            if table.get('partition_column'):
                # 删除partition_date分区已有数据
                try:
                    if table.get('is_del'):
                        spark.sql(
                            f'ALTER TABLE {table["sink_db"]}.{table["sink_tb"]} DROP PARTITION ({table.get("partition_column")}="{self.partition_date}")')
                except:
                    pass
                spark.sql(
                    f"INSERT INTO {table['sink_db']}.{table['sink_tb']} PARTITION({table.get('partition_column')}={self.partition_date}) SELECT * FROM {self.appName}_{name}")
            else:
                try:
                    if table.get('is_del'):
                        spark.sql(
                            f"TRUNCATE TABLE TABLE {table['sink_db']}.{table['sink_tb']})")
                except:
                    pass
                spark.sql(
                    f"INSERT INTO {table['sink_db']}.{table['sink_tb']} SELECT * FROM {self.appName}_{name}")
            logger.info(
                f"Thread-{name}:{table['source_db']}.{table['source_tb']}->{table['sink_db']}.{table['sink_tb']}执行成功---num:{num}")
            log_data['status'] = True
            log_data['num'] = num
            log_data[
                'msg'] = f"导入{table['source_db']}.{table['source_tb']}数据到hive表{table['sink_db']}.{table['sink_tb']}成功"
        except Exception as e:
            logger.error(
                f"{table['source_db']}.{table['source_tb']}->{table['sink_db']}.{table['sink_tb']}执行失败----error:{e}")
            log_data['msg'] = f"导入表{table['source_db']}.{table['source_tb']}失败----error:{e}"
        finally:
            log_data['local_row_update_time_end'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if self.DB_LOG:
                self.DB_LOG_CONN.save([log_data], self.appName, 'append')

    def hive_to_hive(self, spark, logger, table: Mapping[str, Any]) -> None:
        '''
        调用spark将hive数据导入hive，并记录日志

        table={'name': 'db1',
        'source_tb': 'db_code',
        'source_tb': 't_admin_division_code',
        'sink_tb': 'ods_q_db_code_t_admin_division_code'
        'sink_db': 'ods_syx_test',
        'SQL':'',
        'is_del':True,
        'partition_column': 'partition_date',
        'update_column':''
        }
        '''

        name = get_thread_id()
        logger.info(
            f'Thread-{name}:{table["source_db"]}.{table["source_tb"]}->{table["sink_db"]}.{table["sink_tb"]}执行开始')
        assert self.TYPE != 'other' or table.get('update_column', False), "other模式下update_column is not None"
        # 日志
        log_data = deepcopy(self.log_data)
        log_data['source_db'] = table.get('source_db')
        log_data['source_tb'] = table.get('source_tb')
        log_data['sink_db'] = table.get('sink_db')
        log_data['sink_tb'] = table.get('sink_tb')
        try:
            # 导入数据到hive
            if not table.get('partition_column'):
                try:
                    if table.get('is_del'):
                        spark.sql(
                            f'ALTER TABLE {table["sink_db"]}.{table["sink_tb"]} DROP PARTITION ({table.get("sink_partition_column")}="{self.partition_date}")')
                except:
                    pass
                SQL = f"select * from ({table.get('SQL')})"
            else:
                try:
                    if table.get('is_del'):
                        spark.sql(
                            f'TRUNCATE TABLE {table["sink_db"]}.{table["sink_tb"]}')
                except:
                    pass
                if self.TYPE == 'all':
                    SQL = f"select * from ({table.get('SQL')})"
                elif self.TYPE == 'update':
                    SQL = f"select * from ({table.get('SQL')}) where {table.get('partition_column')}= {self.partition_date}"
                elif self.TYPE == 'other':
                    SQL = f"select * from ({table.get('SQL')}) where {table.get('update_column')} between '{self.start_time}' and '{self.end_time}'"

            df = getHiveDataOnSQL(spark, SQL, table.get('partition_column'))
            log_data['SQL'] = SQL
            # 查询为空
            if df.rdd.isEmpty():
                log_data['status'] = True
                log_data['num'] = 0
                logger.info(f'表{table["sink_db"]}.{table["sink_tb"]}无更新---num:0')
                log_data['msg'] = f'表{table["sink_db"]}.{table["sink_tb"]}无更新'
                return
            num = df.count()
            df.createOrReplaceTempView(f"{self.appName}_{name}")
            if not table.get('partition_column'):
                spark.sql(
                    f'INSERT  OVERWRITE table {table["sink_db"]}.{table["sink_tb"]}  SELECT * FROM {self.appName}_{name}')

            else:
                spark.sql(
                    f"INSERT INTO {table['sink_db']}.{table['sink_tb']} PARTITION({table.get('partition_column')}= {self.partition_date}) SELECT * FROM {self.appName}_{name}")

            logger.info(
                f'Thread-{name}:{table["source_db"]}.{table["source_tb"]}->{table["sink_db"]}.{table["sink_tb"]}执行成功---num:{num}')
            log_data['status'] = True
            log_data['num'] = num
            log_data[
                'msg'] = f'导入{table["source_db"]}.{table["source_tb"]}数据到hive表{table["sink_db"]}.{table["sink_tb"]}成功'
        except Exception as e:
            logger.error(
                f'{table["source_db"]}.{table["source_tb"]}->{table["sink_db"]}.{table["sink_tb"]}执行失败----error:{e}')
            log_data['msg'] = f'导入表{table["source_db"]}.{table["source_tb"]}失败----error:{e}'
        finally:
            log_data['local_row_update_time_end'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if self.DB_LOG:
                self.DB_LOG_CONN.save([log_data], self.appName, 'append')

    def split_table_run(self, table: Mapping[str, Any]) -> None:
        name = os.getpid()
        findspark.init()
        spark = SparkSession.builder \
            .appName(self.appName + f'-{name}') \
            .master(self.master) \
            .config("spark.sql.catalogImplementation", "hive") \
            .getOrCreate()
        logger = getLog(self.appName)
        try:
            logger.info(
                f'process-{name}:{table["source_db"]}.{table["source_tb"]}->{table["sink_db"]}.{table["sink_tb"]}执行开始')
            start_time = time.time()
            table_tmp = deepcopy(table)
            tables = []
            # 单库单表
            if table.get('db_num', 0) == 0 and table.get('t_num', 0) == 0:
                table_tmp['source_db'] = table_tmp.get('source_db')
                table_tmp['source_tb'] = table_tmp.get('source_tb')
                tables = [table_tmp]
            # 单库多表
            elif table.get('db_num', 0) == 0 and table.get('t_num', 0) > 0:
                '''
                程序自动添加表下标并且依次遍历分表
                '''
                tables = []
                for i in range(table.get('t_start', 0), table.get('t_num', 0) + 1):
                    table_tmp['source_db'] = table_tmp.get('source_db') + f'_{i}'
                    table_tmp['source_tb'] = table_tmp.get('source_tb')
                    tables.append(deepcopy(table_tmp))
                if table.get('other'):
                    table_tmp['source_db'] = table_tmp.get('source_db') + '_pther'
                    table_tmp['source_tb'] = table_tmp.get('source_tb')
                    tables.append(deepcopy(table_tmp))
            # 多库多表
            elif table.get('db_num', 0) > 0 and table.get('t_num', 0) > 0:
                '''
                程序自动添加库和表下标并且依次遍历分表
                '''
                table['tables'] = []
                for i in range(table.get('db_start', 0), table.get('db_num', 0) + 1):
                    for j in range(table['t_start'], table.get('t_num', 0) + 1):
                        table_tmp['source_db'] = table_tmp.get('source_db') + f'_{i}'
                        table_tmp['source_tb'] = table_tmp.get('source_tb') + f'_{j}'
                        tables.append(deepcopy(table_tmp))
                    if table.get('other'):
                        table_tmp['source_db'] = table_tmp.get('source_db') + f'_{i}'
                        table_tmp['source_tb'] = table_tmp.get('source_tb') + f'_other'
                        tables.append(deepcopy(table_tmp))
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.maxWorkers) as executor:
                if self.outType == 1:
                    # 提交每个表的处理任务到线程池
                    futures = [executor.submit(functools.partial(self.mysql_to_hive, spark, logger, table)) for table in
                               tables]
                    # 等待所有任务完成
                    concurrent.futures.wait(futures)
                elif self.outType == 2:
                    # 提交每个表的处理任务到线程池
                    futures = [executor.submit(functools.partial(self.hive_to_mysql, spark, logger, table)) for table in
                               tables]
                    # 等待所有任务完成
                    concurrent.futures.wait(futures)
                elif self.outType == 3:
                    # 提交每个表的处理任务到线程池
                    futures = [executor.submit(functools.partial(self.hive_to_hive, spark, logger, table)) for table in
                               tables]
                    # 等待所有任务完成
                    concurrent.futures.wait(futures)
            end_time = time.time()
            logger.info(
                f'process-{name}:{table["source_db"]}.{table["source_tb"]}->{table["sink_db"]}.{table["sink_tb"]}执行结束--执行时间:{end_time - start_time}秒')
        except Exception as e:
            logger.error(e)
        finally:
            spark.stop()

    def run(self):
        # logger.setLevel("INFO")
        with multiprocessing.Pool(processes=self.maxProcess) as pool:
            # 使用进程池并行执行 worker 函数
            pool.map(self.split_table_run, self.Task)


if __name__ == '__main__':
    TASK = [

        {"name": "智联招聘爬虫数据", "source_db": "spider", "source_tb": "job", "db_num": 0, "t_num": 0,
         'sink_db': 'ods_job', 'sink_tb': 'ods_job_db_spider_t_job', "update_column": "create_time",
         'partition_column': 'partition_date'},
        {"name": "用户简历信息", "source_db": "job", "source_tb": "resume", "db_num": 0, "t_num": 0,
         'sink_db': 'ods_job', 'sink_tb': 'ods_job_db_job_t_resume', "update_column": "last_update",
         'partition_column': 'partition_date'}
    ]
    MYSQL_CONNECT = {
        'host': '10.8.16.253',
        'port': 3306,
        'user': 'root',
        'password': 'fiang123',
        'charset': 'utf8',
        'db': 'logs'
    }
    MYSQL_PARAMS = {
        'host': '10.8.16.253',
        'port': 3306,
        'user': 'root',
        'password': 'fiang123',
    }
    a = SparkMySQLHiveETL(DB_LOG_PARAMS=MYSQL_CONNECT, MYSQL_PARAMS=MYSQL_PARAMS, appName='ods', Task=TASK)
    a.run()
