import pymongo 
from pymongo import MongoClient 
import networkx as nx 
import matplotlib.pyplot as plt
import seaborn as sns
from operator import itemgetter
import pandas as pd
import itertools

counter=  0

client = MongoClient('mongodb://localhost:27017')
db = client.coronaDatabase
tweets = db.tweets


    
#initialise graph 
graph = nx.Graph()

try: 
  #Change Limit parameter to change number of tweets being handled, important as the graph will take a long time to create 
  #if number is too high
    for tweet in tweets.find().limit(100):
        currentHashtags = []
        for i in tweet['Hashtags']:
            current = i['text'] 
            currentHashtags.append(current)
        
        if len(currentHashtags) > 1:
            duos = list(itertools.combinations(currentHashtags,2))
            for duo in duos:
                graph.add_edge(duo[0], duo[1])
        elif len(currentHashtags) == 1: 
            graph.add_node(currentHashtags[0])


except IndexError as e:
    pass

print("Number of nodes in graph: ", graph.number_of_nodes(), "\nNumber of edges in graph: ", graph.number_of_edges())

pos = nx.spring_layout(graph, k=0.15)
plt.figure()

nx.draw(graph, pos=pos, edge_color="black", linewidths= 0.05, node_size = 10, alpha=0.6, with_labels=True)
nx.draw_networkx_nodes(graph, pos=pos, node_size=5, node_colour= range(graph.number_of_nodes()), cmap="coolwarm")

plt.show()
