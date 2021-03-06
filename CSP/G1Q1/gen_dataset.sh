#!/bin/bash

question=G1Q1

# source dir
src_dir=/data/aviation/air_carrier_statistics_ALL/t-100_domestic_market/*.zip


# HDFS dataset dir 
dataset_dir=/dataset_T1/${question}

hdfs dfs -test -d $dataset_dir
if [ $? == 0 ]; then
   echo "HDFS folder $dataset_dir exists, script continue ..."
   hdfs dfs -rm $dataset_dir/*
else
   echo "HDFS folder $dataset_dir does not exist, create the folder"
   hdfs dfs -mkdir $dataset_dir
fi

CURR_DIR=${PWD}
tmp_dir=/tmp/${question}
rm -r $tmp_dir
mkdir $tmp_dir
cp data_gen.py $tmp_dir 
cd $tmp_dir

n=0
for file in $src_dir
do
   let n=$n+1

   filename=$(basename "$file")
   year="${filename%.*}"
   #echo 'file to be processed '  $filename $year 

   unzip -p $file 349108460_T_T100D_MARKET_ALL_CARRIER_${year}_All.csv | ./data_gen.py > ${year}.txt

done

echo 'File processed:' $n
hdfs dfs -copyFromLocal ./*.txt $dataset_dir
hdfs dfs -ls $dataset_dir

hdfs dfs -test -d /T1/misc
if [ $? == 0 ]; then
	hadoop fs -rm -r /T1/misc
fi 
hadoop fs -mkdir -p /T1/misc
echo " \t,;.?!-:@[](){}_*/" > delimiters.txt
hadoop fs -copyFromLocal delimiters.txt /T1/misc

echo 'Files copied to HDFS, ready to run mapreduce.' 
cd $CURR_DIR
