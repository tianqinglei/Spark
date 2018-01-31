from pyspark.sql import Row,SparkSession
from pyspark.ml.clustering import KMeans, KMeansModel
from pyspark.context import SparkContext as sc
from pyspark.ml.linalg import Vectors

if __name__ == "__main__":
    spark = SparkSession \
        .builder \
        .appName("ChiSqSelectorExample") \
        .getOrCreate()
    rawData = spark.sparkContext.textFile("file:///home/tianlei/iris.txt")


    def f(x):
        rel = {}
        rel['features'] = Vectors.dense(float(x[0]), float(x[1]), float(x[2]), float(x[3]))
        return rel


    df = sc.textFile("file:///usr/local/spark/iris.txt").map(lambda line: line.split(',')).map(lambda p: Row(**f(p))).toDF()
    # 在得到数据后，我们即可通过ML包的固有流程：创建Estimator并调用其fit()
    # 方法来生成相应的Transformer对象，很显然，在这里KMeans类是Estimator，而用于保存训练后模型的KMeansModel类则属于Transformer：
    kmeansmodel = KMeans.setK(3).setFeaturesCol('features').setPredictionCol('prediction').fit(df)
    # KMeansModel作为一个Transformer，不再提供predict()样式的方法，
    # 而是提供了一致性的transform()方法，用于将存储在DataFrame中的给定数据集进行整体处理，
    # 生成带有预测簇标签的数据集：
    results = kmeansmodel.transform(df).collect()
    for item in results:

        print(str(item[0]) + ' is predcted as cluster' + str(item[1]))