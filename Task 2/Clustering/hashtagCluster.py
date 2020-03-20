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
hashtagList = []
counter = 0

def camel_case_split(str): 
  
    return re.findall(r'[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', str) 
      
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
                for word in camel_case_split(current):
                    hashtagList.append(word)


except OSError as e:
    pass

# Vectorize the words
vectorizer = TfidfVectorizer(stop_words='english')
vectorized = vectorizer.fit_transform(hashtagList)

# KMeans 
model = KMeans(max_iter=12000, n_clusters = 8)
model.fit(vectorized)

# Print top terms for each cluster
print("Top terms per cluster:")
order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()

for i in range(8):
    print(i)
    for ind in order_centroids[i, :10]:
        print(terms[ind])
    print

print(counter)














