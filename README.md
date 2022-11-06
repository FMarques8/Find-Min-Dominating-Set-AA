# Find-Min-Dominating-Set-AA
### Brute force and a greedy heuristic algorithm to find dominant sets of a graph.
### Project for a class of my masters which I'm enjoying a lot and is being challenging.

### The brute force algorithm leaves much to be desired as it is very inefficent and with graphs around 60-70 nodes it starts taking a very long time. The goal of this is not to make the algorithm as efficient as possible so I did not try and make it the best possible and made it so that the function to verify if the set is dominant has a nest of 3 for loops.
### This is a optimization problem, with the graphs available in Git I'm getting around 0.56 second process time of the brute force algorithm and about 0.001 seconds with the greedy algorithm, which is a huge difference. However the greedy algorithm only provides 1 somewhat random minimum dominating set, while the brute force algorithm provides every minimum dominating set.

### Decided to compare the running time and algorithm complexity of my is_dom_set function to the networkx function is_dominating_set which is very efficient since it applies graph theory to the verification instead of manually checking the nodes and their connections.

### Feel free to use this code as you see fit, for any questions related contact me via any contact detail on my profile page.
### Disclaimer: this code was built from scratch by myself, however a huge contribution to the mental strategy needed for the implementation is thanks to the pseudo-code by 'ravenspoint' on the thread https://stackoverflow.com/questions/74081159/check-if-its-a-dominant-set-of-a-graph (last opened in: 11:11pm 11/06/2022 [MM/DD/YYYY]).
