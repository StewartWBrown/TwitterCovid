import pymongo
from pymongo import MongoClient
import json

import numpy as np


client = MongoClient('mongodb://localhost:27017')
db = client.coronaDatabase
tweets = db.tweets


tweetArray = []
string_data = []
counter = 0

UKCounter = 0
USACounter = 0
brasilCounter = 0
franceCounter = 0
canadaCounter = 0

try: 
    for tweet in tweets.find():
        if tweet['Country'] == "United Kingdom":
            UKCounter += 1
        elif tweet['Country'] == "United States":
            USACounter += 1
        elif tweet['Country'] == "Brasil":
            brasilCounter += 1
        elif tweet['Country'] == 'France':
            franceCounter += 1
        elif tweet['Country'] == "Canada":
            canadaCounter += 1
        elif tweet['Country'] != "No geo information":
            print(tweet['Country'])
except OSError as e:
    pass


