import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

pd.options.mode.chained_assignment = None  # default='warn'

cwdir = os.getcwd()+"/results/"

data = {entry.name[:-12]: {} for entry in os.scandir(cwdir)}

# using arrays as it is faster to compute than Python lists
statistical_experiment_graph = {'random_nodes': np.array([{'True':0, 'False':0},[]]), 
                                'random_size': np.array([{'True':0, 'False':0},[]]), 
                                'nx': np.array([{'True':0, 'False':0},[]])}

# saving first as dictionaries to later convert to dataframes
for entry in os.scandir(cwdir):
    # iterates over entries in working directory
    if entry.name == 'SWmediumEWD_results.txt':
        with open(entry, 'r') as f:
            k = int(f.readline().strip().split()[-2]) # saves k: the number of trials
            algorithm = 'random_nodes' # dictionary key to access and change information
            f.readline()
            lines = f.readlines()
            for line in lines[:-2]:
                # iterates over lines
                if "(G, p= 20)" in line: 
                    algorithm = line[:-24] # selects the algorithm used from the line
                elif line.startswith("threshold"): # this is the columns header
                    continue
                else: # saves information in text file to dictionary
                    info = line.strip().split("\t")
                    # info[0] = 'True' increments the key True by 1, the same for False 
                    statistical_experiment_graph[algorithm][0][info[0]] += 1
                    # append duration to list
                    statistical_experiment_graph[algorithm][1].append(float(info[1]))
    else:
        with open(entry, 'r') as f:
            for i in range(4): # skips first 4 lines
                f.readline()
            lines = f.readlines()
            for line in lines:
                # Graph information
                if line.startswith("Graph"):    
                    graph_info = line.strip().split()
                    folder = graph_info[1].split("/")[0] # splits xx/yy at the '/'
                    graph_name_list = graph_info[1].split("/")[1][:-4] # splits at same spot and removes '.txt'
                    if 'facebook_combined' in graph_name_list:
                        graph_name = graph_name_list[0]
                    graph_name = graph_name_list[0:5]+" "+graph_name_list[5:]
                    # assigns information to graph dictionary
                    data[entry.name[:-12]][graph_name] = {}
                    data[entry.name[:-12]][graph_name]['nodes'] = int(graph_info[3])
                    data[entry.name[:-12]][graph_name]['edges'] = int(graph_info[-2])
                # adds threshold and duration values of graph
                elif line.startswith("threshold"):
                    data[entry.name[:-12]][graph_name]['threshold'] = bool(line.strip().split(": ")[-1] == 'True')
                elif line.startswith("duration"):
                    data[entry.name[:-12]][graph_name]['duration'] = float(line.strip().split()[-1])

#####
# Analysis
#####

# lets start with the different graph results
grouped_data = {entry.name.split('_')[0]: None for entry in os.scandir(cwdir)} # values as None for now as we will assign the dataframes after
del grouped_data['SWmediumEWD'] # this information will not be added as dataframe
del grouped_data['custom']
grouped_data['custom_tinyG'] = None # renaming 'custom' to 'custom_tinyG' so it collects data from the other dictionary
del grouped_data['SW']
grouped_data['SW_Graphs'] = None # do the same for SW graphs

for key in grouped_data.keys():
    first_df1 = pd.DataFrame(data[key+'_random_nodes']).T
    V_and_E = first_df1[['nodes', 'edges']]
    df1 = first_df1[['threshold', 'duration']]
    df2 = pd.DataFrame(data[key+'_random_size']).T
    # drop 'nodes' and 'edges' for both df2 and df3 and there is already those columns in df1
    df2.drop(['nodes', 'edges'], axis = 1, inplace = True)
    df3 = pd.DataFrame(data[key+'_nx']).T
    df3.drop(['nodes', 'edges'], axis=1, inplace= True)
    grouped_data[key] = pd.concat([V_and_E, df1, df2, df3], axis = 1, keys = ['','random nodes', 'random size', 'nx'])
    grouped_data[key] = grouped_data[key].reindex(sorted(grouped_data[key].index, key = len))
    grouped_data[key] = grouped_data[key].apply(pd.to_numeric, errors = 'coerce') # convert every element to numeric so we're able to use them in numeric functions; ex: correlation matrix
    
    # some data engineering
    # adds a new columns 'E/V ratio' which is the edge to node ratio
    grouped_data[key][('','E/V ratio')] = grouped_data[key][('','edges')]/grouped_data[key][('','nodes')].astype(float).round(1)
    # sorts columns
    cols = list(grouped_data[key])
    cols=cols[0:2]+[cols[-1]]+ cols[2:-1]
    grouped_data[key] = grouped_data[key][cols]


###
# Correlation matrices
###
# not very useful to plot all of the matrices at once as it is very hard to understand each one
# for i in range(len(grouped_data)):
#     plt.subplot(3,3,i+1)
#     sns.heatmap(grouped_data[list(grouped_data.keys())[i]].corr())
#     plt.suptitle("Correlation matrices")
# plt.show()


