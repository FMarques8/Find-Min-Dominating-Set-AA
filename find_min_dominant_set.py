import networkx as nx
import random as rand
import matplotlib.pyplot as plt
import os
import itertools
import time

####
# Graph creation, writting, reading and visualization
####

def create_Graph(edge_size, node_frac):
    """
    Creates a new random Graph object with maximum m edges and n nodes.
    """

    m = edge_size
    n = round(m * node_frac)
    
    if n < 3:
        n += 3

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
        if n_edges > possible_edges: 
            continue

        i = 0 
        print(seen_edge)
        
        if n_edges == 0 or n_edges >= n: 
            continue

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

def write_Graph(G: nx.Graph, id):
    """
    Takes given graph G as input as saves it to a file.
    """
    nx.write_gml(G, "Graph"+str(id)+".txt") # Graph complete data
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
                    
                    try:
                        G = nx.read_gml(entry.name)
                        id +=1
                        print("Graph {id} read".format(id = id))
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

def create_bunch(n_Graphs, edge_size = 30, seed = 97639):
    """
    Creates several graphs and writes them to file.
    """

    rand.seed(seed)

    node_size = [0.125, 0.25, 0.5, 0.75] # Node number is fraction of edges number based on project information

    for id in range(1, n_Graphs + 1):
        m = rand.randint(round(edge_size/5), edge_size) # Edge number between 12.5% and 102.5% of edge_size   
        G = create_Graph(m, node_size[rand.randint(0,3)])
        write_Graph(G, id)


