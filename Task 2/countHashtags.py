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

hashtagDict = {}
counter = 0



try: 
    for tweet in tweets.find():
        counter += 1
        if counter % 1000 == 0: 
          print(counter)
        
        for i in tweet['Hashtags']:
            current = i['text']

            if current in hashtagDict: 
                hashtagDict[current] += 1
            else: 
                hashtagDict[current] = 1

    # Sorted popularity gives twitter users that were mentioned the most at the end of the dictionary. 
    sortedHashtags = sorted(hashtagDict.items(), key=lambda x: x[1], reverse = False) 
    
    for i in sortedHashtags:
        print(i[0], i[1])
    
except OSError as e:
    pass

