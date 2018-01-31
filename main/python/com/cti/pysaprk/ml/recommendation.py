# 导入需要的包
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.recommendation import ALS
from pyspark.sql import Row, SparkSession
from pyspark.context import SparkContext as sc

if __name__ == "__main__":
    spark = SparkSession \
        .builder \
        .appName("LogisticRegressionWithElasticNet") \
        .getOrCreate()


    def f(x):
        rel = {}
        rel['userId'] = int(x[0])
        rel['movieId'] = int(x[0])
        rel['rating'] = int(x[0])
        rel['timeStamp'] = int(x[0])
        return rel


    # 读书数据
    ratings = sc.textFile("file:////spark/data/mllib/als/sample_movielens_ratings.txt").map(
        lambda line: line.split('::')).map(lambda p: Row(**f(p))).toDF()

    # 构建模型
    # 把MovieLens数据集划分训练集和测试集
    training, test = ratings.randomSplit([0.8, 0.2])
    # 使用ALS来建立推荐模型，这里我们构建了两个模型，一个是显性反馈，一个是隐性反馈
    alsExplicit = ALS(maxIter=5, regParam=0.01, userCol="userId", itemCol="movieId", ratingCol="rating")
    alsImplicit = ALS(maxIter=5, regParam=0.01, implicitPrefs=True, userCol="userId", itemCol="movieId",
                      ratingCol="rating")
    modelExplicit = alsExplicit.fit(training)
    modelImplicit = alsImplicit.fit(training)
    #  把推荐模型放在训练数据上训练：
    predictionsExplicit = modelExplicit.transform(test)
    predictionsImplicit = modelImplicit.transform(test)

    # 模型评估
    # 通过计算模型的均方根误差来对模型进行评估，均方根误差越小，模型越准确：
    evaluator = RegressionEvaluator().setMetricName("rmse").setLabelCol("rating").setPredictionCol("prediction")
    # 打印出两个模型的均方根误差 ：
    # print("Explicit:Root-mean-square error = " + str(rmseExplicit))
    #
    # print("Explicit:Root-mean-square error = " + str(rmseImplicit))
