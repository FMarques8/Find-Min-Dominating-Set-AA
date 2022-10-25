import numpy as np
import networkx as nx
import random as rand
import matplotlib.pyplot as plt

# Creating the graph and storing in a file
seed = 97639 # Student number
rand.seed(seed) # Sets new 'random' module seed

m = 20 # Number of edges
n = round(m/4) # Number of vertices, a fraction of the number of edges

def create_Graph():
    """Creates a new Graph object, and generates random n vertices and m edges. Vertices are separated by atleast 
    1 unit of each other"""

    G = nx.Graph() # Initializes object
    seen_pos = set() # Set for existing position

    # First the nodes
    for i in range(1,n+1):
        x,y = (rand.randint(1,20), rand.randint(1,20)) # Generates coordinates
        
        if i ==1: 
            G.add_node(1, pos=(x,y))
            continue


        if (x,y) not in seen_pos:
            tmp = list(nx.get_node_attributes(G, 'pos').values())

            # Iterates over the temporary node position list
            for j in range(0,len(tmp)):
                x_tmp, y_tmp = tmp[j]
                can_add = True

                # Checks if x and y are atleast 1 unit away from other nodes' x and y
                if abs(x - x_tmp) >= 1 and abs(y - y_tmp)>= 1:
                    can_add = True

                else:
                    can_add = False
                    break

            if can_add:
                G.add_node(i, pos=(x,y))
                seen_pos.add((x,y))
                print("Node added.")

            else: 
                print("Node too close.")

    # Now the edges


    return G

    
G = create_Graph()
print(nx.get_node_attributes(G, 'pos'))
