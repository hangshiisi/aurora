from pyspark import SparkContext
from pyspark import SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from pyspark.sql import SQLContext, Row

import sys
import time
import signal 

config = SparkConf()
config.set("spark.streaming.stopGracefullyOnShutdown", "true") 
	
filtered = None 
ssc = None 

def close_handler(signal, frame): 
	print('Closing down, print out result ')
	try: 
		if filtered: 
			filtered.foreachRDD(lambda rdd: print_rdd(rdd))
		if ssc: 
			ssc.stop(true, true)
	except: 
		pass 	
	sys.exit(0)	 

def getSqlContextInstance(sparkContext):
    if ('sqlContextSingletonInstance' not in globals()):
        globals()['sqlContextSingletonInstance'] = SQLContext(sparkContext)
    return globals()['sqlContextSingletonInstance']
    


config.set('spark.streaming.stopGracefullyOnShutdown', True)

#sc = SparkContext(appName='g1ex1', conf=config, pyFiles=['flight.py'])
signal.signal(signal.SIGINT, close_handler)


sc = SparkContext(appName='g1ex1', conf=config)
ssc = StreamingContext(sc, 10)
ssc.checkpoint('file:///tmp/g1ex1')

#lines = ssc.socketTextStream(sys.argv[1], int(sys.argv[2]))

zkQuorum, topic = sys.argv[1:]
kvs = KafkaUtils.createStream(ssc, zkQuorum, "spark-streaming-consumer", {topic: 1})
lines = kvs.map(lambda x: x[1])

def process(time, rdd):
    print("========= %s =========" % str(time))
    try:
        # Get the singleton instance of SQLContext
        sqlContext = getSqlContextInstance(rdd.context)
        # Convert RDD[String] to RDD[Row] to DataFrame
        parts = rdd.map(lambda line: line.split("\t"))
        delays= parts.map(lambda w: Row(carrier=w[0], delay=float(w[7])))
        dataFrame = sqlContext.createDataFrame(delays)
        # Register as table
        dataFrame.registerTempTable("carrier_delays")
        # Do word count on table using SQL and print it
        carrier_delays_df = \
                sqlContext.sql("SELECT carrier, avg(delay) AS avg_delay FROM carrier_delays GROUP BY carrier ORDER BY avg_delay ASC LIMIT 10")
        carrier_delays_df.show()
    except Exception as e: print (e)

lines.foreachRDD(process)

# start streaming process
ssc.start()

try:
    ssc.awaitTermination()
except:
    pass

try:
    time.sleep(10)
except:
    pass
    