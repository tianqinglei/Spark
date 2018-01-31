from __future__ import print_function

# $example on$
from pyspark.ml.classification import LogisticRegression
# $example off$
from pyspark.sql import SparkSession

if __name__ == "__main__":
    spark = SparkSession \
        .builder \
        .appName("LogisticRegressionWithElasticNet") \
        .getOrCreate()


    # 加载数据
    training = spark.read.format("libsvm").load("file:///home/tianlei/soft/spark/data/mllib/sample_libsvm_data.txt")

    lr = LogisticRegression(maxIter=10, regParam=0.3, elasticNetParam=0.8)

    # Fit 模型
    lrModel = lr.fit(training)

    #
    print("Coefficients: " + str(lrModel.coefficients))
    print("Intercept: " + str(lrModel.intercept))

    # 也可以使用多项分类进行二元分类
    mlr = LogisticRegression(maxIter=10, regParam=0.3, elasticNetParam=0.8, family="multinomial")

    # Fit 模型
    mlrModel = mlr.fit(training)

    # Print the coefficients and intercepts for logistic regression with multinomial family
    print("Multinomial coefficients: " + str(mlrModel.coefficientMatrix))
    print("Multinomial intercepts: " + str(mlrModel.interceptVector))
    # $example off$

    spark.stop()
