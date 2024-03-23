import os
import osmnx as ox
import networkx as nx
import pickle

# Get the directory of the script
dir_path = os.path.dirname(os.path.realpath(__file__))

# Construct the full path to the OSM file
file_path = os.path.join(dir_path, 'attleborough.osm')

# Load the OSM file
G = ox.graph_from_xml(file_path)

# Convert to undirected graph
G = G.to_undirected()

# Construct the full path to the output pickle file
file_path_output = os.path.join(dir_path, 'graph.pickle')

# Write the graph to a file
with open(file_path_output, 'wb') as f:
    pickle.dump(G, f)