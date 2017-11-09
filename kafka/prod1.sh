#!/usr/bin/env bash

topic="test"
brokerip="localhost:9092"

for i in `find /data/G2/*`; do
     echo $i 
#    cat $i | \
#    /home/aurora/NJ/kafka/bin/kafka-console-producer.sh \
#    --broker-list $brokerip --topic $topic
    #sleep 1
done

