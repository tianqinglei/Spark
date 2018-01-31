from __future__ import print_function

# 导入Word2Vec所需要的包，
from pyspark.ml.feature import Word2Vec

from pyspark.sql import SparkSession

if __name__ == "__main__":
    spark = SparkSession \
        .builder \
        .appName("Word2VecExample") \
        .getOrCreate()

    # 并创建三个词语序列，每个代表一个文档：
    documentDF = spark.createDataFrame([
        ("Hi I heard about Spark".split(" "),),
        ("I wish Java could use case classes".split(" "),),
        ("Logistic regression models are neat".split(" "),)
    ], ["text"])

    # 新建一个Word2Vec，显然，它是一个Estimator，设置相应的超参数，这里设置特征向量的维度为3，Word2Vec模型还有其他可设置的超参数，
    word2Vec = Word2Vec(vectorSize=3, minCount=0, inputCol="text", outputCol="result")
    # 读入训练数据，用fit()方法生成一个Word2VecModel。
    model = word2Vec.fit(documentDF)
    # 利用Word2VecModel把文档转变成特征向量。
    result = model.transform(documentDF)
    for row in result.collect():
        text, vector = row
        print("Text: [%s] => \nVector: %s\n" % (", ".join(text), str(vector)))


    spark.stop()