# here we can see how the number of edges increases exponentially with the number of nodes
# for i in range(len(grouped_data)):
#     plt.subplot(3,3,i+1)
#     plt.suptitle("Relationship between nodes, edges and their ratio")
#     plt.plot(grouped_data[list(grouped_data.keys())[i]][[('','nodes'),('','edges'),('','E/V ratio')]])
#     plt.title(list(grouped_data.keys())[i])
#     plt.legend(['number of nodes', 'number of edges', 'E/V ratio'])
#     if len(grouped_data[list(grouped_data.keys())[i]]) > 15:
#         plt.xticks(range(1, len(grouped_data[list(grouped_data.keys())[i]])+1, 20), list(range(1, len(grouped_data[list(grouped_data.keys())[i]])+1, 20)))
#     else:
#         plt.xticks(rotation = 'vertical')
#     plt.xlabel("Graph")
#     plt.ylabel("Value")
# plt.show()


# here we can see better the relation between the ratio and the number of nodes 
# for i in range(len(grouped_data)):
#     plt.subplot(3,3,i+1)
#     plt.suptitle("Relationship between nodes, edges and their ratio")
#     plt.plot(grouped_data[list(grouped_data.keys())[i]][[('','nodes'),('','E/V ratio')]])
#     plt.title(list(grouped_data.keys())[i])
#     plt.legend(['number of nodes', 'number of edges', 'E/V ratio'])
#     if len(grouped_data[list(grouped_data.keys())[i]]) > 15:
#         plt.xticks(range(1, len(grouped_data[list(grouped_data.keys())[i]])+1, 20), list(range(1, len(grouped_data[list(grouped_data.keys())[i]])+1, 20)))
#     else:
#         plt.xticks(rotation = 20)
#     plt.xlabel("Graph")
#     plt.ylabel("Value")
# plt.show()


# we can see the difference in runtimes of each algorithm
# for i in range(len(grouped_data)):
#     plt.subplot(3,3,i+1)
#     plt.suptitle("Algorithm runtime for each graph")
#     plt.plot(grouped_data[list(grouped_data.keys())[i]][[('random nodes','duration'),('random size','duration'),('nx','duration')]])
#     plt.title(list(grouped_data.keys())[i])
#     plt.legend(['random nodes', 'random size', 'nx'])
#     if len(grouped_data[list(grouped_data.keys())[i]]) > 15:
#         plt.xticks(range(1, len(grouped_data[list(grouped_data.keys())[i]])+1, 20), list(range(1, len(grouped_data[list(grouped_data.keys())[i]])+1, 20)))
#     else:
#         plt.xticks(rotation = 20)
#     plt.xlabel("Graph")
#     plt.ylabel("Seconds")
# plt.show()

# now the histograms 
# for i in range(len(grouped_data)):
#     plt.subplot(3,3,i+1)
#     plt.suptitle("Algorithm runtime for each graph")
#     sns.histplot(grouped_data[list(grouped_data.keys())[i]][[('random nodes','duration'),('random size','duration'),('nx','duration')]], bins=10)
#     plt.title(list(grouped_data.keys())[i])
#     plt.legend(['random nodes', 'random size', 'nx'])
#     plt.xlabel("Seconds")
#     plt.ylabel("Count")
# plt.show()

# now without nx algorithm as that is much faster than the other two
# for i in range(len(grouped_data)):
#     plt.subplot(3,3,i+1)
#     plt.suptitle("Algorithm runtime for each graph")
#     sns.histplot(grouped_data[list(grouped_data.keys())[i]][[('random nodes','duration'),('random size','duration')]], bins=25, kde = True)
#     plt.title(list(grouped_data.keys())[i])
#     plt.legend(['random nodes', 'random size'])
#     plt.xlabel("Seconds")
#     plt.ylabel("Count")
# plt.show()


# now to study the graph that was put through each algorithm n = 1000 times
# for key in statistical_experiment_graph.keys():
#     plt.title("Each algorithm runtime for the graph SWmediumEWD")
#     sns.histplot(statistical_experiment_graph[key][1], bins = 25, kde = True)
#     plt.legend(['random nodes', 'random size', 'nx'])
#     plt.ylabel("Seconds")
# plt.show()

# now again without the nx algorithm
# for key in statistical_experiment_graph.keys():
#     if key == 'nx':
#         continue
#     plt.subplot(1,2,1)
#     plt.title("Non normalized distribution")
#     sns.histplot(data = statistical_experiment_graph[key][1], bins = 50, kde = True)
#     plt.legend(['random nodes', 'random size'])
    
    
#     plt.subplot(1,2,2)
#     plt.title("Normalized distribution")
#     sns.histplot(data = statistical_experiment_graph[key][1], bins = 50, kde = True, stat='density')
#     plt.legend(['random nodes', 'random size'])
#     plt.ylabel("Seconds")
# plt.show()

print("###############\nMeans\n###############")
means = []
for key in statistical_experiment_graph.keys():
    #means
    x_mean = round(np.mean(statistical_experiment_graph[key][1]),5)
    print("{key} mean: {x_mean}".format(key = key, x_mean = x_mean))
    #medians
    x_mean = round(np.median(statistical_experiment_graph[key][1]),5)
    print("{key} median: {x_mean}".format(key = key, x_mean = x_mean))
    #standard deviations
    x_mean = round(np.std(statistical_experiment_graph[key][1]),5)
    print("{key} std: {x_mean}".format(key = key, x_mean = x_mean))
    # variances
    x_mean = round(np.var(statistical_experiment_graph[key][1]),5)
    print("{key} var: {x_mean}".format(key = key, x_mean = x_mean))
