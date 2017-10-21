#!/bin/bash
hadoop fs -rm -r /output_T1/G1Q1

#hadoop jar TopAirports.jar TopAirports -D delimiters=/T1/misc/delimiters.txt -D N=10 /dataset_T1/G1Q1 /output_T1/G1Q1


hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.8.1.jar \
    -mapper mapper.py \
    -reducer topN.py \
    -input  /dataset_T1/G1Q1 \
    -output /output_T1/topN \
    -file mapper.py \
    -file topN.py

