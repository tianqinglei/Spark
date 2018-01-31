//package com.cti.neo4j;
//
//import org.neo4j.cypher.internal.compiler.v2_3.planDescription.InternalPlanDescription;
//import org.neo4j.cypher.internal.javacompat.ExecutionEngine;
//import org.neo4j.cypher.javacompat.ExecutionEngine;
//import org.neo4j.cypher.javacompat.ExecutionResult;
//import org.neo4j.graphdb.Direction;
//import org.neo4j.graphdb.GraphDatabaseService;
//import org.neo4j.graphdb.Node;
//import org.neo4j.graphdb.NotInTransactionException;
//import org.neo4j.graphdb.Relationship;
//import org.neo4j.graphdb.RelationshipType;
//import org.neo4j.graphdb.ReturnableEvaluator;
//import org.neo4j.graphdb.StopEvaluator;
//import org.neo4j.graphdb.Transaction;
//import org.neo4j.graphdb.Traverser.Order;
//import org.neo4j.graphdb.factory.GraphDatabaseFactory;
//import org.neo4j.graphdb.index.Index;
//import org.neo4j.graphdb.traversal.Traverser;
//import org.neo4j.unsafe.impl.batchimport.cache.idmapping.string.RadixCalculator;
//
//import java.util.Arrays;
//import java.util.HashMap;
//import java.util.Map;
//
//public class GraphDatabase2 {
//    private  static GraphDatabaseService graphdb;
//    private static Relationship relationship;
//    private static Index<Node> nodeIndex;
//
//    public enum RelTypes implements RelationshipType {
//        USERS_REFERENCE,
//        USER,
//        KNOWS
//    }
//
//    private static void registerShuntdownHOOK  (final GraphDatabaseService graphdb){
//        Runtime.getRuntime().addShutdownHook(new Thread() {
//            @Override
//            public void run() {
//                graphDb.shutdown();
//            }
//        });
//    }
//
//    public static void main(RadixCalculator.String[] args) {
//        graphdb = new GraphDatabaseFactory().newEmbeddedDatabase(new java.io.File("db"));
//        nodeIndex = graphdb.index().forNodes("nodex");
//        Transaction tx = graphdb.beginTx();
//        try {
//            // neo4j statement
//            tx.success();
//            System.out.println("successfully");
//        } finally {
//            tx.finish();
//        }
//        //cyper statement
//        ExecutionEngine engine = new ExecutionEngine(graphdb);
//        Map<String, Object> params = new HashMap<String, Object>();
//        params.put("id", Arrays.asList(1, 2));
//        ExecutionResult result = engine.execute("xxx");
//
//        System.out.println(result);
//
//        List<String> columns = result.columns();
//        System.out.println(columns);
//
//        //***************************************************
//        registerShutdownHook(graphdb);
//
//    }
//
//}
