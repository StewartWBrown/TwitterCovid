import pymongo
from pymongo import MongoClient
import json
import re 
import string
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score

client = MongoClient('mongodb://localhost:27017')
db = client.coronaDatabase
tweets = db.tweets

locationArray = {}
counter = 0

try: 
    for tweet in tweets.find():
        counter += 1
        if counter % 1000 == 0: 
          print(counter)
        
        if tweet['Country'] is not "No geo information":
                tweet_location = tweet['Country']
                if tweet_location in locationArray: 
                    locationArray[tweet_location] += 1
                else: 
                    locationArray[tweet_location] = 1

    # Sorted popularity gives twitter users that were mentioned the most at the end of the dictionary. 
    sortedLocations = sorted(locationArray.items(), key=lambda x: x[1], reverse = True) 
    
    for i in sortedLocations:
        print(i[0], i[1])



except OSError as e:
    pass

