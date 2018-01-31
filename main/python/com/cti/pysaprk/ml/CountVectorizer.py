from __future__ import print_function

from pyspark.sql import SparkSession

from pyspark.ml.feature import CountVectorizer



if __name__ == "__main__":
    spark = SparkSession \
        .builder \
        .appName("CountVectorizerExample") \
        .getOrCreate()

    #
    # 假设我们有如下的DataFrame，其包含id和words两列，可以看成是一个包含两个文档的迷你语料库。
    df = spark.createDataFrame([
        (0, "a b c".split(" ")),
        (1, "a b b c a".split(" "))
    ], ["id", "words"])

    # 通过CountVectorizer设定超参数，训练一个CountVectorizer，
    # 这里设定词汇表的最大量为3，设定词汇表中的词至少要在2个文档中出现过，以过滤那些偶然出现的词汇。
    cv = CountVectorizer(inputCol="words", outputCol="features", vocabSize=3, minDF=2.0)

    model = cv.fit(df)

    result = model.transform(df)
    result.show(truncate=False)


    spark.stop()
