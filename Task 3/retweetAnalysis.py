import pymongo 
from pymongo import MongoClient 
import networkx as nx 
import matplotlib.pyplot as plt
import seaborn as sns
from operator import itemgetter
import pandas as pd

counter=  0

client = MongoClient('mongodb://localhost:27017')
db = client.coronaDatabase
tweets = db.tweets

# Retweet Data is an array of the retweets:
# mentionData[0] is who retweeted the tweet
# mentionData[1] is the user who was retweeted
# mentionData[2] is the tweet ID
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
    for tweet in tweets.find().limit(2000):
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
  

print("Number of nodes in graph: ", graph.number_of_nodes(), "\nNumber of edges in graph: ", graph.number_of_edges())

pos = nx.spring_layout(graph, k=0.15)
plt.figure()

nx.draw(graph, pos=pos, edge_color="black", linewidths= 0.05, node_size = 10, alpha=0.6, with_labels=False)
nx.draw_networkx_nodes(graph, pos=pos, node_size=5, node_colour= range(graph.number_of_nodes()), cmap="coolwarm")

plt.show()
