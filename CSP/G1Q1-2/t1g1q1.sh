#!/bin/bash
hadoop fs -rm -r /output_T1/G1Q1-2

hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.8.1.jar \
    -mapper mapper.py \
    -reducer reducer.py \
    -input  /dataset_T1/G1Q1-2 \
    -output /output_T1/G1Q1 \
    -file mapper.py \
    -file reducer.py

