from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import operator
import numpy as np
import json
#import matplotlib.pyplot as plt
import sys
from operator import methodcaller
import random
import pyspark_cassandra
import pyspark_cassandra.streaming
from uuid import uuid1
from pyspark_cassandra import CassandraSparkContext

from pyspark.sql import SQLContext

reload(sys)
sys.setdefaultencoding('utf-8')
def load_wordlist(filename):
    """ 
    This function returns a list or set of words from the given filename.
    """
    words = {}
    f = open(filename, 'rU')
    text = f.read()
    text = text.split('\n')
    for line in text:
        words[line] = 1
    f.close()
    return words

def main():
    tickerSymbols = load_wordlist("../Dataset/tickerSymbols.txt")


    conf = SparkConf().\
    setMaster("local[2]").\
    setAppName("StockStreamer").\
    set("spark.cassandra.connection.host",\
    "52.25.173.31, 35.165.251.179, 52.27.187.234, 52.38.246.84")

    #conf = SparkConf().setMaster("local[2]").setAppName("Streamer")
    sc = SparkContext(conf=conf)
    sc.setLogLevel("WARN")
    # Creating a streaming context with batch interval of 1 sec
    ssc = StreamingContext(sc, 10)
    ssc.checkpoint("checkpoint")
    kstream = KafkaUtils.createDirectStream(\
    ssc, topics = ['stock-topic1'], kafkaParams = {"metadata.broker.list": 'localhost:9092'})
    stock = kstream.map(lambda (key, value): json.loads(value))
    stock.pprint()
    stock.saveToCassandra("tweetdb","stocktable")
    #value = stock.map(lambda stock1: stock1[u'bidaskvalvol'])
    #value.pprint()
    #text_counts = stock.map(lambda stockQ: (stockQ['bidaskvalvol'],1)).reduceByKey(lambda x,y: x + y)

    #text_counts.pprint()

    # Start the computation
    ssc.start()
    ssc.awaitTerminationOrTimeout(10000)
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
    #stock = kstream.map(lambda (key, value): json.loads(value))
    stock = kstream.map(lambda x: json.loads(x[1]))
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
