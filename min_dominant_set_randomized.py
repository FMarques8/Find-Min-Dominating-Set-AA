import random
import networkx as nx
import matplotlib.pyplot as plt
import os
import time


def read_Graph(fname: str, form: str = 'SW', size_check: bool = True, name: str = 'Graph'):
    """
    Reads and converts graph depending on type. fname = file name;
    form = graph format; name = 'Graph', name for later saving to file
    size_check = True verifies the number of nodes in graph.
    Current supported graph formats are S&W, Mendeley data, Stanford
    and custom created graphs with find_min_dominating_sets.
    """

    if form == 'SW' or form == 'stanford':
        
        G = nx.Graph(name = name)
        with open(fname, 'r') as f:
            
            if form == 'SW':
                for i in range(4):
                    f.readline() #skips first 4 lines if its a graph from S&W
                    f.readline()
                    n = int(f.readline().strip().split()[0])
                    
                    # if algorithm is loading graphs, it only cares about number of nodes
                    if size_check == True:
                        if n > 500:
                            return True
                        else:
                            return False
                    
            lines = f.readlines()
            for line in lines:
                
                edge = [int(u) for u in line.strip().split()[0:2]] #reads only first 2 entries of each line
                if edge == []: #some lines are empty lists and this will raise exception when adding the edge
                    continue
                if edge[0] != edge[1]:
                    G.add_edge(edge[0], edge[1])
            
            # for the stanford graph used we can only check number of nodes after creating the graph
            if size_check == True:
                if len(G.nodes) > 500:
                    return True
                else:
                    return False
                    
    elif form == 'custom': #previous project graphs -> very tiny
        G = nx.read_gml(fname)
        G.graph['name'] = name
        if size_check == True:
            if len(G.nodes) > 500:
                return True
            else:
                return False
    
    elif form == 'BD': #adjacency matrix
        with open(fname, 'r') as f:
            # n = int(f.readline().strip().split()[0])
            n = int(f.readline().strip().split()[0])
            
            if size_check == True:
                if n > 500:
                    return True
                else:
                    return False
            
            # initializes graph and adds nodes from range
            G = nx.Graph(name = name)
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

def random_nodes_min_dom_sets(G: nx.Graph, p: int = 20):
    """
    Returns up to p minimum dominant sets of G. Randomly chooses the nodes
    to remove, using the greedy heuristic used previously.
    """
    dom_sets = []
    threshold = 0 # threshold in case it doesnt find new dominant sets
    reached_threshold = False # variable to let us know if the threshold was reached or not
    
    for i in range(p):
        edges = [list(e) for e in G.edges]
        nodes = [v for v in G.nodes]
        removed_nodes = []
        
        while len(nodes) > 0: # Iterates over nodes until there are none left
            
            # as it randomly chooses nodes, there is no need to count the number of connections for each node
            rndm_node = nodes[random.randrange(0, len(nodes))] # chooses random node, will also be removed
            while rndm_node not in nodes:
                rndm_node = nodes[random.randrange(0, len(nodes))]
            
            removed_nodes.append(rndm_node) # list of removed nodes which will be the minimum dominating set later
            nodes.remove(rndm_node)
            
            adjacent_nodes= []
            for edge in reversed(edges):
                # Adds the adjacent node to a list and removes the main node edge
                if edge[0] == rndm_node:
                    adjacent_nodes.append(edge[1])
                    edges.remove(edge)
                    try:
                        nodes.remove(edge[1])
                    except ValueError:
                        continue
                elif edge[1] == rndm_node:
                    adjacent_nodes.append(edge[0])
                    edges.remove(edge) 
                    try:
                        nodes.remove(edge[0])
                    except ValueError:
                        continue
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
            
        if threshold >= 50: #threshold in case new unique dom sets arent found
            reached_threshold = True
            break
    
    len_arr = [len(x) for x in dom_sets] #creates array with length of each dom set
    min_sets = [x for x in dom_sets if len(x) == min(len_arr)] #creates array with minimum dominating sets
    
    return min_sets, reached_threshold


