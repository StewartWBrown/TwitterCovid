import pymongo 
from pymongo import MongoClient 
import networkx as nx 
import matplotlib.pyplot as plt
import seaborn as sns
from operator import itemgetter
import pandas as pd
import numpy as np
from scipy import stats
import numpy as np
from scipy import stats

counter=  0

client = MongoClient('mongodb://localhost:27017')
db = client.coronaDatabase
tweets = db.tweets

# Mention Data is an array of the mentions:
# mentionData[0] is who sent the tweet
# mentionData[1] is who recieved the tweet
# mentionData[2] is the tweet ID
mentionData = []

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
  #Change Limit parameter to change number of tweets being handled, important as the graph will take a long time to create 
  #if number is too high
    for tweet in tweets.find():
        counter += 1
        if counter % 1000 == 0: 
          print(counter)
        # Skips tweets that were retweets, only interested in mentions from original tweets
        if isRetweet(tweet['message']):
          next
        else: 
          # Extract the tweeter, tweeted and tweetID of whoever the tweet is between
          if tweet['mentions']:
            for i in tweet['mentions']:
              currentMention = []
              currentMention.extend((tweet['Username'], i['screen_name'], tweet['_id']))
              mentionData.append(currentMention)

except OSError as e:
    pass


# Creating the graph 
graph = nx.Graph()


# Adding the user who tweeted and the user who was mentioned in each interaction to a graph 
for interaction in mentionData: 
  graph.add_edge(interaction[0], interaction[1])

#Average degree of nodes and most frequent
print("Graph has ", graph.number_of_nodes(), "nodes and ", graph.number_of_edges() , " edges.")
degrees = [val for (node, val) in graph.degree()]

print("Number of ties:", degrees.count(2))
print("Number of tirads: ", degrees.count(3))
print("Average degree of the nodes in the Graph is ", np.mean(degrees))
print("Most common degree of the nodes found in the Graph is ", stats.mode(degrees)[0][0])


