package com.cti.kafka;

public class KafkaProperties {
    public static final String TOPIC = "test";
    public static final String ZK = "192.168.199.111:2181";
    public static final String BROKER_LIST = "192.168.199.111:9092";
    public static final String KAFKA_SERVER_URL = "192.168.112.185";
    public static final int KAFKA_SERVER_PORT = 9092;
    public static final int KAFKA_PRODUCER_BUFFER_SIZE = 64 * 1024;
    public static final int CONNECTION_TIMEOUT = 100000;
    public static final String TOPIC2 = "topic2";
    public static final String TOPIC3 = "topic3";
    public static final String CLIENT_ID = "SimpleConsumerDemoClient";

    private KafkaProperties() {
    }
}
