import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

cwdir = os.getcwd()+"/results/"

data = {entry.name[:-12]: {} for entry in os.scandir(cwdir)}

# using arrays as it is faster to compute than Python lists
statistical_experiment_graph = {'random_nodes': np.array([{True:0, False:0},[]]), 
                                'random_size': np.array([{True:0, False:0},[]]), 
                                'nx': np.array([{True:0, False:0},[]])}

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
                    statistical_experiment_graph[algorithm][0][info[0]=='True'] += 1
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
                    graph_name = graph_info[1].split("/")[1][:-4] # splits at same spot and removes '.txt'
                    # assigns information to graph dictionary
                    data[entry.name[:-12]][graph_name] = {}
                    data[entry.name[:-12]][graph_name]['nodes'] = int(graph_info[3])
                    data[entry.name[:-12]][graph_name]['edges'] = int(graph_info[-2])
                # adds threshold and duration values of graph
                elif line.startswith("threshold"):
                    data[entry.name[:-12]][graph_name]['threshold'] = bool(line.split(":")[-1] == 'True')
                elif line.startswith("duration"):
                    data[entry.name[:-12]][graph_name]['duration'] = float(line.split(":")[-1] == 'True')

data['SWmediumEWD'] = statistical_experiment_graph
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
    grouped_data[key] = pd.concat([V_and_E, df1, df2, df3], axis = 1, keys = ['','random nodes', 'random_size', 'nx'])

print(grouped_data['BD0'])

# grouped_data['BD0'].apply(grouped_data['BD0']['node'] / grouped_data['BD0']['edges'] ,axis = 1)