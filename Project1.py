import numpy as np
import networkx as nx
import random as rand
import matplotlib.pyplot as plt

# Creating the graph and storing in a file
seed = 97639 # Student number
rand.seed(seed) # Sets new 'random' module seed

m = 20 # Number of edges
n = round(m/2) # Number of vertices, a fraction of the number of edges

def create_Graph():
    """
    Creates a new Graph object, and generates random n vertices and m edges. Vertices are separated by atleast 
    1 unit of each other
    """

    G = nx.Graph() # Initializes object
    seen_pos = set() # Set for existing position
    

    # First the nodes
    k=1
    G.add_node(k, pos=(rand.randint(1,20), rand.randint(1,20))) # Adds the first node

    while len(list(G)) < n:
    
        x,y = (rand.randint(1,20), rand.randint(1,20)) # Generates coordinates
        
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
                G.add_node(k, pos=(x,y)) # Adds node to graph
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

    while len(G.edges)<=m:
        u,v = (rand.randint(1,n), rand.randint(1,n)) # Creates first edge
        
        # Checks if u and v nodes are the same and corrects the 2nd node if they are
        if u == v: 
            v = rand.randint(1,n)
            continue
        
        if (u,v) not in seen_edge and (v,u) not in seen_edge: # (u,v) and (v,u) edges are the same
            G.add_edge(u,v)
            seen_edge.add((u,v))
            print("Edge added")

        else:
            print("Edge already exists")
    
    print("\n###########")
    print("All edges added to graph.")
    print("###########\n")

    return G

    
G = create_Graph()
print(nx.get_node_attributes(G, 'pos'))
print(G.edges)

# Draw Graph

fig, ax = plt.subplots()
nx.draw_networkx(G, pos= nx.get_node_attributes(G, 'pos'), with_labels = True)
ax.tick_params(left = True, bottom = True, labelleft = True, labelbottom = True)

plt.xlabel("x")
plt.ylabel("y")
plt.title("Unidirected Graph G(V,E)")

plt.show()