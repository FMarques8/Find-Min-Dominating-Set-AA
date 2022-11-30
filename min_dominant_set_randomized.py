import random
import networkx as nx
import matplotlib.pyplot as plt
import os
import time


def read_Graph(fname: str, form: str = 'SW'):
    """
    Reads and converts graph depending on type. fname = file name
    form = graph format
    Current supported graph formats are S&W, Mendeley data, Stanford
    and custom created graphs with find_min_dominating_sets.
    """

    if form == 'SW' or form == 'stanford':
        
        G = nx.Graph()
        with open(fname, 'r') as f:
            
            if form == 'SW':
                for i in range(4):
                    f.readline() #skips first 4 lines if its a graph from S&W
            
            lines = f.readlines()

            for line in lines:
                
                edge = [int(u) for u in line.strip().split()[0:2]] #reads only first 2 entries of each line
                if edge == []: #some lines are empty lists and this will raise exception when adding the edge
                    continue
                if edge[0] != edge[1]:
                    G.add_edge(edge[0], edge[1])
                    
    elif form == 'custom': #previous project graphs -> very tiny
        G = nx.read_gml(fname)
    
    elif form == 'BD': #adjacency matrix
        with open(fname, 'r') as f:
            n = int(f.readline().strip().split()[0])
            
            # initializes graph and adds nodes from range
            G = nx.Graph()
            G.add_nodes_from(range(n))
            i = 0 # index

            for row in f.readlines():
                if row == '':
                    continue
                
                row = row.strip().split()
                
                for j in range(len(row)): # column, the len(row) should always be the same
                    if row[j] == '1':
                        G.add_edge(i,j)
                i += 1   
        
    else:
        print("Format not supported.")
    
    return G


# IDEA 1
## RANDOMLY CHOOSE SUBSET SIZE AND GET SOME OR ALL DOMINANT SETS OF THAT SIZE
## IF THERE ARE DOM SETS OF THAT SIZE, RANDOMLY CHOOSE ANOTHER SIZE OF SUBSET
## AND KEEP A SMALLER ONE, REPEAT PROCESS UNTIL IT CANT REDUCE ANYMORE

# IDEA 2
## RANDOMLY CHOOSE NODES TO REMOVE USING THE PREVIOUS HEURISTIC 
## INSTEAD OF GOING AFTER NODES WITH GREATER NUMBER OF CONNECTIONS
## AND REPEAT A FEW TIMES TO GET SEVERAL DOM SETS

# MIGHT BE A GOOD IDEA TO USE BOTH METHODS

def random_node_min_dom_sets(G: nx.Graph, p: int = 20):
    """
    Returns up to p minimum dominant sets of G. Randomly chooses the nodes
    to remove, using the greedy heuristic used previously.
    """
    dom_sets = []
    threshold = 0 # threshold in case it doesnt find new dominant sets

    for i in range(p):
        edges = [list(e) for e in G.edges]
        nodes = [v for v in G.nodes]
        
        removed_nodes = []
        while len(nodes) > 0: # Iterates over nodes until there are none left
            
            # as it randomly chooses nodes, there is no need to count the number of connections for each node
            rndm_node = nodes[random.randint(0, len(nodes)-1)] # chooses random node, will also be removed
            while rndm_node not in nodes:
                rndm_node = nodes[random.randint(0, len(nodes)-1)]
            # len(G)-1 because randint includes both extremes into the function, and the last node is len(G)-1
            
            removed_nodes.append(rndm_node) # list of removed nodes which will be the minimum dominating set later
            nodes.remove(rndm_node)
            
            adjacent_nodes= []
            for edge in reversed(edges):
                # Adds the adjacent node to a list and removes the main node edge
                if edge[0] == rndm_node:
                    adjacent_nodes.append(edge[1])
                    nodes.remove(edge[1])
                    edges.remove(edge)
                elif edge[1] == rndm_node:
                    adjacent_nodes.append(edge[0])
                    nodes.remove(edge[0])
                    edges.remove(edge) 
                    
            # Removed adjacent nodes' edges
            for adj_node in adjacent_nodes:
                for edge in reversed(edges):
                    if edge[0] == adj_node or edge[1] == adj_node:
                        edges.remove(edge)

        if ~any(node in D for node in removed_nodes for D in dom_sets) and sorted(removed_nodes) not in dom_sets:
            dom_sets.append(sorted(removed_nodes))
        else:
            i -= 1
            threshold +=1
            
        if threshold >= 100: #threshold in case new unique dom sets arent found
            break
    
    len_arr = [len(x) for x in dom_sets] #creates array with length of each dom set
    min_sets = [x for x in dom_sets if len(x) == min(len_arr)] #creates array with minimum dominating sets
    
    return min_sets


