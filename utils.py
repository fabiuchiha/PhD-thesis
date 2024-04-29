from collections import defaultdict
from cdlib import NodeClustering, algorithms
from infomap import Infomap
from scipy import io
import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import gravis as gv
import csv, os, pickle, random


path = 'Data'
matricesPath = 'Raw matrices'
correlationMatricesPath = 'Correlation matrices'
correlationImagesPath = 'Correlation images'
graphsPath = 'Networkx graphs'

def dataToBinary(data, filename):
    with open(filename, 'wb') as object_file:
        pickle.dump(data, object_file)

def binaryToData(fileName):
    with open(fileName, 'rb') as object_file:
        data = pickle.load(object_file)
        return data
    
def averageDegree(network):
    degrees = [val for (node, val) in network.degree()]
    sum = 0
    for d in degrees:
        sum += d
    return sum/len(degrees)

def kin(network):
    nodes = network.nodes()
    sum = 0
    for n in nodes:
        sum += network.in_degree(n)
    return sum/len(nodes)

def kout(network):
    nodes = network.nodes()
    sum = 0
    for n in nodes:
        sum += network.out_degree(n)
    return sum/len(nodes)

def APL(network):
    if (nx.is_directed(network)):
        largestComponent = 0
        largestAPL = 0
        for C in (network.subgraph(c) for c in nx.weakly_connected_components(network)):
            if largestComponent<len(C.nodes):
                largestComponent = len(C.nodes)
                apl = nx.average_shortest_path_length(C)
                largestAPL = apl
        return largestAPL
    else:
        for C in (network.subgraph(c) for c in nx.connected_components(network)):
            return nx.average_shortest_path_length(C)

def networkInfo(network):
    print("Average degree:", averageDegree(network))
    if (nx.is_directed(network)):
        print("Internal average degree:", kin(network))
        print("External average degree:", kout(network))
    print("Clustering coefficient:", nx.average_clustering(network))
    print("Average Path Length (highest value):", APL(network))

def infomapClustering(net, flags):
    # Add infomap flags
    im = Infomap(flags)
    # Add network to infomap
    im.add_networkx_graph(net)
    # Run infomap
    im.run()
    # Get infomap communities
    communities = defaultdict(list)
    for node_id, module_id in im.modules:
        communities[module_id].append(node_id)
    # Return communities as NodeClustering class    
    return NodeClustering(list(communities.values()), net, "Infomap", method_parameters={"flags": flags})