def random_size_min_dom_sets(G: nx.Graph, p:int = 20):
    """
    Returns up to p minimum dominant sets of G. Creates random subsets in similar form to 
    random_node_min_dom_sets and minimizes subsets.
    """
    min_dom_sets = []
    threshold = 0 # threshold in case it doesnt find new dominant sets
    reached_threshold = False # variable to let us know if the threshold was reached or not
    
    min_size = len(G) #sets the size that will help with minimizing as the size of the graph
    
    for i in range(p):
        edges = [list(e) for e in G.edges]
        nodes = [v for v in G.nodes]
        removed_nodes = []
        
        while len(nodes) > 0: # Iterates over nodes until there are none left
            
            # as it randomly chooses nodes, there is no need to count the number of connections for each node
            rndm_node = nodes[random.randrange(0, len(nodes))] # chooses random node, will also be removed
            while rndm_node not in nodes:
                rndm_node = nodes[random.randrange(0, len(nodes))]
            
            removed_nodes.append(rndm_node) # list of removed nodes which will be the minimum dominating set later
            nodes.remove(rndm_node)
            
            adjacent_nodes= []
            for edge in reversed(edges):
                # Adds the adjacent node to a list and removes the main node edge
                if edge[0] == rndm_node:
                    adjacent_nodes.append(edge[1])
                    edges.remove(edge)
                    try:
                        nodes.remove(edge[1])
                    except ValueError:
                        continue
                    
                elif edge[1] == rndm_node:
                    adjacent_nodes.append(edge[0])
                    edges.remove(edge)
                    try:
                        nodes.remove(edge[0])
                    except ValueError:
                        continue
                    
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
            
        if threshold >= 50: #threshold in case new unique dom sets arent found
            reached_threshold = True
            break
    
    return min_dom_sets, reached_threshold


def nx_min_dom_sets(G:nx.Graph, p:int = 20):
    """
    Returns up to p minimum dominating sets
    """
    current_min_dominating_set = nx.dominating_set(G) # starting dominating set for comparison in the algorithm
    minimum_dominating_sets = [current_min_dominating_set] #list with minimum dominating sets
    
    threshold = 0 # as this involves a while loop it is advised to use a threshold in case the algorithm gets stuck
    reached_threshold = False # variable to let us know if the threshold was reached or not
    
    for i in range(p):
        random_set = random.sample(range(0,len(G)), random.randrange(1,len(G))) # creates random subset which will be tested
        if nx.is_dominating_set(G, random_set):
            if len(random_set) < len(current_min_dominating_set): #if random set is smaller than previous dominating set, replace variables
                current_min_dominating_set = random_set
                minimum_dominating_sets = [current_min_dominating_set]
                
            elif len(random_set) == len(current_min_dominating_set):
                if ~any(node in D for node in random_set for D in minimum_dominating_sets) and sorted(random_set) not in minimum_dominating_sets:
                    minimum_dominating_sets.append(random_set)
                
        else:
            i = i + 1
            threshold += 1
            
        if threshold > 50:
            reached_threshold = True
            break
        
    return minimum_dominating_sets, reached_threshold


cwdir = os.getcwd() # Please include graph files in same workspace, or change this variable to directory where they are located
# Assuming that in the graph folder there are no other files other than the graph .txt files

graph_dir = {'custom_tinyG': 'custom', 'stanford': 'stanford', 'SW_Graphs': 'SW', 
             'BD0': 'BD', 'BD1': 'BD', 'BD2': 'BD', 'BD3': 'BD', 'BD5': 'BD', 'BD6': 'BD'}

######
## Loading the graphs
######

G_list = [] # list with every graph, grouped by directory

for dir in graph_dir.keys():
    lst = []
    with os.scandir(cwdir+"/"+dir) as itr:
        for entry in itr:
            if entry.name.startswith('Experimentos'): # skips some specific files that are not graphs found in the 'BD' folders
                continue
            fname = cwdir+"/"+dir+"/"+entry.name
            is_large = read_Graph(fname = fname, form = graph_dir[dir], size_check = True, name = dir+"/"+entry.name)
            print(entry.name)
            # skips very large graphs, a few will still be computed later but they are computationally heavy
            # this saves alot of time
            if is_large:
                print(fname+" is too large.")
                continue
            else: # if graph is below certain size (500) appends it to list of graphs
                lst.append(read_Graph(fname = fname, form = graph_dir[dir], size_check = False, name = dir+"/"+entry.name))
                print(fname + " loaded.")
    G_list.append(lst)
    
