#!/usr/bin/env python 

from cassandra.cluster import Cluster
from pyspark.sql import SparkSession
from pyspark.sql.types import StringType
from pyspark import SQLContext


#cluster = Cluster()
#session = cluster.connect() 


spark = SparkSession \
    .builder \
    .appName("Python Spark SQL basic example") \
    .config("spark.some.config.option", "some-value") \
    .getOrCreate()

spark.read\
    .format("org.apache.spark.sql.cassandra")\
    .options(table="kv", keyspace="test")\
    .load().show()

# write something 
#test_data = spark.read.csv("f.csv", header=False) 
test_data = spark.sparkContext.textFile("f.csv").map(\
                    lambda l: l.strip().split(",")) 
test_df = test_data.toDF(['k','v']) 

test_df.show() 

#insert into cassandra 
test_df.write\
    .format("org.apache.spark.sql.cassandra")\
    .mode('append')\
    .options(table="kv", keyspace="test")\
    .save()


#verify the results 
copy_df = spark.read\
    .format("org.apache.spark.sql.cassandra")\
    .options(table="kv", keyspace="test")\
    .load()

copy_df.show()

# need to have a way to create the table first 
# either from cqlsh or codes 

copy_df.write\
    .format("org.apache.spark.sql.cassandra")\
    .mode('overwrite')\
    .options(table="kv_copy", keyspace="test")\
    .save()

print("after copying ")
spark.read\
    .format("org.apache.spark.sql.cassandra")\
    .options(table="kv_copy", keyspace="test")\
    .load().show()
