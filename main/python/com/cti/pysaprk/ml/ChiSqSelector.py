from __future__ import print_function

from pyspark.sql import SparkSession

from pyspark.ml.feature import ChiSqSelector
from pyspark.ml.linalg import Vectors

# $example off$

if __name__ == "__main__":
    spark = SparkSession \
        .builder \
        .appName("ChiSqSelectorExample") \
        .getOrCreate()

    # 这是一个具有三个样本，四个特征维度的数据集，标签有1，0两种，我们将在此数据集上进行卡方选择：
    df = spark.createDataFrame([
        (7, Vectors.dense([0.0, 0.0, 18.0, 1.0]), 1.0,),
        (8, Vectors.dense([0.0, 1.0, 12.0, 0.0]), 0.0,),
        (9, Vectors.dense([1.0, 0.0, 15.0, 0.1]), 0.0,)], ["id", "features", "clicked"])
    # 用卡方选择进行特征选择器的训练，为了观察地更明显，我们设置只选择和标签关联性最强的一个特征
    # 可以通过numTopFeatures参数方法进行设置）：
    selector = ChiSqSelector(numTopFeatures=1, featuresCol="features",
                             outputCol="selectedFeatures", labelCol="clicked")

    result = selector.fit(df).transform(df)

    print("ChiSqSelector output with top %d features selected" % selector.getNumTopFeatures())
    result.show()

    # 用训练出的模型对原数据集进行处理，可以看见，第三列特征被选出作为最有用的特征列：
    spark.stop()
