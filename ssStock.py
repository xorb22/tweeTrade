from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import operator
import numpy as np
import json
#import matplotlib.pyplot as plt


def main():
    conf = SparkConf().setMaster("local[2]").setAppName("Streamer")
    sc = SparkContext(conf=conf)
    sc.setLogLevel("WARN")
    # Creating a streaming context with batch interval of 1 sec
    ssc = StreamingContext(sc, 1)
    ssc.checkpoint("checkpoint")
    kstream = KafkaUtils.createDirectStream(
    ssc, topics = ['stocktopic'], kafkaParams = {"metadata.broker.list": 'localhost:9092'})
    stock = kstream.map(lambda (key, value): json.loads(value))
    #stock.pprint()
    value = stock.map(lambda stock1: stock1[u'bidaskvalvol'])
    value.pprint()
    #text_counts = stock.map(lambda stockQ: (stockQ['bidaskvalvol'],1)).reduceByKey(lambda x,y: x + y)

    #text_counts.pprint()

    # Start the computation
    ssc.start()
    ssc.awaitTerminationOrTimeout(100)
    ssc.stop(stopGraceFully = True)

    

def updateFunction(newValues, runningCount):
    if runningCount is None:
       runningCount = 0
    return sum(newValues, runningCount) 


def sendRecord(record):
    connection = createNewConnection()
    connection.send(record)
    connection.close()


def stream(ssc, duration):
    kstream = KafkaUtils.createDirectStream(
    ssc, topics = ['stocktopic'], kafkaParams = {"metadata.broker.list": 'localhost:9092'})
    stock = kstream.map(lambda (key, value): json.loads(value))
    stock.pprint()

    text_counts = stock.map(lambda stockQ: (stockQ['bidaskvalvol'],1)).reduceByKey(lambda x,y: x + y)
    
    text_counts.pprint()
        
    # Start the computation
    ssc.start() 
    ssc.awaitTerminationOrTimeout(duration)
    ssc.stop(stopGraceFully = True)

    return 0


if __name__=="__main__":
    main()
