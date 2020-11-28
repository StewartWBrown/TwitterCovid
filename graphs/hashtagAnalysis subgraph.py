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
    for tweet in tweets.find().limit(10000):
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

pos = nx.spring_layout(graph, k=0.15)
plt.figure()

 



graphSorted = sorted(nx.connected_components(graph), key=len, reverse=True)
G0 = graph.subgraph(graphSorted[0])

nx.draw_networkx_nodes(G0, pos=pos, node_size=2, node_colour= range(graph.number_of_nodes()), cmap="coolwarm",with_labels = True)
nx.draw_networkx_edges(G0, pos=pos,
  with_labels=True,
  edge_color='r',
  width=0.1)
plt.show()

