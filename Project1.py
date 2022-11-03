import numpy as np
import networkx as nx
import random as rand
import matplotlib.pyplot as plt
import os
import itertools
import time


####
# Graph creation, writting, reading and visualization
####


seed = 97639 # Student number as seed
rand.seed(seed) # Sets new 'random' module seed

m = 30# Maximum number of edges
n = round(m/2)# Number of vertices, a fraction of the maximum number of edges

graph_counter = 0

def create_Graph():
    """
    Creates a new random Graph object with maximum m edges and n nodes. Vertices are separated by atleast 
    0.1 unit of each other. Self-loops can be accepted by commenting the correct condition segment below.
    """

    global graph_counter
    graph_counter += 1 

    G = nx.Graph() # Initializes object 

    seen_pos = set() # Set for existing position

    # First the nodes
    k=1
    G.add_node(k, pos=(rand.randint(1,20), rand.randint(1,20))) # Adds the first node

    while len(list(G)) < n:
    
        x,y = (1+ rand.random()*20, 1+ rand.random()*20) # Generates random coordinates
        
        if (x,y) not in seen_pos:
            tmp = list(nx.get_node_attributes(G, 'pos').values()) 
            
            # Iterates over the temporary node position list
            for j in range(0,len(tmp)):
                x_tmp, y_tmp = tmp[j]
                can_add = True

                # Checks if x and y are atleast 1 unit away from other nodes' x and y
                if abs(x - x_tmp) >= 0.01 and abs(y - y_tmp)>= 0.01:
                    can_add = True
                    
                else:
                    can_add = False
                    break

            if can_add:
                G.add_node(k, pos=(x,y), n_edges = 0) # Adds node to graph
                k+=1
                seen_pos.add((x,y)) # Adds coordinates to positions set
                print("Node added.")

            else: 
                print("Node too close.")

    print("\n###########")
    print("All nodes added to graph.")
    print("###########\n")

    # Now the edges
    seen_edge = set()
    possible_edges = m 

    # repeats loop until the maximum number of edges is achieved, i.e. possible_edges == 0
    while possible_edges > 0:


        safeguard = 0 # a safeguard against the infinite loop that is happening for n = 12.5% and n= 25% of m at lower values,
                      # like m = 20 and n = 1/6 * m. These values create an infinite loop in this section!
                      # This makes sense since there is a limited number of loops possible in a graph, even if self-loops are included

        n_edges = rand.randint(1, n)
        if n_edges > possible_edges: continue

        i = 0 
        print(seen_edge)
        if n_edges == 0 or n_edges >= n: continue

        else: # add edges until required random number of edges in a vertex is achieved
            while i < n_edges:
                print(seen_edge)
                u,v = (rand.randint(1,n), rand.randint(1,n)) # Creates first edge
                
                # Checks if u and v nodes are not the same and corrects the 2nd node if they are
                # Prevents self-loop, can opt out my commenting this condition segment
                if u == v: 
                    v = rand.randint(1,n)
                    continue
                
                if (u,v) not in seen_edge and (v,u) not in seen_edge: # (u,v) and (v,u) edges are the same
                    G.add_edge(u,v)
                    seen_edge.add((u,v))
                    G.nodes[u]['n_edges'] += 1 # Increments edge number of each node
                    G.nodes[v]['n_edges'] += 1
                    print("Edge added")
                    i +=1
                    print(seen_edge)
                    possible_edges -= 1
                else:
                    print("Edge already exists")
                    safeguard +=1
                    
                    if safeguard == 500: # threshold for cancelling loop, might need to be changed depending on graph size
                        possible_edges = 0
                        break
                    continue
                    
    
    print("\n###########")
    print("All edges added to graph.")
    print("###########\n")

    return G

def write_Graph(G: nx.Graph):
    """
    Takes given graph G as input as saves it to a file. Uses GML format
    since it's able to also store node attributes.
    """
    nx.write_gml(G, "Graph"+str(graph_counter)+".txt") # Graph complete data
    print("\nGraph saved.")

def read_Graphs():
    """"
    Reads "Graph*.txt" files in current directory and returns a list with every graph in directory.
    """
    path = os.getcwd() # gets files from current directory
    id = 0 # counter for graphs read

    G_lst = []

    with os.scandir(path) as itr: # iterates directory for graph text files
        for entry in itr:
            if not entry.name.startswith('.'): #excludes hidden files 
                if entry.name.startswith('Graph') and entry.name.endswith('.txt'):
                    print(entry.name)
                    try:
                        G = nx.read_gml(entry.name)
                        id +=1
                        print("Graph {id} read:".format(id = id))
                        print(G)
                        G_info = [G, id]
                        G_lst.append(G_info) # G_info -> [nx.Graph, adj_list, id]
                        
                    except FileNotFoundError:
                        print("That file doesn't exist. Maybe there are no graphs in this directory.")
                        continue
    return G_lst

def visualize_Graph(G: nx.Graph):
    """
    Creates matplotlib figure with labeled and positioned nodes, and edges for a given graph G.
    """

    fig, ax = plt.subplots() # Initializes plot instance

    nx.draw_networkx(G, pos= nx.get_node_attributes(G, 'pos'), with_labels = True) # Draws graph with correct coordinates
    ax.tick_params(left = True, bottom = True, labelleft = True, labelbottom = True) # Adds axis units to aid understanding of graph

    # Plot labels
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Graph")
    plt.show()

# Look up networkx dominating set for existing algorithm to compare to created algorithm later

####
# Brute force algorithm
####

## HEURISTIC : GET NODE ATTRIBUTE THAT HAS NUMBER OF EDGES CONNECTED TO THAT NODE, GET THAT NODE AND ADJACENT ONES 'REMOVED' FROM ALGORITHM AND FIND THE REMAINING, REPEAT 

####
# Exhaustive search algorithm - find all dominating sets then choose lowest vertice one(s).
####

# create every possible combination, varying in size, then run a check up and keep ones that are valid dominant sets

def is_dom_set(G, D):
    """
    Returns a boolean whether the subset of G is a dominant set or not.
    """

    edges = G.edges
    V = G.nodes

    is_dom = False
    for d in D:
        for v in V:
            if v not in D: #and len(D) != 1: # verifies if node is in subset D, if not, verifies if its adjacent to any another node in the set
                for d2 in D:
                    if (d2,v) in edges or (v,d2) in edges: # checks if nodes are adjacent
                        is_dom = True
                        break
                    else:
                        is_dom = False
                if is_dom == True:
                    continue
                else: 
                    return False
                    
    return True




def find_dom_sets(G):
    """
    Finds all possible dominating sets in a given graph G. First it creates every possible combinations, then it keeps 
    only the dominant sets
    """

    nodes_arr = G.nodes
    subsets = [list(S) for l in range(1, len(nodes_arr)) for S in itertools.combinations(nodes_arr, l)] # every possible set of vertices from G

    dom_sets = []

    edges = G.edges

    for D in subsets: 
        if is_dom_set(G, D):
            dom_sets.append(tuple(D)) #list with every dominant set of given graph

    return dom_sets

    
# for i in range(5): #creates 5 random graphs and stores them
#     m = rand.randint(4,60)
#     n = round(m/4)
#     G = create_Graph()
#     write_Graph(G)

G_lst = read_Graphs()

print(G_lst)

dom_sets = []
for i in range(len(G_lst)):
    dom_sets.append(find_dom_sets(G_lst[i][0]))
