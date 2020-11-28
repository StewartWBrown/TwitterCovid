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
    for tweet in tweets.find().limit(60000):
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
  

print("Number of nodes in graph: ", graph.number_of_nodes(), "\nNumber of edges in graph: ", graph.number_of_edges())

pos = nx.spring_layout(graph, k=0.15)
plt.figure()

nx.draw(graph, pos=pos, edge_color="black", linewidths= 0.05, node_size = 10, alpha=0.6, with_labels=False)
nx.draw_networkx_nodes(graph, pos=pos, node_size=5, node_colour= range(graph.number_of_nodes()), cmap="coolwarm")


plt.show()
