package com.cti.spark.graphx

import org.apache.spark.{SparkConf, SparkContext}
import org.apache.spark.graphx.GraphLoader

object SimpleGraphX2 {
    def main(args: Array[String]): Unit = {
        val conf = new SparkConf().setAppName("SimpleGraphXpagerunk").setMaster("local[4]")
        val sc = new SparkContext(conf)

        //加载edge为graph
        val graph = GraphLoader.edgeListFile(sc, "file:///home/tianlei/soft//spark/data/graphx/followers.txt")
//        运行Run PageRank
        val ranks = graph.pageRank(0.0001).vertices

        //// Join the ranks with the usernames
        val users = sc.textFile("file:///home/tianlei/soft//spark/data/graphx/users.txt")
            .map{
                line =>
                    val fields = line.split(",")
                    (fields(0).toLong ,fields(1))
            }

        val runksByusername = users.join(ranks).map{
            case (id ,(username,rank)) => (username,rank)
        }
        println(runksByusername.collect().mkString("\n"))

    }

}
