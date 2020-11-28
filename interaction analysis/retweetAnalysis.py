import pymongo 
from pymongo import MongoClient 
import networkx as nx 
import matplotlib.pyplot as plt
import seaborn as sns
from operator import itemgetter
import pandas as pd
import numpy as np
from scipy import stats

counter=  0

client = MongoClient('mongodb://localhost:27017')
db = client.coronaDatabase
tweets = db.tweets

# Retweet Data is an array of the retweets:
# retweetData[0] is who retweeted the tweet
# retweetData[1] is the user who was retweeted
# retweetData[2] is the tweet ID
retweetData = []

# Determines if the tweet is a retweet, this allows us to extract data from it
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
        # Skips tweets that were not retweets, only interested in handling retweets
        if isRetweet(tweet['message']):
          # Add relevent information to array of retweet data
          currentRetweet = []
          #currentRetweet.extend((tweet['Username'], tweet['mentions'][0]['screen_name'], tweet['_id']))

          currentRetweet.append(tweet['Username'])
          currentRetweet.append(tweet['mentions'][0]['screen_name'])
          currentRetweet.append(tweet['_id'])
          retweetData.append(currentRetweet)
        else: 
          next

except IndexError as e:
    pass


# Creating the graph 
graph = nx.Graph()


# Adding the user who tweeted and the user who was mentioned in each interaction to a graph 
for interaction in retweetData: 
  graph.add_edge(interaction[0], interaction[1])
  

#Average degree of nodes and most frequent
print("Graph has ", graph.number_of_nodes(), "nodes and ", graph.number_of_edges() , " edges.")
degrees = [val for (node, val) in graph.degree()]

print("Number of ties:", degrees.count(2))
print("Number of tirads: ", degrees.count(3))
print("Average degree of the nodes in the Graph is ", np.mean(degrees))
print("Most common degree of the nodes found in the Graph is ", stats.mode(degrees)[0][0])
