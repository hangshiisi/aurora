

file = sc.textFile('hdfs://localhost:9000/user/sniper/departure_by_carriers/part-r-00000')
rdd = file.map(lambda line: line.split())
rdd2 = rdd.map(lambda tuple: (tuple[0], tuple[1], float(tuple[2])))
from pyspark.sql import Row
rdd3 = rdd2.map(lambda row: Row(airport=row[0], carrier=row[1], dep_delay=row[2]))
df = spark.createDataFrame(rdd3)
df.write\
    .format("org.apache.spark.sql.cassandra")\
    .mode('append')\
    .options(table="airport_carrier_departure", keyspace="aviation")\
    .save()


#./bin/pyspark --conf spark.cassandra.connection.host=127.0.0.1 --packages datastax:spark-cassandra-connector:2.0.0-RC1-s_2.11

# https://github.com/gitaroktato/cloud-capstone


#https://github.com/stephendimig/cc-capstone/blob/master/Group_2/group2_3.sh
import re
import io
import subprocess
proc = subprocess.Popen(['hadoop','fs', '-cat', '/user/root/output/pig/*'],stdout=subprocess.PIPE)

f = open('export.cql', 'w')
f.write("truncate mykeyspace.results3;\n")
for line in proc.stdout:
    match = re.search(r'(\S{3})\s*(\S{3})\s*(\S{2}|\S{2} [(]{1}[0-9]+[)]{1})\s*([\d.]+)', line)
    f.write("INSERT INTO mykeyspace.results3 (origin, dest, unique_carrier, arrival_delay_avg) VALUES('" + match.group(1) +  "', '" + match.group(2) + "', '" + match.group(3) + "', " + match.group(4) + ");\n")


#https://github.com/gmcorral/cloud-capstone/tree/master/spark
#https://github.com/alvatar/cloud-computing-capstone/blob/master/3-02-v2-traveler.sh




create keyspace aviation WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1 };
create table aviation.airport_carrier_departure (
  airport text,
  carrier text,
  dep_delay decimal,
  PRIMARY KEY(airport, dep_delay, carrier)
);
create table aviation.airport_airport_departure (
  airport text,
  airport_to text,
  dep_delay decimal,
  PRIMARY KEY(airport, dep_delay, airport_to)
);
create table aviation.airport_airport_arrival (
  airport text,
  airport_to text,
  arr_delay decimal,
  PRIMARY KEY(airport, airport_to)
);
create table aviation.best_flights_2008 (
  airport_from text,
  airport_to text,
  given_date date,
  am_or_pm text,
  carrier text,
  flight_num text,
  departure_time text,
  arr_delay decimal,
  PRIMARY KEY(airport_from, airport_to, given_date, am_or_pm)
);