print("All graphs loaded.")

######
## Running the algorithms for the graphs and saving the results
######

# if p = 1 results will be highly innacurate
# the threshold was set to 10000 and it is still triggered alot of times!

# random_size_min_dom_sets needs atleast p=2 to be able to minimize the subsets

# random_nodes_min_dom_sets needs a very high value for p to have a chance to return
# subsets as minimized as possible, but as it is very heavy the results will not be the best
# for that function, this was realized after creating the function, but it will still be accounted 
# for the study

# although nx_min_dom_sets also minimizes the size of the subsets, it is still possible for the function
# to return false minimum dominating sets, the only way would be to generate every possible subset for each graph
# this process would take a very long time and its not worth it 

for i in range(len(G_list)):
    with open((list(graph_dir.keys())[i])+"_random_nodes_results.txt", 'w') as f:
        f.write("#############################\n")
        f.write(list(graph_dir.keys())[i] + "/ graphs\n")
        f.write("#############################\n")
        f.write("\n")
        for G in G_list[i]:
            f.write("Graph {G} with {n} nodes and {e} edges.\n".format(G = G.graph['name'], n = len(G.nodes), e = len(G.edges)))
            start = time.time()
            sets_min, threshold = random_nodes_min_dom_sets(G, p = 3)
            end = time.time()
            for D in sets_min:
                for v in D:
                    f.write(str(v)+",")
                f.write("\n")
            f.write("threshold reached: "+ str(threshold) + "\n")
            f.write("duration: "+ str(end-start) + "\n")
            f.write("\n")

for i in range(len(G_list)):
    with open((list(graph_dir.keys())[i])+"_random_size_results.txt", 'w') as f:
        f.write("#############################\n")
        f.write(list(graph_dir.keys())[i] + "/ graphs\n")
        f.write("#############################\n")
        f.write("\n")
        for G in G_list[i]:
            f.write("Graph {G} with {n} nodes and {e} edges.\n".format(G = G.graph['name'], n = len(G.nodes), e = len(G.edges)))
            start = time.time()
            sets_min, threshold = random_size_min_dom_sets(G, p = 3)
            end = time.time()
            for D in sets_min:
                for v in D:
                    f.write(str(v)+",")
                f.write("\n")
            f.write("threshold reached: "+ str(threshold) + "\n")
            f.write("duration: "+ str(end-start) + "\n")
            f.write("\n")

for i in range(len(G_list)):
    with open((list(graph_dir.keys())[i])+"_nx_results.txt", 'w') as f:
        f.write("#############################\n")
        f.write(list(graph_dir.keys())[i] + "/ graphs\n")
        f.write("#############################\n")
        f.write("\n")
        for G in G_list[i]:
            f.write("Graph {G} with {n} nodes and {e} edges.\n".format(G = G.graph['name'], n = len(G.nodes), e = len(G.edges)))
            start = time.time()
            sets_min, threshold = nx_min_dom_sets(G, p = 3)
            end = time.time()
            for D in sets_min:
                for v in D:
                    f.write(str(v)+",")
                f.write("\n")
            f.write("threshold reached: "+ str(threshold) + "\n")
            f.write("duration: "+ str(end-start) + "\n")
            f.write("\n")

# Load some random large graphs

large_graph_dir = {'stanford': 'stanford'}

big_G_list = []

# As we are purposedly loading large graphs, there is no need to verify the size first

for dir in large_graph_dir.keys():
    lst = []
    dir_list = os.listdir(cwdir+"/"+dir)
    graphs_read = []
    
    if len(dir_list) == 1: # if directory only has 1 graph (ex.: 'stanford'), there is no need to randomize the chosen graph
        lst.append(read_Graph(fname = cwdir+"/"+dir+"/"+dir_list[0], form = large_graph_dir[dir], size_check=False, name = dir+"/"+dir_list[0]))
        print(cwdir+"/"+dir+"/"+dir_list[0] + " loaded.")
    else:
        for i in range(3): # chooses 3 random graphs
            k = random.randint(0, len(dir_list))
            if k not in graphs_read:
                lst.append(read_Graph(fname = cwdir+"/"+dir+"/"+dir_list[k], form = large_graph_dir[dir], size_check=False, name = dir+"/"+dir_list[k]))
                print(cwdir+"/"+dir+"/"+dir_list[k] + " loaded.")
                graphs_read.append(k)
    big_G_list.append(lst)
