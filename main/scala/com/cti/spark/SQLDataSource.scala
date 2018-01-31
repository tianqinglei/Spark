package com.cti.spark

import org.apache.spark.SparkConf
import org.apache.spark.sql.SparkSession

object SQLDataSource {

    case class Person(name: String, age: Long)




    def main(args: Array[String]): Unit = {
            val conf = new SparkConf()
            conf.setAppName("SQLDataSource")
            conf.setMaster("local[5]")

            val spark = SparkSession.builder().config(conf).getOrCreate()

            import spark.implicits._
            //runBasicDataSource(spark)
            // runBasicParquet(spark)
       // runParquetSchemaMerging(spark)
        runJsonDataset(spark)

            spark.stop()
        }

     def runBasicDataSource(spark: SparkSession):Unit = {
        val usersDF = spark.read.load("file:///home/tianlei/soft/spark/examples/src/main/resources/users.parquet")
       usersDF.select("name","favorite_color)").write.save("file:///home/tianlei/namesAndFavColors.parquet")
        val peopleDF = spark.read.format("json").load("file:///home/tianlei/soft/spark/examples/src/main/resources/people.json")
         peopleDF.select("name", "age").write.format("parquet").save("file:///home/tianlei/namesAndAges.parquet")

         val peopleDFCsv = spark.read.format("csv")
             .option("sep", ";")
             .option("inferSchema", "true")
             .option("header", "true")
             .load("file:///home/tianlei/soft/spark/examples/src/main/resources/people.csv")
         peopleDF.write.bucketBy(42, "name").sortBy("age").saveAsTable("people_bucketed")
         usersDF.write.partitionBy("favorite_color").format("parquet").save("namesPartByColor.parquet")

         usersDF
             .write
             .partitionBy("favorite_color")
             .bucketBy(42, "name")
             .saveAsTable("users_partitioned_bucketed")
         spark.sql("DROP TABLE IF EXISTS people_bucketed")
         spark.sql("DROP TABLE IF EXISTS users_partitioned_bucketed")
   }

    def runBasicParquet(spark: SparkSession):Unit = {
        import spark.implicits._
        val peopleDF = spark.read.json("file:///home/tianlei/soft/spark/examples/src/main/resources/people.json")
        //DataFrame可以保存为parquetwen文件，包括schema信息
        peopleDF.write.parquet("file:///home/tianlei/people.parquet")
        //阅读上面的parque文件
        val parquetFileDF = spark.read.parquet("file:///home/tianlei/people.parquet")
        parquetFileDF.createOrReplaceTempView("parquetFile")
        val namesDF = spark.sql("SELECT name FROM parquetFile WHERE age BETWEEN 13 AND 19")
        namesDF.map(attributes => "Name: " + attributes(0)).show()


    }

    def runParquetSchemaMerging(spark: SparkSession) :Unit= {
        import spark.implicits._
        val squaresDF = spark.sparkContext.makeRDD(1 to 5).map(i => (i, i * i)).toDF("value", "square")
        squaresDF.write.parquet("file:///home/tianlei/data/test_table/key=1")
        val cubesDF = spark.sparkContext.makeRDD(6 to 10).map(i => (i, i * i * i)).toDF("value", "cube")
        cubesDF.write.parquet("file:///home/tianlei/data/test_table/key=2")
        val mergedDF = spark.read.option("mergeSchame","true").parquet("file:///home/tianlei/data/test_table")
        mergedDF.printSchema()

    }

    def runJsonDataset(spark: SparkSession):Unit = {
        import spark.implicits._
        val path = "file:///home/tianlei/soft/spark/examples/src/main/resources/people.json"
        val peopleDF = spark.read.json(path)
        peopleDF.printSchema()
        peopleDF.createOrReplaceTempView("people")
        val teenagerNamesDF = spark.sql("SELECT name FROM people WHERE age BETWEEN 13 AND 19")
        teenagerNamesDF.show()


    }


}
