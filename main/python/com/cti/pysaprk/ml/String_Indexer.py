from __future__ import print_function

# $example on$
from pyspark.ml.feature import StringIndexer
# $example off$
from pyspark.sql import SparkSession

if __name__ == "__main__":
    spark = SparkSession \
        .builder \
        .appName("StringIndexerExample") \
        .getOrCreate()

    # 创建一个简单的DataFrame，它只包含一个id列和一个标签列category：
    df = spark.createDataFrame(
        [(0, "a"), (1, "b"), (2, "c"), (3, "a"), (4, "a"), (5, "c")],
        ["id", "category"])
    # 我们创建一个StringIndexer对象，设定输入输出列名，其余参数采用默认值，并对这个DataFrame进行训练，
    # 产生StringIndexerModel对象：
    indexer = StringIndexer(inputCol="category", outputCol="categoryIndex")
    indexed = indexer.fit(df).transform(df)
    indexed.show()
    # 随后即可利用该对象对DataFrame进行转换操作，可以看到，StringIndexerModel依次按照出现频率的高低，
    # 把字符标签进行了排序，即出现最多的“a”被编号成0，“c”为1，出现最少的“b”为0。

    spark.stop()