print("Large graphs loaded.")

# # As the algorithm before didn't choose any graphs for these 3 folders, we can replace the text file with new data as they were empty

for i in range(len(big_G_list)):
    with open((list(large_graph_dir.keys())[i])+"_random_nodes_results.txt", 'w') as f:
        f.write("#############################\n")
        f.write(list(large_graph_dir.keys())[i] + "/ graphs\n")
        f.write("#############################\n")
        f.write("\n")
        for G in big_G_list[i]:
            f.write("Graph {G} with {n} nodes and {e} edges.\n".format(G = G.graph['name'], n = len(G.nodes), e = len(G.edges)))
            start = time.time()
            sets_min, threshold = random_nodes_min_dom_sets(G, p = 3)
            end = time.time()
            for D in sets_min:
                for v in D:
                    f.write(str(v)+",")
                f.write("\n")
            f.write("threshold reached: "+ str(threshold) + "\n")
            f.write("duration: "+ str(end-start) + "\n")
            f.write("\n")

for i in range(len(big_G_list)):
    with open((list(large_graph_dir.keys())[i])+"_random_size_results.txt", 'w') as f:
        f.write("#############################\n")
        f.write(list(large_graph_dir.keys())[i] + "/ graphs\n")
        f.write("#############################\n")
        f.write("\n")
        for G in big_G_list[i]:
            f.write("Graph {G} with {n} nodes and {e} edges.\n".format(G = G.graph['name'], n = len(G.nodes), e = len(G.edges)))
            start = time.time()
            sets_min, threshold = random_size_min_dom_sets(G, p = 3)
            end = time.time()
            for D in sets_min:
                for v in D:
                    f.write(str(v)+",")
                f.write("\n")
            f.write("threshold reached: "+ str(threshold) + "\n")
            f.write("duration: "+ str(end-start) + "\n")
            f.write("\n")

for i in range(len(big_G_list)):
    with open((list(large_graph_dir.keys())[i])+"_nx_results.txt", 'w') as f:
        f.write("#############################\n")
        f.write(list(large_graph_dir.keys())[i] + "/ graphs\n")
        f.write("#############################\n")
        f.write("\n")
        for G in big_G_list[i]:
            f.write("Graph {G} with {n} nodes and {e} edges.\n".format(G = G.graph['name'], n = len(G.nodes), e = len(G.edges)))
            start = time.time()
            sets_min, threshold = nx_min_dom_sets(G, p = 3)
            end = time.time()
            for D in sets_min:
                for v in D:
                    f.write(str(v)+",")
                f.write("\n")
            f.write("threshold reached: "+ str(threshold) + "\n")
            f.write("duration: "+ str(end-start) + "\n")
            f.write("\n")

####
# Now to run a small graph several times for statistical purposes
####

G = read_Graph(cwdir+"/SW_Graphs/SWmediumEWD.txt", form='SW', size_check=False, name="SWmediumEWD.txt")
n = 1000
with open("SWmediumEWD_results.txt", 'w') as f:
    f.write("Statistical results for {n} runs.\n\n".format(n=n))
    f.write("random_nodes_min_dom_sets(G, p= 20)\nthreshold\tduration\n")
    for i in range(n):
        start = time.time()
        sets_min, threshold = random_nodes_min_dom_sets(G, p = 20)
        end = time.time()
        f.write("{threshold}\t{duration}\n".format(threshold=threshold, duration = end-start))
        
    f.write("random_size_min_dom_sets(G, p= 20)\nthreshold\tduration\n")    
    for i in range(n):
        start = time.time()
        sets_min, threshold = random_size_min_dom_sets(G, p = 20)
        end = time.time()
        f.write("{threshold}\t{duration}\n".format(threshold=threshold, duration = end-start))
        
    f.write("nx_min_dom_sets(G, p= 20)\nthreshold\tduration\n")    
    for i in range(n):
        start = time.time()
        sets_min, threshold = nx_min_dom_sets(G, p = 20)
        end = time.time()
        f.write("{threshold}\t{duration}\n".format(threshold=threshold, duration = end-start))