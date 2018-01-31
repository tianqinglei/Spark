//package com.cti.neo4j;
//
//import org.neo4j.graphdb.*;
//import org.neo4j.graphdb.factory.GraphDatabaseFactory;
//import org.neo4j.kernel.api.proc.Neo4jTypes;
//
//import java.io.File;
//
//public class GraphDatabase {
//    private  static  final File DB_PATH = new File("file:///home/tianlei/Neo4jDB");
//    private static GraphDatabaseService graphDb;
//
//
//    private static void registerShutdownHook(final GraphDatabaseService graphDb){
//        Runtime.getRuntime().addShutdownHook(new Thread(){
//            @Override
//            public void run() {
//                graphDb.shutdown();
//            }
//        });
//    }
////    图数据库是一个有向图，由通过关系Relationships连接的节点Nodes构成，节点和关系可以有自己的属性Properties。
////    关系的类型可以通过枚举enum创建（Label也可以）：
//    public static enum RelTypes implements RelationshipType {
//        RELEASED;
//
//    }
//    private static void addData(){
//        Node node1;
//        Node node2;
//        Label label1;
//        Label label2;
//        Relationship relationship;
//
//
//        try (Transaction tx = graphDb.beginTx()) {
//            //创建标签
//            label1 = Label.label( "Musician");
//            label2 = Label.label( "Album");
//            //创建结点
//            node1 = graphDb.createNode(label1);
//            node1.setProperty("name","xiaoming");
//            node2 = graphDb.createNode(label2);
//            node2.setProperty("name","xiaohong");
//
//            //创建关系及属性
//            relationship = node1.createRelationshipTo(node2,RelTypes.RELEASED);
//            relationship.setProperty("date","2018-01-10");
//            //输出结果
//            System.out.println("created node name is " + node1.getProperty("name"));
//           System.out.println(relationship.getProperty("date"));
//            System.out.println("created node name is " + node2.getProperty("name"));
//           //提交事务
//            tx.success();
//
//        }
//        graphDb.shutdown();
//
//    }
//    private static void queryAndUpdate(){
//        try (Transaction tx = graphDb.beginTx()){
//            //查询节点
//            Label label = Label.label("Musician");
//            Node node = graphDb.findNode(label, "name", "xiaoming");
//            System.out.println("query node name is " + node.getProperty("name"));
//            node.setProperty("birthday","2011-12-14");
//            System.out.println(node.getProperties("name") + "'s birthday is " + node.getProperty("birthday", new String()));
//            tx.success();
//
//
//        }
//        graphDb.shutdown();
//    }
//
//    public static void main(String[] args) {
//        graphDb = new GraphDatabaseFactory().newEmbeddedDatabase(DB_PATH);
//         registerShutdownHook(graphDb);
//                 addData();
//                // queryAndUpdate();
//               // delete();
//    }
//}
