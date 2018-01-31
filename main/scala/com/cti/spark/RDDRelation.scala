package com.cti.spark

import org.apache.spark.SparkConf
import org.apache.spark.sql.{SaveMode, SparkSession}

case class Record(key:Int,value:String)
object RDDRelation {
    def main(args: Array[String]): Unit = {
        val conf = new SparkConf()
        conf.setAppName("rddrelation")
        conf.setMaster("local[5]")

        val spark = SparkSession.builder().config(conf).getOrCreate()

        import spark.implicits._

        val df = spark.createDataFrame((1 to 100).map(i => Record(i, s"val_$i")))
        //创建临时表，可以写sql
        df.createOrReplaceTempView("records")
       // spark.sql("select * from records").collect().foreach(println)

        //聚合
//        val count = spark.sql("select count(*) from records").collect().head.getLong(0)
//        print(count)

//        val rddFromSql = spark.sql("SELECT key, value FROM records WHERE key < 10")
//        rddFromSql.rdd.map(row => s"Key:${row(0)},Value:${row(1)}").collect().foreach(println)

//        df.where($"key"===1).orderBy($"value".asc).select($"key").collect().foreach(println)
//   写rdd为parquet文件
       // df.write.mode(SaveMode.Overwrite).parquet("file:///home/tianlei/pair.parquet")

        //读取parquet文件
        val parquetFile = spark.read.parquet("file:///home/tianlei/pair.parquet")
        parquetFile.where($"key" === 1).select($"value".as("a")).collect().foreach(println)

        //创建临时视图
        parquetFile.createOrReplaceTempView("parquetFile")
        spark.sql("select * from parquetFile").collect().foreach(println)

        spark.stop()



    }



}
