from tweepy.streaming import StreamListener 
from tweepy import OAuthHandler 
from tweepy import Stream 
import json
import pymongo
from pymongo import MongoClient


import credentials

# Connect to mongodb and create database
client = MongoClient('mongodb://localhost:27017')
db = client.coronaDatabase
tweets = db.tweets

errorCounter = 0

#override tweepy.streamListener to add logic to on_status 
class MyStreamListener(StreamListener):
    def on_connect(self): 
       print("Now connected to Twitter Streaming API")
       

    # When status recieved, take variables that are cared about and put them into table
    def on_data(self, status):
        status = json.loads(status)


        try:
            tweet_id = status['id_str']
            tweet_date = status['created_at']
            author_name = status['user']['screen_name']
            author_bio = status['user']['description']

 
            if status['place'] is not None:
                tweet_location = status['place']['country']
            else: 
                tweet_location = "No geo information"

            if status['truncated'] == True:
                tweet_message = status['extended_tweet']['full_text']
                tweet_hashtags = status['extended_tweet']['entities']['hashtags']
                user_mentions = status['extended_tweet']['entities']['user_mentions']

            else:
                tweet_message = status['text']
                tweet_hashtags = status['entities']['hashtags']
                user_mentions = status['entities']['user_mentions']


            tweet = {
                'message' : tweet_message,
                '_id' : tweet_id,
                'date' : tweet_date,
                'Username' : author_name,
                'bio' : author_bio,
                'Country': tweet_location,
                'Hashtags' : tweet_hashtags,
                'mentions': user_mentions                
            }

            # Instert tweet into table
            tweets.insert_one(tweet)
            print(errorCounter)
            print(tweet_message)
            
        except Exception as e: 
            
            print(e)

# Print out error if error occurs
    def on_error(self, status):
        errorCounter = errorCounter +1
        print(status)



if __name__ == "__main__":

    # Start stream listener 
    myStreamListener = MyStreamListener()
    auth = OAuthHandler(credentials.CONSUMER_KEY, credentials.CONSUMER_SECRET)
    auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)

    myStream = Stream(auth, myStreamListener)

    #Pick what words to be filtered
    myStream.filter(track=['Corona', 'coronavirus', 'Borris', 'schools', 'pandemic', 'covid19', 'outbreak'])
    