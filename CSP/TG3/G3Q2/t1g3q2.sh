#!/bin/bash
hdfs dfs -rm -r /output_T1/G3Q2 

pig  -Dpig.additional.jars=/usr/share/cassandra/*.jar:/usr/share/cassandra/lib/*.jar \
  -x mapreduce -param PIG_IN_DIR=/dataset_T1/G3Q2  -param PIG_OUT_DIR=/output_T1/G3Q2  -f bestroute.pig
