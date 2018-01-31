package com.cti.kafka;

public class KafkaTrain {
    public static void main(String[] args) {
        boolean isAsync = args.length == 0 || !args[0].trim().equalsIgnoreCase("sync");
        Producer producerThread = new Producer(KafkaProperties.TOPIC, isAsync);
        producerThread.start();


        Consumer consumerThread = new Consumer(KafkaProperties.TOPIC);
        consumerThread.start();


    }
}
