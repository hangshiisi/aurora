#!/bin/bash
hadoop fs -rm -r /output_T1/G1Q1

#hadoop jar TopAirports.jar TopAirports -D delimiters=/T1/misc/delimiters.txt -D N=10 /dataset_T1/G1Q1 /output_T1/G1Q1


hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.8.1.jar \
    -mapper mapper.py \
    -reducer reducer.py \
    -input  /dataset_T1/G1Q1 \
    -output /output_T1/G1Q1 \
    -file mapper.py \
    -file reducer.py

