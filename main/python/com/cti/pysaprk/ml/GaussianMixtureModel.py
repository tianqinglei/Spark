from pyspark.sql import Row,SparkSession
from pyspark.ml.clustering import GaussianMixture, GaussianMixtureModel
from pyspark.ml.linalg import Vectors
from pyspark.context import SparkContext as sc

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


    df = sc.textFile("file:///usr/local/spark/iris.txt").map(lambda line: line.split(',')).map(
        lambda p: Row(**f(p))).toDF()
    # 我们建立一个简单的GaussianMixture对象，设定其聚类数目为3，其他参数取默认值。
    gm = GaussianMixture().setK(3).setPredictionCol("Prediction").setProbabilityCol("Probability")
    gmm = gm.fit(df)
    # 调用transform()方法处理数据集之后，打印数据集，可以看到每一个样本的预测簇以及其概率分布向量
    # （这里为了明晰起见，省略了大部分行，只选择三行）：
    result = gmm.transform(df)
    result.show(150, False)
    # 得到模型后，即可查看模型的相关参数，与KMeans方法不同，GMM不直接给出聚类中心，
    # 而是给出各个混合成分（多元高斯分布）的参数。在ML的实现中，
    # GMM的每一个混合成分都使用一个MultivariateGaussian类（位于org.apache.spark.ml.stat.distribution包）来存储，
    # 我们可以使用GaussianMixtureModel类的weights成员获取到各个混合成分的权重，
    # 使用gaussians成员来获取到各个混合成分的参数（均值向量和协方差矩阵）：
    for i in range(3):
        print("Component " + str(i) + " : weight is " + str(gmm.weights[i]) + "\n mu vector is " + str(
            gmm.gaussiansDF.select('mean').head()) + " \n sigma matrix is " + str(gmm.gaussiansDF.select('cov').head()))