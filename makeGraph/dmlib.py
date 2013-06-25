import requests
from contextlib import closing
import networkx as nx
from collections import defaultdict
import json
import math
import cPickle as pickle
from networkx.readwrite import json_graph
import gc

GRAPH = None

def build_graph(Pickle_save=False):
    print 'Starting Graph building'
    GRAPH = nx.Graph()
    words = {}
    pairs = {}
    sum_words_counts = 0
    #reads the file
    with closing(open('combined_output', 'r')) as data_file:
        #build the graph (calcultating the pmi)
        for line in data_file:
            key_value = line.split('\t')
            key = json.loads(key_value[0])
            value = json.loads(key_value[1])
            if len(key) == 1:
                if len(key[0])>1:
                    if value>19:
                        #single word case
                        GRAPH.add_node(key[0], weight=value)
                        #words[key[0]] = value
                        sum_words_counts += value

    with closing(open('combined_output', 'r')) as data_file:
        for line in data_file:
            key_value = line.split('\t')
            key = json.loads(key_value[0])
            value = json.loads(key_value[1])            
            if len(key) == 2:
                if (key[0] in GRAPH.node) and (key[1] in GRAPH.node):
                    if value>5:
                        pairs[key[0]+'#'+key[1]] = value
    print 'Dictionaries built'
        

    for key_pair,value in pairs.iteritems():
        #value = pairs[key_pair]
        key = key_pair.split('#')
        #count_word0 = float( GRAPH.node.get(key[0],1) )
        count_word0 = float( GRAPH.node[key[0]]['weight'] )
        #count_word1 = float( GRAPH.node.get(key[1],1) )
        count_word1 = float( GRAPH.node[key[1]]['weight'] )
        count_pair  = float( value )
        pmi = math.log((count_pair / sum_words_counts) / ((count_word0 / sum_words_counts) * (count_word1 / sum_words_counts)), 2)
        if pmi>10:
            GRAPH.add_edge(key[0], key[1], weight=pmi)


    print 'Saving Graph to file'
    words=None
    pairs=None
    if Pickle_save:
        gc.collect()
        p = pickle.Pickler(open("graph.cache","wb"))
        p.fast=True
        p.dump(GRAPH)
    else:
        nx.write_gml(GRAPH,'graph10c.gml')
    #with closing(open('graph.cache', 'w')) as graph_file:    
    #    pickle.dump(GRAPH, graph_file)
    

def load_graph():
    #loads the file of the graph previously built
    with closing(open('graph.cache', 'r')) as graph_file:    
        GRAPH = pickle.load(graph_file)

def json_network():
    #returns the string of the json of the graph previously loaded
    return json_graph.dumps(GRAPH)

def json_2axis(word1, word2, degree_filter, pmi_filter):
    #filter = (min_value, max_value)
    #get all neighbours of word1
    #get all neighbours of word2
    #construct a list of words like: [(word_a, pm1_word1, pm1_word2), (word_b, pm1_word1, pm1_word2), ...]
    #return the json of this list of words
    pass

def get_filtered_neighbors(word, degree_filter, pmi_filter):
    #filter = (min_value, max_value)
    #get the neighnors
    #for each node filter by degree
    #for each edge filter by pmi
    #return the list of neighbors
    pass

if __name__ == '__main__':
    build_graph()
