
#导入需要的包：
from pyspark.ml.linalg import Vector, Vectors
from pyspark.sql import Row,SparkSession
from pyspark.context import SparkContext
from pyspark.ml import Pipeline
from pyspark.ml.feature import IndexToString, StringIndexer, VectorIndexer
from pyspark.ml.classification import  DecisionTreeClassifier,DecisionTreeClassificationModel
from pyspark.ml.evaluation import  MulticlassClassificationEvaluator
# 读取数据，简要分析：
if __name__ == "__main__":

    spark = SparkSession \
        .builder \
        .appName("ChiSqSelectorExample") \
        .getOrCreate()
    # 读取文本文件，第一个map把每行的数据用“,”隔开，比如在我们的数据集中，每行被分成了5部分，前4部分是鸢尾花的4个特征，
    # 最后一部分是鸢尾花的分类；我们这里把特征存储在Vector中，创建一个Iris模式的RDD，
    # 然后转化成dataframe；然后把刚刚得到的数据注册成一个表iris，注册成这个表之后，我们就可以通过sql语句进行数据查询；
    # 选出我们需要的数据后，我们可以把结果打印出来查看一下数据。

    def f(x):
        rel = {}
        rel['features'] = Vectors.dense(float(x[0]), float(x[1]), float(x[2]), float(x[3]))
        rel['label'] = str(x[4])
        return rel

    data = spark.sparkContext.textFile("file:///home/tianlei/iris.txt").map(lambda line: line.split(',')).map(
    lambda p: Row(**f(p))).toDF()
    data.createOrReplaceTempView("iris")

    df = spark.sql("select * from iris")
    rel = df.rdd.map(lambda t :str(t[1]+ ":"+str(t[0]))).collect()
    for item in rel:
        print(item)

    #3. 进一步处理特征和标签，以及数据分组：
    # 分别获取标签列和特征列，进行索引，并进行了重命名
    labelIndexer = StringIndexer().setInputCol("label").setOutputCol("indexedLabe").fit(df)
    featureIndexer = VectorIndexer().setInputCol("features").setOutputCol("indexedFeatures").setMaxCategories(4).fit(df)

    #     /这里我们设置一个labelConverter，目的是把预测的类别重新转化成字符型的。
    labelConverter = IndexToString().setInputCol("prediction").setOutputCol("predictedLabel").setLabels(labelIndexer.labels)

    # 接下来，我们把数据集随机分成训练集和测试集，其中训练集占70%。
    trainingData, testData = data.randomSplit([0.7, 0.3])


    #     构建决策树分类模型：
    #     训练决策树模型,这里我们可以通过setter的方法来设置决策树的参数，
    # 也可以用ParamMap来设置（具体的可以查看spark mllib的官网）。具体的可以设置的参数可以通过explainParams()来获取。
    dtClassifier = DecisionTreeClassifier().setLabelCol("labelIndexer").setFeaturesCol("featureIndexer")
    # /在pipeline中进行设置stage
    pipelinedClassifier = Pipeline().setStages([labelIndexer, featureIndexer, dtClassifier, labelConverter])

    # //训练决策树模型
    modelClassifier = pipelinedClassifier.fit(trainingData)

    #     //进行预测
    predictionsClassifier = modelClassifier.transform(testData)
    # // 查看部分预测的结果
    predictionsClassifier.select("predictedLabel", "label", "features").show(20)

    #     评估决策树分类模型：
    evaluatorClassifier = MulticlassClassificationEvaluator().setLabelCol("indexedLabe").setPredictionCol("prediction").setMetricName("accuracy")

    accuracy = evaluatorClassifier.evaluate(predictionsClassifier)
    print("Test Error = " + str(1.0 - accuracy))
    treeModelClassifier = modelClassifier.stages[2]

    print("Learned classification tree model:\n" + str(treeModelClassifier.toDebugString))
