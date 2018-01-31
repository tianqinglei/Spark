package com.cti.spark

import org.apache.spark.SparkConf
import org.apache.spark.sql.SparkSession

object SparkSQL {


   
    case class Person (name:String,age:Long)

   

    def main(args: Array[String]): Unit = {
        val conf = new SparkConf()
        conf.setAppName("rddrelation")
        conf.setMaster("local[5]")

        val spark = SparkSession.builder().config(conf).getOrCreate()

        import spark.implicits._
       // runBasicDataFrame(spark)
        //runDatasetCreation(spark)
        runInferSchema(spark)

        spark.stop()

    }

    /**
      *   DataFrame基本操作
      * @param spark
      */

    def runBasicDataFrame(spark: SparkSession):Unit = {
        val df = spark.read.json("file:///home/tianlei/soft/spark/examples/src/main/resources/people.json")
        df.show()

        import spark.implicits._
//        df.printSchema()
//        df.select("name").show()
//        df.select($"name",$"age" + 1).show()
//        df.filter($"age" > 21).show()
//        df.groupBy("age").count().show()
        //注册数据框为临时视图

//         df.createOrReplaceTempView("people")
//        val sqlDF = spark.sql("select * from people")
//        sqlDF.show()
         //注册为全局临时视图
        df.createGlobalTempView("people")
        //spark.sql("select * from global_temp.people").show()
        spark.newSession().sql("select * from global_temp.people").show()
        

    }

    /**
      * DataSet操作
      * @param spark
      */
    def runDatasetCreation(spark: SparkSession):Unit = {
        import spark.implicits._
        val caseClassDS = Seq(Person("Andy", 32)).toDS()
        caseClassDS.show()

         val primitiveDS = Seq(1, 2, 3).toDS()
         primitiveDS.map(_ + 1).collect()
        
           //DataFrame可以转化为DataSet
         val path = "file:///home/tianlei/soft/spark/examples/src/main/resources/people.json"
        val peopleDS =spark.read.json(path).as[Person]
        peopleDS.show()
     
    }
     def runInferSchema(spark: SparkSession) :Unit= {
         import spark.implicits._
         val peopleDF = spark.sparkContext
             .textFile("file:///home/tianlei/soft/spark/examples/src/main/resources/people.txt")
             .map(_.split(","))
             .map(attributes =>Person(attributes(0),attributes(1).trim.toInt))
             .toDF()
         //注册为临时表
         peopleDF.createOrReplaceTempView("people")
         val teenagersDF = spark.sql("SELECT name, age FROM people WHERE age BETWEEN 13 AND 19")
         teenagersDF.map(teenager => "Name: " + teenager(0)).show()


         teenagersDF.map(teenager => "Name: " + teenager.getAs[String]("name")).show()
         
         
         
         
     }


}
