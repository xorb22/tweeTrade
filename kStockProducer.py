import datetime
import time
import json
import random
from kafka import KafkaProducer
producer = KafkaProducer(bootstrap_servers='localhost:9092')

while 1:
	# producer.send('foobar', b'some_message_bytes')
        val = random.random()*5+100
	dic={'date': datetime.datetime.now().strftime("%m-%d-%Y"), 'time': datetime.datetime.now().strftime("%H:%M:%S"),'ticker':'INSI', 'bidaskvalvol': [val, val, val,int(round(random.random()*1000))]}
	json_string = json.dumps(dic)
	producer.send('stock-topic',json_string)
	time.sleep(1)
#f.close()  # you can omit in most cases as the destructor will call it
