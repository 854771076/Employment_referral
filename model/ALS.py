from pyspark.ml.feature import VectorAssembler
from pyspark.ml.linalg import Vectors, DenseVector
from pyspark.ml.feature import Normalizer,MinMaxScaler
from pyspark.sql.functions import *
from pyspark.sql import SparkSession
from pyspark.sql.types import *
import numpy as np

MYSQL_PARAMS = {
        'host': '10.8.16.83',
        'port': 3306,
        'user': 'root',
        'password': 'fiang123',
        'db':'jobfree',
        'table':'recommendforallusers'
    }


spark = SparkSession.builder \
    .appName("model") \
    .master('yarn') \
    .config('spark.sql.shuffle.partitions', '200') \
    .config('spark.jars', 'hdfs:///user/cdh/jars/mysql-connector-java-5.1.49.jar') \
    .getOrCreate()
weights =[0.2124, 0.1711, 0.0709, 0.1368, 0.3194, 0.0236, 0.0658]
def weighted_cos_similarity(vector1, vector2):
    # 确保向量和权重的长度相同
    assert len(vector1) == len(vector2) == len(weights), "向量和权重的长度必须相同"
    # 计算向量每个元素乘以对应权重后的加权向量
    weighted_vector1 = np.multiply(vector1, weights)
    weighted_vector2 = np.multiply(vector2, weights)
    # 计算加权向量的点积
    dot_product = np.dot(weighted_vector1, weighted_vector2)
    # 计算加权向量的模
    norm_vector1 = np.linalg.norm(weighted_vector1)
    norm_vector2 = np.linalg.norm(weighted_vector2)
    # 计算带权重的余弦相似度
    similarity = dot_product / (norm_vector1 * norm_vector2)
    return float(similarity)
def cos_similarity(Vector1, Vector2):
    similarity = Vector1.dot(Vector2) / (np.linalg.norm(Vector1) * np.linalg.norm(Vector2))
    return float(similarity)
cos_similarity_udf = udf(cos_similarity, DoubleType())
weighted_cos_similarity_udf = udf(weighted_cos_similarity, DoubleType())
# 加载用户画像数据
user_profile_df = spark.sql('SELECT * FROM `dwd_jobfree`.`dwd_jobfree_db_jobfree_t_resume_train`')
job_postings_df = spark.sql('SELECT * FROM `dwd_jobfree`.`dwd_jobfree_db_spider_t_jobs_train`  ')
user_profile_df=user_profile_df.drop('selfevaluate','skilllabel','summary','words','words2','text_features','text_features2','features','pcaFeatures','preferredSalaryMax')
job_postings_df =job_postings_df .drop('jobsummary','skilllabel','summary','words','words2','text_features','text_features2','features','pcaFeatures','salary_max')

# 合并用户画像特征为一个向量列
assembler = VectorAssembler(inputCols=user_profile_df.columns[1:], outputCol="features")
user_profile_df = assembler.transform(user_profile_df)

# 合并招聘信息特征为一个向量列
assembler = VectorAssembler(inputCols=job_postings_df.columns[1:], outputCol="features")
job_postings_df = assembler.transform(job_postings_df)
# 标准化向量列
minmax = MinMaxScaler(inputCol="features", outputCol="job_features_norm")
minmax_model=minmax.fit(job_postings_df)

job_postings_df =minmax_model.transform(job_postings_df)
minmax =MinMaxScaler(inputCol="features", outputCol="user_features_norm")
minmax_model=minmax.fit(job_postings_df)
user_profile_df = minmax_model.transform(user_profile_df)

# # 获取用户画像向量和招聘信息特征向量的笛卡尔积
cartesian_df = user_profile_df.crossJoin(job_postings_df)


# # 计算相似度
# cartesian_df = cartesian_df.withColumn("similarity",cos_similarity_udf(cartesian_df['user_features_norm'],cartesian_df['job_features_norm']) )
cartesian_df = cartesian_df.withColumn("similarity",weighted_cos_similarity_udf(cartesian_df['user_features_norm'],cartesian_df['job_features_norm']) )

# # 显示相似度计算结果，可以根据需要进行进一步筛选和排序
cartesian_df.orderBy("similarity", ascending=False).show()

# # 假设筛选条件为相似度大于0.9的用户-招聘信息对
filtered_df = cartesian_df.filter("similarity> 0.7")
# # 根据相似度值进行降序排序
sorted_df = filtered_df.orderBy("similarity", ascending=False)

from pyspark.ml.recommendation import ALS
rating_matrix_df=sorted_df.selectExpr('user_id','job_id','similarity')
rating_matrix_df.show()
# 创建ALS模型实例
als = ALS(userCol="user_id", itemCol="job_id", ratingCol="similarity", coldStartStrategy="drop",implicitPrefs=True,maxIter=10,regParam=0.01)

# 拆分数据集为训练集和测试集
(training_data, test_data) = rating_matrix_df.randomSplit([0.8, 0.2])

# 训练ALS模型
model = als.fit(training_data)

from pyspark.ml.evaluation import RegressionEvaluator
# 使用测试集评估模型
predictions = model.transform(test_data)

# 创建 RegressionEvaluator 评估器
evaluator = RegressionEvaluator(labelCol="similarity", predictionCol="prediction", metricName="rmse")
# 计算 RMSE
rmse = evaluator.evaluate(predictions)
# 输出评估结果
print("Root Mean Squared Error (RMSE):", rmse)
df=model.recommendForAllUsers(180)
df.createOrReplaceTempView('recommendForAllUsers')
spark.sql('INSERT  OVERWRITE table ads_jobfree.ads_jobfree_db_jobfree_t_recommendforallusers  SELECT user_id,to_json(recommendations) FROM recommendForAllUsers')

df2=spark.sql('SELECT * FROM ads_jobfree.ads_jobfree_db_jobfree_t_recommendforallusers')
df2.write.format('jdbc') \
        .mode('overwrite') \
        .option('url',
                f"jdbc:mysql://{MYSQL_PARAMS.get('host')}:{MYSQL_PARAMS.get('port')}/{MYSQL_PARAMS.get('db')}?useSSL=false&useUnicode=true") \
        .option('dbtable', MYSQL_PARAMS.get('table')) \
        .option('user', MYSQL_PARAMS.get('user')) \
        .option('driver', 'com.mysql.jdbc.Driver') \
        .option('password', MYSQL_PARAMS.get('password')) \
        .save()