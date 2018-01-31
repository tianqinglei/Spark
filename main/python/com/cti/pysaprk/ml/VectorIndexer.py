from __future__ import print_function
# 倘若所有特征都已经被组织在一个向量中，又想对其中某些单个分量进行处理时，
# Spark ML提供了VectorIndexer类来解决向量数据集中的类别性特征转换
# 通过为其提供maxCategories超参数，它可以自动识别哪些特征是类别型的，
# 并且将原始值转换为类别索引。它基于不同特征值的数量来识别哪些特征需要被类别化，
# 那些取值可能性最多不超过maxCategories的特征需要会被认为是类别型的。


from pyspark.ml.feature import VectorIndexer

from pyspark.sql import SparkSession

if __name__ == "__main__":
    spark = SparkSession \
        .builder \
        .appName("VectorIndexerExample") \
        .getOrCreate()


    data = spark.read.format("libsvm").load("file:///home/tianlei/soft/spark/data/mllib/sample_libsvm_data.txt")

    indexer = VectorIndexer(inputCol="features", outputCol="indexed", maxCategories=10)
    indexerModel = indexer.fit(data)

    categoricalFeatures = indexerModel.categoryMaps
    print("Chose %d categorical features: %s" %
          (len(categoricalFeatures), ", ".join(str(k) for k in categoricalFeatures.keys())))


    indexedData = indexerModel.transform(data)
    indexedData.show()


    spark.stop()
