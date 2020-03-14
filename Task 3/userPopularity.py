import pymongo 
from pymongo import MongoClient 
import networkx as nx 

client = MongoClient('mongodb://localhost:27017')
db = client.coronaDatabase
tweets = db.tweets

popularity = {}
interactions = {}
counter = 0
# Determines if the tweet is a retweet, discards the tweet for mention analysis as tweet may have multiple mentions 
# as not an original tweet
def isRetweet(text):
   # for seperator in twitter_prefixes: 
      #  text = text.replace(seperator, ' ')
    if text[:2] != "RT":
        return False
    else: 
        return True
  

try: 
    for tweet in tweets.find():
        counter += 1
        if counter % 1000 == 0: 
          print(counter)
        # takes the tweet and extracts the relevent text from it, giving only message 
        if isRetweet(tweet['message']):
          next
        else: 
          if tweet['mentions']:
            for i in tweet['mentions']:
              #interactions[tweet['username']] = interactions[i['screen_name']]
              if i['screen_name'] in popularity:
                popularity[i['screen_name']] += 1
              else: 
                popularity[i['screen_name']] = 1

    # Sorted popularity gives twitter users that were mentioned the most at the end of the dictionary. 
    sortedPopularity = sorted(popularity.items(), key=lambda x: x[1], reverse = True) 

except OSError as e:
    pass