####
# Brute force algorithm
# Finds all dominating sets and returns ones with minimum length.
####

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
    Finds all possible dominating sets in a given graph G. 
    """

    nodes_arr = G.nodes
    subsets = [list(S) for l in range(0, len(nodes_arr)) for S in itertools.combinations(nodes_arr, l+1)] # every possible set of vertices from G
    dom_sets = []

    for D in subsets: 
        if len(D) == len(G):
            dom_sets.append(tuple(D))
            continue

        if is_dom_set(G, D):
            dom_sets.append(tuple(D)) #list with every dominant set of given graph

    return dom_sets

def find_minimum_dom_sets(G):
    """
    Finds all the minimum dominant sets in a given graph G.
    """
    dom_sets = find_dom_sets(G)
    min_len = min([len(x) for x in dom_sets])
    min_sets = [x for x in dom_sets if len(x) == min_len]

    return min_sets

####
# Greedy heuristic:
# Find the first node with most edges and remove that and every node connected to it, update edges with removed nodes and move to the next one
# Repeat until the length of the node list is 0.
####

def greedy_min_dom_set(G):
    """
    Greedy heuristic based algorithm to find a minimum dominating set of graph G.
    """

    edges = [list(e) for e in G.edges]
    edge_count = {node : 0 for node in G.nodes} # node dictionary with edge counts -> {node: n_of_edges}

    removed_nodes = []

    while len(edge_count) > 0: # Iterates over nodes until there are none left

        # Counts the number of edges of each node
        for edge in edges:
            for node in list(edge_count.keys()):
                if node == edge[0] or node == edge[1]:
                    edge_count[node] += 1

        max_idx = list(edge_count.values()).index(max(edge_count.values())) # index of node with most edges
        node_to_rem = list(edge_count.keys())[max_idx] # Main node which will be removed
        removed_nodes.append(node_to_rem) # list of removed nodes which will be the minimum dominating set later
        
        adjacent_nodes= []

        for edge in reversed(edges):
            # Adds the adjacent node to a list and removes the main node edge
            if edge[0] == node_to_rem:
                adjacent_nodes.append(edge[1])
                edges.remove(edge)
            elif edge[1] == node_to_rem:
                adjacent_nodes.append(edge[0])
                edges.remove(edge) 

        # Removed adjacent nodes' edges
        for adj_node in adjacent_nodes:
            for edge in reversed(edges):
                if edge[0] == adj_node or edge[1] == adj_node:
                    edges.remove(edge)
        
        del edge_count[node_to_rem] # Remove main node from dictionary

        # Remove adjacent nodes from dictionary
        for adj_node in adjacent_nodes:
            del edge_count[adj_node]

        # Reset edge count with remaining nodes
        edge_count = {n:0 for n in edge_count}

    return removed_nodes



def run_brute_force():
    """
    Function to run and time the brute force algorithm. 
    """

    G_lst = read_Graphs() # Read all graphs in directory
    min_sets = []
    durations = []

    # Running the brute force algorithm and printing the minimum dominating sets
    
    for i in range(len(G_lst)):
        start = time.time() # Timing the duration of the algorithm
        min_set = find_minimum_dom_sets(G_lst[i][0])
        print("Graph {i} minimum dominating set:".format(i=i+1))
        print(min_set)
        end = time.time()
        min_sets.append(min_set)
        durations.append(end-start)

    print("Brute force done.")

    return min_sets, durations

def run_greedy_heuristic():
    """
    Function to run and time the greedy heuristic algorithm.
    """

    G_lst = read_Graphs()
    durations = []
    min_sets = []

    # Running the greedy heuristic algorithm and printing the minimum dominating sets
    for i in range(len(G_lst)):
        start = time.time() # Timing the duration of the algorithm
        min_set = greedy_min_dom_set(G_lst[i][0])
        print("Graph {i} minimum dominating set:".format(i=i+1))
        print(min_set)
        end = time.time()
        min_sets.append(min_set)
        durations.append(end-start)

    print("Greedy done.")

    return min_sets, durations

# Find min dominating sets using networkx and time it
def nx_algorithm():
    """
    Function to run and time the algorithm making use of networkx functions. 
    """

    G_lst = read_Graphs() # Read all graphs in directory
    durations = []
    min_sets = []

    # Running the greedy heuristic algorithm and printing the minimum dominating sets

    for i in range(len(G_lst)):
        start = time.time() # Timing the duration of the algorithm
        subsets = [list(S) for l in range(0, len(G_lst[i][0].nodes)) for S in itertools.combinations(G_lst[i][0].nodes, l+1)] # every possible subset of G
        dom_sets = [D for D in subsets if nx.is_dominating_set(G_lst[i][0], D)] # list with all dominant sets
        lengths = [len(D) for D in dom_sets] # list with set lenghts
        min_set = [D for D in dom_sets if len(D) == min(lengths)] # minimum dominating sets
        print("Graph {i} minimum dominating sets:".format(i=i+1))
        print(min_sets)
        end = time.time()
        min_sets.append(min_set)
        durations.append(end-start)

    print("nx done.")

    return min_sets, durations


# Create 10 graphs
# Then read them into list
p = 10
# create_bunch(p)
G_lst = read_Graphs()

def get_results():
    """
    Runs every algorithm and saves times, and averages to file.
    """

    # Running brute force algorithm
    brute_min_sets, brute_dur = run_brute_force()
    brute_dur_average = sum(brute_dur)/len(brute_dur)


    # Running the greedy heuristic algorithm
    greedy_sets, greedy_dur = run_greedy_heuristic()
    greedy_dur_average = sum(greedy_dur)/len(greedy_dur)

<<<<<<< HEAD
<<<<<<< HEAD
# Running networkx function based algorithm
nx_sets, nx_dur = nx_algorithm()
nx_dur_average = sum(nx_dur)/len(nx_dur)
=======
    print("here")
    print(greedy_sets)
    # Running networkx function based algorithm
    nx_sets, nx_dur = nx_algorithm()
    nx_dur_average = sum(nx_dur)/len(nx_dur)
>>>>>>> 34e6659 (update)
=======
    # Running networkx function based algorithm
    nx_sets, nx_dur = nx_algorithm()
    nx_dur_average = sum(nx_dur)/len(nx_dur)
>>>>>>> 27a20fdd0ff97d68d448ff19b2eeaf63d807505c

    with open('results.txt', 'w') as f:

        f.write("Brute force\n")
        f.write("Average {dur}\n".format(dur = round(brute_dur_average,7)))
        for dur in brute_dur: 
            f.write("{d}\t".format(d = dur))
        print("############")
        print("Brute force average running time: {dur} seconds.".format(dur = round(brute_dur_average,7)))
        print("############")
        print()

        f.write("\n\nGreedy heuristic\n".format(p = p))
        f.write("Average {dur}\n".format(dur = round(greedy_dur_average, 7)))
        for dur in greedy_dur: 
            f.write("{d}\t".format(d = dur))
        print("############")
        print("Greedy heuristic average running time: {dur} seconds.".format(dur = round(greedy_dur_average,7)))
        print("############")
        print()

        f.write("\n\nnx based algorithm\n".format(p = p))
        f.write("Average {dur}\n".format(dur = round(nx_dur_average, 7)))
        for dur in nx_dur: 
            f.write("{d}\t".format(d = dur))
        print("############")
        print("nx based algorithm average running time: {dur} seconds.".format(dur = round(nx_dur_average, 7)))
        print("############")

<<<<<<< HEAD
<<<<<<< HEAD
=======
=======
>>>>>>> 27a20fdd0ff97d68d448ff19b2eeaf63d807505c
def see_results():
    """
    Plots the times from get_results.
    """

    with open("results.txt", 'r') as f:
        lines = f.readlines()
        line_lst = []
        averages = []
        times = []

        for line in lines:
            line_lst.append(line.strip().split())

        for e in line_lst:
            if 'Average' in e:
                averages.append(float(e[1]))    
            
            if line_lst.index(e)%4 == 2:
                times.append([float(x) for x in e])

    print("Averages")
    print(averages)
    print("Times")
    print(times)

    graphs_n = [x for x in range(1,p+1)] 
    plt.plot(graphs_n, times[0], '-o', label= "Brute force")
    plt.plot(graphs_n, times[1], '-o', label = "Greedy heuristic")
    plt.plot(graphs_n, times[2], '-o', label = "nx function")
    plt.legend()
    plt.ylabel("Time (s)")
    plt.xlabel("Graph number")
    plt.xlim([0.8,10.2])
    plt.show()

<<<<<<< HEAD
#visualize_Graph(G_lst[1][0])
#see_results()
>>>>>>> 34e6659 (update)
=======
visualize_Graph(G_lst[1][0])
#see_results()
>>>>>>> 27a20fdd0ff97d68d448ff19b2eeaf63d807505c
