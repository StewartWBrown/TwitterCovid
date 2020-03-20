import pymongo 
from pymongo import MongoClient 
import networkx as nx 
import matplotlib.pyplot as plt
import seaborn as sns
from operator import itemgetter
import pandas as pd
import itertools
import numpy as np
from scipy import stats

counter=  0

client = MongoClient('mongodb://localhost:27017')
db = client.coronaDatabase
tweets = db.tweets


    
#initialise graph 
graph = nx.Graph()

try: 
  #Change Limit parameter to change number of tweets being handled, important as the graph will take a long time to create 
  #if number is too high
    for tweet in tweets.find():
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

#Average degree of nodes and most frequent
print("Graph has ", graph.number_of_nodes(), "nodes and ", graph.number_of_edges() , " edges.")
degrees = [val for (node, val) in graph.degree()]

print("Number of ties:", degrees.count(2))
print("Number of tirads: ", degrees.count(3))
print("Average degree of the nodes in the Graph is ", np.mean(degrees))
print("Most common degree of the nodes found in the Graph is ", stats.mode(degrees)[0][0])


