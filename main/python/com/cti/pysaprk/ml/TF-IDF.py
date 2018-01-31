from __future__ import print_function
from pyspark.ml.feature import HashingTF, IDF, Tokenizer
from pyspark.sql import SparkSession

if __name__ == "__main__":
    spark = SparkSession \
        .builder \
        .appName("TfIdfExample") \
        .getOrCreate()


    sentenceData = spark.createDataFrame([
        (0.0, "Hi I heard about Spark"),
        (0.0, "I wish Java could use case classes"),
        (1.0, "Logistic regression models are neat")
    ], ["label", "sentence"])
    # 文档集合后，即可用tokenizer对句子进行分词
    tokenizer = Tokenizer(inputCol="sentence", outputCol="words")
    wordsData = tokenizer.transform(sentenceData)
    # 得到分词后的文档序列后，即可使用HashingTF的transform()方法把句子哈希成特征向量，这里设置哈希表的桶数为2000。
    hashingTF = HashingTF(inputCol="words", outputCol="rawFeatures", numFeatures=20)
    featurizedData = hashingTF.transform(wordsData)
    # alternatively, CountVectorizer can also be used to get term frequency vectors
    # IDF来对单纯的词频特征向量进行修正，使其更能体现不同词汇对文本的区别能力，IDF是一个Estimator，调用fit()
    # 方法并将词频向量传入，即产生一个IDFModel。
    idf = IDF(inputCol="rawFeatures", outputCol="features")
    idfModel = idf.fit(featurizedData)
    # IDFModel是一个Transformer，调用它的transform()方法，即可得到每一个单词对应的TF-IDF度量值。
    rescaledData = idfModel.transform(featurizedData)

    rescaledData.select("label", "features").show()


    spark.stop()