def random_size_min_dom_sets(G: nx.Graph, p:int = 20):
    """
    Returns up to p minimum dominant sets of G. Creates random subsets in similar form to 
    random_node_min_dom_sets and minimizes subsets.
    """
    min_dom_sets = []
    threshold = 0 # threshold in case it doesnt find new dominant sets
    
    min_size = len(G) #sets the size that will help with minimizing as the size of the graph
    
    for i in range(p):
        edges = [list(e) for e in G.edges]
        nodes = [v for v in G.nodes]
        removed_nodes = []
        
        while len(nodes) > 0: # Iterates over nodes until there are none left
            
            # as it randomly chooses nodes, there is no need to count the number of connections for each node
            rndm_node = nodes[random.randint(0, len(nodes)-1)] # chooses random node, will also be removed
            while rndm_node not in nodes:
                rndm_node = nodes[random.randint(0, len(nodes)-1)]
            # len(G)-1 because randint includes both extremes into the function, and the last node is len(G)-1
            
            removed_nodes.append(rndm_node) # list of removed nodes which will be the minimum dominating set later
            nodes.remove(rndm_node)
            
            adjacent_nodes= []
            for edge in reversed(edges):
                # Adds the adjacent node to a list and removes the main node edge
                if edge[0] == rndm_node:
                    adjacent_nodes.append(edge[1])
                    nodes.remove(edge[1])
                    edges.remove(edge)
                elif edge[1] == rndm_node:
                    adjacent_nodes.append(edge[0])
                    nodes.remove(edge[0])
                    edges.remove(edge) 
                    
            # Removed adjacent nodes' edges
            for adj_node in adjacent_nodes:
                for edge in reversed(edges):
                    if edge[0] == adj_node or edge[1] == adj_node:
                        edges.remove(edge)

        if len(removed_nodes) < min_size:
            min_size = len(removed_nodes) #sets new minimum size of set
            min_dom_sets = [removed_nodes] #resets list with dom sets (minimum) and iteration in for loop
            i = 0
        elif len(removed_nodes) == min_size: #if set has same size as current minimum set, add to list
            if ~any(node in D for node in removed_nodes for D in min_dom_sets) and sorted(removed_nodes) not in min_dom_sets:
                min_dom_sets.append(sorted(removed_nodes))
        else: #if size of set is greater than current minimum length, increment the threshold
            i -= 1
            threshold +=1
            
        if threshold >= 100: #threshold in case new unique dom sets arent found
            break
    
    return min_dom_sets


cwdir = os.getcwd() # Please include graph files in same workspace, or change this variable to directory where they are located
# Assuming that in the graph folder there are no other files other than the graph .txt files
print(cwdir)
graph_dir = {'custom_tinyG': 'custom', 'stanford': 'stanford', 'SW_Graphs': 'SW', 
             'BD0': 'BD', 'BD1': 'BD', 'BD2': 'BD', 'BD3': 'BD', 'BD5': 'BD', 'BD6': 'BD'}

G_list = [] # list with every graph, grouped by directory

i = 0
for dir in graph_dir.keys():
    lst = []
    with os.scandir(cwdir+"/"+dir) as itr:
        for entry in itr:
            fname = cwdir+"/"+dir+"/"+entry.name
            print(fname + " loaded.")
            G = read_Graph(fname = fname, form = graph_dir[dir])
            lst.append(G)
    G_list.append(lst)


min_sets = []
times = []
for group in G_list:
    sub_min_sets = []
    sub_times = []
    for G in group:
        print(G)
        start = time.time()
        sets_min = random_size_min_dom_sets(G, p = 1)
        end = time.time()
        sub_min_sets.append(sets_min)
        sub_times.append(end-start)
    min_sets.append(sub_min_sets)
    times.append(sub_times)

print(times)