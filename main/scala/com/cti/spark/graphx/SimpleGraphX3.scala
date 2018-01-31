package com.cti.spark.graphx

import org.apache.spark.graphx.GraphLoader
import org.apache.spark.{SparkConf, SparkContext}
import org.apache.spark.graphx.GraphLoader

object SimpleGraphX3 {
    def main(args: Array[String]): Unit = {
        val conf = new SparkConf().setAppName("SimpleGraphXconnectedComponents").setMaster("local[4]")
        val sc = new SparkContext(conf)

        //加载edge为graph
        val graph = GraphLoader.edgeListFile(sc, "file:///home/tianlei/soft//spark/data/graphx/followers.txt")
        // Find the connected components

        val cc = graph.connectedComponents().vertices


        //// Join the connected components with the usernames
        val users = sc.textFile("file:///home/tianlei/soft//spark/data/graphx/users.txt")
            .map {
                line =>
                    val fields = line.split(",")
                    (fields(0).toLong, fields(1))
            }
        val ccByUsername = users.join(cc).map{
            case (id,(username,cc)) =>(username , cc)
        }
        println(ccByUsername.collect().mkString("\n"))

    }

}
