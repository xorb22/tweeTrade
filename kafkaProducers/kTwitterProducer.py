'''
This script connect to twitter stream API and ingests stream data in topic of Kafka producer
'''
#!/usr/bin/env python
# import required libraries
from kafka import SimpleProducer, KafkaClient
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from twitter_config import consumer_key, consumer_secret, access_token, access_token_secret

# Kafka settings
topic = b'twitter-topic1'

# setting up Kafka producer
kafka = KafkaClient('localhost:9092')
producer = SimpleProducer(kafka)


#This is a basic listener that just put received tweets to kafka cluster.
class StdOutListener(StreamListener):
    def on_data(self, data):
        producer.send_messages(topic, data.encode('utf-8'))
        #print data
        return True

    def on_error(self, status):
        print status

if __name__ == '__main__':
    print 'running the twitter-stream python code'
    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    # Goal is to keep this process always going
    while True:
        try:
            stream.sample()
        except:
            pass
