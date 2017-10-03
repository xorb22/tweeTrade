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
#print(len(tickerSymbols))
#sys.exit()


while 1:
	# producer.send('foobar', b'some_message_bytes')
        val = random.random()*5+100
	stockQuote = np.random.rand(len(tickerSymbols),4)
	#print(stockQuote)
	#sys.exit()
        #jsonStock = ''
	#jsonStock =json.dumps({'insertion_time':datetime.datetime.now().strftime("%Y-%m-%d")})+'\n'+json.dumps({'insertion_time':datetime.datetime.now().strftime("%Y-%m-%d")})
        insert_time =datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	for counter, ticker in enumerate(tickerSymbols):
		timeMain = int(time.time());
		stockVal = 100. * np.exp((timeMain % 130)/100.) + 30*np.random.rand()
		#stockVal = 100+20*np.sin(2*3.14/20*timeMain)+3*np.random.rand()
		#if (timeMain % 100)
		
		jsonStock = json.dumps({'insertion_time':insert_time\
		      ,'ticker':ticker,\
			'value': [stockVal, stockVal, stockVal, stockVal]})
		producer.send('stock-topic1',jsonStock)
	#jsonStock = remove_last_line_from_string(jsonStock)
	#print jsonStock
	#sys.exit()
	#dic = dict(zip(tickerSymbols,stockQuote.tolist()))
        #dic['date'] = datetime.datetime.now().strftime("%m-%d-%Y")
	#dic['time'] = datetime.datetime.now().strftime("%H:%M:%S")
	#json_string = json.dumps(dic)
	#producer.send('stock-topic1',jsonStock)
	time.sleep(samplingRate)
#f.close()  # you can omit in most cases as the destructor will call it
