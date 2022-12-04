# Find the Mininimum Dominating Set
## Brute force and a greedy heuristic algorithm to find dominant sets of a graph.
### Project for a class of my masters which was very enjoyable and challenging.

 The brute force algorithm leaves much to be desired as it is very inefficent and with graphs around 60-70 nodes it starts taking a very long time. The goal of this is not to make the algorithm as efficient as possible so I did not try and make it the best possible and made it so that the function to verify if the set is dominant has a nest of 3 for loops.

 This is a optimization problem, with the graphs available in Git I'm getting around 0.56 seconds process time of the brute force algorithm and about 0.001 seconds with the greedy algorithm, which is a huge difference. However the greedy algorithm only provides 1 somewhat random minimum dominating set, while the brute force algorithm provides every minimum dominating set.

 Decided to compare the running time and algorithm complexity of my is_dom_set function to the networkx function is_dominating_set which is very efficient since it applies graph theory to the verification instead of manually checking the nodes and their connections.

## Random algorithms to find the minimum dominating sets of a graph.
### Back to this topic again, this time employing random and probabilistic algorithms.

For this project, the probabilities are uniform as only functions from module *random* were used. It is possible to alter the probabilities to favour certain set sizes or which node to pick, however this seemed pointless and so, it was not used.

To solve the problem, two different modifications of the greedy heuristic were used. One chooses random nodes and if it's a dominant set it is added to a list and in the end, only the smallest sets are kept and assumed the gamma sets. The other does the same but minimizes the size of the set. A third function, employing once again, functions from the module *networkx* were used, in a similar fashion to the previous project. However, the algorithm also minimizes the dominant sets until it finds a given number of sets.

One downside to these functions is that as the sets are randomized, it is possible to solve and find the wrong minimum dominant sets. This can be fixed, by finding a huge number of dominant sets of the graph, which, inevitably, will have some minimum dominant sets. This was not done because it would take a very long time to compute.

I'm pretty happy with the results of the implementation and this time around, it was much easier to solve the problem than on the first time. This can also be due to the familiarization with the problem in hand.

# Licensing and Disclaimer
#### Feel free to use this code as you see fit, for any questions related contact me via any contact detail on my profile page.
#### Disclaimer: this code was built from scratch by myself, however a huge contribution to the mental strategy needed for the implementation of the exhaustive search is thanks to the pseudo-code by 'ravenspoint' on the thread https://stackoverflow.com/questions/74081159/check-if-its-a-dominant-set-of-a-graph (last opened in: 11:11pm 11/06/2022 [MM/DD/YYYY]).
