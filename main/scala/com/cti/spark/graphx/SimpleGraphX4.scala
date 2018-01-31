package com.cti.spark.graphx

import org.apache.spark.{SparkConf, SparkContext}
import org.apache.spark.graphx.{GraphLoader, PartitionStrategy}

object SimpleGraphX4 {
    def main(args: Array[String]): Unit = {
        val conf = new SparkConf().setAppName("SimpleGraphXconnectedComponents").setMaster("local[4]")
        val sc = new SparkContext(conf)

        //加载edge为graph
        val graph = GraphLoader.edgeListFile(sc, "file:///home/tianlei/soft//spark/data/graphx/followers.txt",true).partitionBy(PartitionStrategy.RandomVertexCut)
        val triCounts = graph.triangleCount().vertices

        val users = sc.textFile("file:///home/tianlei/soft//spark/data/graphx/users.txt")
            .map {
                line =>
                    val fields = line.split(",")
                    (fields(0).toLong, fields(1))
            }
        val triCountByUsername = users.join(triCounts).map{
            case (id,(username ,tc))=> (username,tc)
        }
        println(triCountByUsername.collect().mkString("\n"))
    }

}
