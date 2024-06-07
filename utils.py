from collections import defaultdict
from cdlib import NodeClustering, algorithms, evaluation
from infomap import Infomap
import gravis as gv
from scipy import io
import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import csv, os, pickle, random
import igraph as ig
#from msb import Balance


path = 'Data'
matricesPath = 'Raw matrices'

pearsonCorrelationMatricesPath = 'Correlation matrices Pearson'
pearsonCorrelationImagesPath = 'Correlation images Pearson'
euclideanCorrelationMatricesPath = 'Correlation matrices Euclidean'
euclideanCorrelationImagesPath = 'Correlation images Euclidean'

pearsonGraphsPath = 'Networkx graphs Pearson'
euclideanGraphsPath = 'Networkx graphs Euclidean'

pearsonAverageDegreesPath = 'Pearson average degrees'
pearsonClusteringCoefficientsPath = 'Pearson clustering coefficients'
pearsonAveragePathLenghtsPath = 'Pearson average path lenghts'


def dataToBinary(data, filename):
    with open(filename, 'wb') as object_file:
        pickle.dump(data, object_file)

def binaryToData(fileName):
    with open(fileName, 'rb') as object_file:
        data = pickle.load(object_file)
        return data
    
def averageDegree(network):
    degrees = []
    if nx.is_weighted(network):
        degrees = [val for (node, val) in network.degree(weight='weight')]
    else:
        degrees = [val for (node, val) in network.degree()]
    sum = 0
    for d in degrees:
        sum += d
    return sum/len(degrees)

def APL(network):
    if (nx.is_directed(network)):
        largestComponent = 0
        largestAPL = 0
        for C in (network.subgraph(c) for c in nx.weakly_connected_components(network)):
            if largestComponent<len(C.nodes):
                largestComponent = len(C.nodes)
                if nx.is_weighted(network):
                    apl = nx.average_shortest_path_length(C, weight='weight')
                else:
                    apl = nx.average_shortest_path_length(C)
                largestAPL = apl
        return largestAPL
    else:
        for C in (network.subgraph(c) for c in nx.connected_components(network)):
            if nx.is_weighted(network):
                return nx.average_shortest_path_length(C, weight='weight')
            else:
                return nx.average_shortest_path_length(C)

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
