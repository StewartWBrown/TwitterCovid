import pymongo
from pymongo import MongoClient
import json

import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score

client = MongoClient('mongodb://localhost:27017')
db = client.coronaDatabase
tweets = db.tweets

tweetArray = []
string_data = []
counter = 0

'''
try: 
    for tweet in tweets.find().limit(1000):
        counter += 1
        print(tweet['message'])
        print(counter)
        tweetArray.append(tweet['message'])
        sentence = tweet['message'].strip().split(' ')
        for word in sentence:
            if word not in stop_words:
                print("not in")
                word = word.lower()
                string_data.append(word)
            else:
                print("in")

'''

try: 
    for tweet in tweets.find().limit(1000):
        counter += 1
        print(tweet['message'])
        print(counter)
        tweetArray.append(tweet['message'])


except OSError as e:
    pass

vectorizer = TfidfVectorizer(stop_words='english')
vectorized = vectorizer.fit_transform(tweetArray)


model = KMeans(max_iter=2000)
model.fit(vectorized)

print("Top terms per cluster:")
order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()
for i in range(8):
    print(i)
    for ind in order_centroids[i, :10]:
        print(terms[ind])
    print

print(counter)


