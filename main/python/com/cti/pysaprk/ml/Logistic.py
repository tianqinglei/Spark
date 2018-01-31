# 导入需要的包
from pyspark.sql import Row, functions, SparkSession

from pyspark.context import  SparkContext
from pyspark.ml.linalg import Vector, Vectors
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml import Pipeline
from pyspark.ml.feature import IndexToString, StringIndexer, VectorIndexer, HashingTF, Tokenizer
from pyspark.ml.classification import LogisticRegression, LogisticRegressionModel, BinaryLogisticRegressionSummary, \
    LogisticRegression

if __name__ == "__main__":
    spark = SparkSession \
        .builder \
        .appName("ChiSqSelectorExample") \
            .getOrCreate()
    # 2. 读取数据，简要分析：
    #  我们定制一个函数，来返回一个指定的数据，然后读取文本文件，第一个map把每行的数据用“,”隔开，比如在我们的数据集中，每行被分成了5部分，
    # 前4部分是鸢尾花的4个特征，最后一部分是鸢尾花的分类；我们这里把特征存储在Vector中，创建一个Iris模式的RDD，然后转化成dataframe；
    # 最后调用show()方法来查看一下部分数据。
    def f(x):
        rel = {}
        rel['feartures'] = Vectors.dense(float(x[0]), float(x[1]), float(x[2]), float(x[3]))
        rel ['label'] = str(x[4])
        return  rel

    data = spark.sparkContext.textFile("file:///home/tianlei/iris.txt").map(lambda line: line.split(',')).map(lambda p: Row(**f(p))).toDF()
    data.show()
    #     因为我们现在处理的是2分类问题，所以我们不需要全部的3类数据，我们要从中选出两类的数据。这里首先把刚刚得到的数据注册成一个表iris，
    # 注册成这个表之后，我们就可以通过sql语句进行数据查询，比如我们这里选出了所有不属于“Iris-setosa”类别的数据；
    # 选出我们需要的数据后，我们可以把结果打印出来看一下，这时就已经没有“Iris-setosa”类别的数据。
    data.createOrReplaceTempView("iris")
    df = spark.sql("select * from iris where label != 'Iris-setosa'")
    rel = df.map(lambda t: str(t[1]) + ":" + str(t[0])).collect()
    for item in rel:
        print(item)

    # 构建ML的pipeline
    # 分别获取标签列和特征列，进行索引，并进行了重命名。
    lalelIndexer = StringIndexer.setInputCol("label").setOutputCol("indexeLabel").fit(df)
    featureIndexer = VectorIndexer.setInputCol("features").setOutputCol("indexeFeatures").fit(df)

    #     数据集随机分成训练集和测试集，其中训练集占70%。
    trainingData,testData = df.randomSplit([0.7,0.3])
    #    设置logistic的参数，这里我们统一用setter的方法来设置，也可以用ParamMap来设置（具体的可以查看spark mllib的官网）。
    # 这里我们设置了循环次数为10次，正则化项为0.3等，具体的可以设置的参数可以通过explainParams()来获取，
    # 还能看到我们已经设置的参数的结果。
    lr = LogisticRegression.setLabelCol("lalelIndexer").setFeaturesCol("featureIndexer").setMaxIter(10).setRegParam(
        0.3).setElasticNetParam(0.8)
    print("LogisticRegression parameters:\n" + lr.explainParams())
    # 设置一个labelConverter，目的是把预测的类别重新转化成字符型的。
    labelConverter = IndexToString().setInputCol("prediction").setOutputCol("predictedLabel").setLabels(
        lalelIndexer.labels)
    #     构建pipeline，设置stage，然后调用fit()来训练模型。
    lrPipeline = Pipeline().setStages([lalelIndexer, featureIndexer, lr, labelConverter])
    lrPipelineModel = lrPipeline.fit(trainingData)

    #      pipeline本质上是一个Estimator，当pipeline调用fit()的时候就产生了一个PipelineModel，
    # 本质上是一个Transformer。然后这个PipelineModel就可以调用transform()来进行预测，生成一个新的DataFrame，
    # 即利用训练得到的模型对测试集进行验证。
    lrPredictions = lrPipelineModel.transform(testData)
    #     后我们可以输出预测的结果，其中select选择要输出的列，collect获取所有行的数据，用foreach把每行打印出来。
    # 其中打印出来的值依次分别代表该行数据的真实分类和特征值、预测属于不同分类的概率、预测的分类。
    preRel = lrPredictions.select("predictedLabel", "label", "features", "probability").collect()
    for item in preRel:
        print(str(item['label']) + ',' + str(item['features']) + '-->prob=' + str(
            item['probability']) + ',predictedLabel' + str(item['predictedLabel']))






