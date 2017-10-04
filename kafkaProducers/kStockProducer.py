/* This python script synthesizes and creates a Kafka producer at the Kafka service that
is already running in a local server.
*/
import datetime
import time
import json
import random
from kafka import KafkaProducer
import numpy as np
import sys

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

def remove_last_line_from_string(s):
    return s[:s.rfind('\n')]

producer = KafkaProducer(bootstrap_servers='localhost:9092')
tickerSymbols = load_wordlist("../Dataset/tickerSymbols.txt")
samplingRate = 5

while 1:
        val = random.random()*5+100
	stockQuote = np.random.rand(len(tickerSymbols),4)
        insert_time =datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	for counter, ticker in enumerate(tickerSymbols):
		timeMain = int(time.time());
		stockVal = 100. * np.exp((timeMain % 130)/100.) + 30*np.random.rand()		
		jsonStock = json.dumps({'insertion_time':insert_time\
		      ,'ticker':ticker,\
			'value': [stockVal, stockVal, stockVal, stockVal]})
		producer.send('stock-topic1',jsonStock)
	time.sleep(samplingRate)
