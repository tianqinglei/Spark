from __future__ import print_function


from pyspark.ml.feature import OneHotEncoder, StringIndexer

from pyspark.sql import SparkSession

if __name__ == "__main__":
    spark = SparkSession \
        .builder \
        .appName("OneHotEncoderExample") \
        .getOrCreate()

    # 首先创建一个DataFrame，其包含一列类别性特征，需要注意的是，在使用OneHotEncoder进行转换前，
    # DataFrame需要先使用StringIndexer将原始标签数值化：
    df = spark.createDataFrame([
        (0, "a"),
        (1, "b"),
        (2, "c"),
        (3, "a"),
        (4, "a"),
        (5, "c")
    ], ["id", "category"])

    stringIndexer = StringIndexer(inputCol="category", outputCol="categoryIndex")
    model = stringIndexer.fit(df)
    indexed = model.transform(df)
    # 我们创建OneHotEncoder对象对处理后的DataFrame进行编码，可以看见，编码后的二进制特征呈稀疏向量形式，
    # 与StringIndexer编码的顺序相同，
    # 需注意的是最后一个Category（”b”）被编码为全0向量，若希望”b”也占有一个二进制特征，
    # 则可在创建OneHotEncoder时指定setDropLast(false)。
    encoder = OneHotEncoder(inputCol="categoryIndex", outputCol="categoryVec")
    encoded = encoder.transform(indexed)
    encoded.show()

    spark.stop()
