from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import operator
import numpy as np
import json
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

#import matplotlib.pyplot as plt

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

def tweetwithSentiment(tweet,pwords, nwords):
    
    text = tweet.get(u'text')
    if text is not None:
         words = text.split(" ")
         sentiment = np.sign(sum([(1 if word in pwords else -1 if word in nwords else 0)  for word in words]))
         print(type(tweet))
         tweet["sentiment"]=sentiment
         return (tweet)
    return 0

def main():
    pwords = load_wordlist("./Dataset/positive.txt")
    nwords = load_wordlist("./Dataset/negative.txt")

    conf = SparkConf().setMaster("local[2]").setAppName("TweeStreamer")
    sc = SparkContext(conf=conf)
    sc.setLogLevel("WARN")
    # Creating a streaming context with batch interval of 1 sec
    ssc = StreamingContext(sc, 10)
    ssc.checkpoint("checkpoint")

    kstream = KafkaUtils.createDirectStream(
    ssc, topics = ['twitter-topic1'],
    kafkaParams = {"metadata.broker.list": 'localhost:9092'})
   
    
    #tweets = kstream.map(lambda x: json.loads( x[1].decode('utf-8')))
    tweets = kstream.map(lambda x: json.loads( x[1]))
    tweetsUsentiment = tweets.map(lambda tweet: tweetwithSentiment(tweet, pwords, nwords))
    tweetsUsentiment.pprint()
   
    #tweetsUsentiment.saveToCassandra("killranalytics", "real_time_data") 
 
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

if __name__=="__main__":
    main()
