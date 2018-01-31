//package com.cti.spark.graphx
//
//import org.apache.log4j.{Level, Logger}
//import org.apache.spark.rdd.RDD
//import org.apache.spark.{SparkConf, SparkContext}
//import org.apache.spark.graphx._
//object SimpleGraphX {
//    def main(args: Array[String]): Unit = {
////        ////屏蔽日志
////        Logger.getLogger("org.apache.spark").setLevel(Level.WARN)
////        Logger.getLogger("org.eclipse.jetty.server").setLevel(Level.OFF)
//        //设置运行环境
//        val conf = new SparkConf().setAppName("SimpleSparkGraphX").setAppName("local[4]")
//        val sc = new SparkContext(conf)
//
//        //设置users顶点
//        val users: RDD[(VertexId, (String, String))] =
//            sc.parallelize(Array((3L, ("rxin", "student")), (7L, ("jgonzal", "postdoc")), (5L, ("franklin", "prof")), (2L, ("istoica", "prof"))))
//        //设置relationship
//        val relationships: RDD[Edge[String]] =
//            sc.parallelize(Array(Edge(3L, 7L, "collab"), Edge(5L, 3L, "advisor"), Edge(2L, 5L, "colleague"), Edge(5L, 7L, "pi")))
//        //定义默认的作者
//        val defaultUser = ("John","Missing")
//        //初始化Graph
//        val graph = Graph(users,relationships,defaultUser)
//
//        //展示图的属性
//        println("展示图的属性")
//        println("找到图中属性是student的顶点")
//        graph.vertices.filter{case (id ,(name,occupation)) =>occupation =="student"}.collect().foreach{
//            case (id,(name ,occupation)) =>println(s"$name is $occupation")
//        }
//
//        println(".............................")
//        println("找到图中边属性是advisor的边")
//        graph.edges.filter(e =>e.attr =="advisor").collect().foreach(
//            e => println(s"${e.srcId} to ${e.dstId} att ${e.attr}"))
//        )
//
//        println("---------------------------------------------")
//        println("找出图中最大的出度、入度、度数：")
//        def max (a:(VertexId,Int) , b : (VertexId,Int)):(VertexId,Int) = {
//
//            if (a._2 > b._2) a else b
//        }
//
//        println("max of outDegrees:" + graph.outDegrees.reduce(max) +
//            " max of inDegrees:" + graph.inDegrees.reduce(max) + " max of Degrees:" + graph.degrees.reduce(max))
//
//
//
//
//
//    }
//
//}
