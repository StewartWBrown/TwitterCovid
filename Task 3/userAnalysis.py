import pymongo 
from pymongo import MongoClient 
import networkx as nx 
import matplotlib.pyplot as plt
import seaborn as sns
from operator import itemgetter

client = MongoClient('mongodb://localhost:27017')
db = client.coronaDatabase
tweets = db.tweets
# Mention Data is an array of the mentions:
# mentionData[0] is who sent the tweet
# mentionData[1] is who recieved the tweet
# mentionData[2] is the tweet ID

mentionData = []

#Popularity is a dictionary of the most popular mentioned users
popularity = {}

counter = 0
# Determines if the tweet is a retweet, discards the tweet for mention analysis as tweet may have multiple mentions 
# as not an original tweet

def connected_component_subgraphs(G):
    for c in nx.connected_components(G):
        yield G.subgraph(c)

def isRetweet(text):
   # for seperator in twitter_prefixes: 
      #  text = text.replace(seperator, ' ')
    if text[:2] != "RT":
        return False
    else: 
        return True
  

try: 
    for tweet in tweets.find().limit(10000):
        counter += 1
        if counter % 1000 == 0: 
          print(counter)
        # Skips tweets that were retweets, only interested in mentions from original tweets
        if isRetweet(tweet['message']):
          next
        else: 
          if tweet['mentions']:
            for i in tweet['mentions']:
              currentMention = []
              currentMention.append(tweet['Username'])
              currentMention.append(i['screen_name'])
              currentMention.append(tweet['_id'])
              if i['screen_name'] in popularity:
                popularity[i['screen_name']] += 1
              else: 
                popularity[i['screen_name']] = 1
            mentionData.append(currentMention)

    # Sorted popularity gives twitter users that were mentioned the most at the end of the dictionary. 
    sortedPopularity = sorted(popularity.items(), key=lambda x: x[1], reverse = True) 

except OSError as e:
    pass


graph = nx.Graph()
for interaction in mentionData: 

    graph.add_edge(interaction[0], interaction[1])

nx.draw(graph)
plt.show()