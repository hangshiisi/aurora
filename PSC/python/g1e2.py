from pyspark import SparkContext
from pyspark import SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

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

def print_rdd(rdd):
    print('==========XYZ S===================')
    #airlines = rdd.takeOrdered(10, key = lambda x: -x[1][0]/airline[1][1])
    airlines = rdd.takeOrdered(10, key = lambda (x,y): -y[1]/y[0])
 
    for airline in airlines:
        print("%s, %f,%d" % (airline[0], \
               airline[1][0]/airline[1][1], airline[1][1]))
    print('==========XYZ E===================')


config.set('spark.streaming.stopGracefullyOnShutdown', True)

#sc = SparkContext(appName='g1ex1', conf=config, pyFiles=['flight.py'])
signal.signal(signal.SIGINT, close_handler)


sc = SparkContext(appName='g1ex2', conf=config)
ssc = StreamingContext(sc, 10)
ssc.checkpoint('file:///tmp/g1ex2')

zkQuorum, topic = sys.argv[1:]
kvs = KafkaUtils.createStream(ssc, zkQuorum, "spark-streaming-consumer", {topic: 1})
lines = kvs.map(lambda x: x[1])

def updateFunction(newValues, runningCount):
    if runningCount is None: 
        runningCount = (0., 0)
    
    values, counter = runningCount 
    for val in newValues: 
        values += val[0]
        counter += val[1]

    return (values, counter) 

filtered = lines.map(lambda line: line.split("\t"))\
        		.map(lambda word: (word[0]+" " + word[1], (float(word[7]), 1)) )\
        		.updateStateByKey(updateFunction)
                
filtered.foreachRDD(lambda rdd: print_rdd(rdd))

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
    