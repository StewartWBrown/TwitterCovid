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

tweetArray = []
string_data = []
counter = 0

# Function to remove links from a string of text using regular expression package
def removeLinks(text): 
    link_struct = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
    linksInTweet = re.findall(link_struct, text)

    for link in linksInTweet :
        text = text.replace(link[0], '')
    return text

# Function to remove common twitter entities which are not wanted: @, # and RT from a string
def removeEntities(text):
    twitter_prefixes = ['@', '#']
   # for seperator in twitter_prefixes: 
      #  text = text.replace(seperator, ' ')
    realWords = []
    for word in text.split():
        word = word.strip()

        # Remove Twitter entities
        if word: 
            if word[0] not in twitter_prefixes and word[:2] != "RT":
                realWords.append(word)

    return ' '.join(realWords)


try: 
    for tweet in tweets.find():
        counter += 1
        if counter % 1000 == 0:
            print("Tweets searched: ", counter)
        # takes the tweet and extracts the relevent text from it, giving only message 
        actual_tweet = removeEntities(removeLinks(tweet['message']))
        tweetArray.append(actual_tweet)

except OSError as e:
    pass

# Vectorize the words
vectorizer = TfidfVectorizer(stop_words='english')
vectorized = vectorizer.fit_transform(tweetArray)

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


