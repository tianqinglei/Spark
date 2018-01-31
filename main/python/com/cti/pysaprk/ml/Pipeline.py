#  引入要包含的包并构建训练数据集。
from pyspark.ml import Pipeline
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.feature import HashingTF, Tokenizer

from pyspark.sql import SparkSession
from pyspark.conf import SparkConf


if __name__ == "__main__":
    # # conf = SparkConf().setMaster("local[4]").setAppName("PipelineExample")
    # spark = SparkSession \
    #     .builder \
    #     .config(conf) \
    #     .getOrCreate()
    spark = SparkSession \
        .builder \
        .appName("PipelineExample") \
        .getOrCreate()

    # $example on$
    # Prepare training documents from a list of (id, text, label) tuples.
    training = spark.createDataFrame([
        (0, "a b c d e spark", 1.0),
        (1, "b d", 0.0),
        (2, "spark f g h", 1.0),
        (3, "hadoop mapreduce", 0.0)
    ], ["id", "text", "label"])

    tokenizer = Tokenizer(inputCol="text", outputCol="words")
    hashingTF = HashingTF(inputCol=tokenizer.getOutputCol(), outputCol="features")
    lr = LogisticRegression(maxIter=10, regParam=0.001)
    pipeline = Pipeline(stages=[tokenizer, hashingTF, lr])

    # 现在构建的Pipeline本质上是一个Estimator，在它的fit（）方法运行之后，它将产生一个PipelineModel，它是一个Transformer
    model = pipeline.fit(training)

    # 测试数据的时候使用。
    test = spark.createDataFrame([
        (4, "spark i j k"),
        (5, "l m n"),
        (6, "spark hadoop spark"),
        (7, "apache hadoop")
    ], ["id", "text"])

    # 调用我们训练好的PipelineModel的transform（）方法，让测试数据按顺序通过拟合的工作流，生成我们所需要的预测结果。
    prediction = model.transform(test)
    selected = prediction.select("id", "text", "probability", "prediction")
    for row in selected.collect():
        rid, text, prob, prediction = row
        print("(%d, %s) --> prob=%s, prediction=%f" % (rid, text, str(prob), prediction))

    spark.stop()
