# The Centrality Index of a Graph (Sabidussi, 1966)

## Introduction
Sabidussi (1966) introduced the centrality index as a way to measure how central a node is in a graph, based on its distances to all other nodes. This concept laid the groundwork for later centrality measures, including closeness and betweenness centrality.

## 1. Centrality Index Definition
The centrality index of a node is defined as the inverse of the sum of shortest path distances from that node to all other nodes:

$$
C_{SI}(v) = \frac{1}{\sum_{u \neq v} d(v, u)}
$$

where $d(v, u)$ is the shortest path distance between nodes $v$ and $u$.

## 2. Example Calculation
For a simple chain graph with 5 nodes:
- Node 0: $C_{SI}(0) = 1 / (1+2+3+4) = 1/10 = 0.1$
- Node 2 (middle): $C_{SI}(2) = 1 / (2+1+1+2) = 1/6 = 0.1667$

## 3. Results
| Node | Centrality Index |
|------|------------------|
| 0    | 0.1000           |
| 1    | 0.1429           |
| 2    | 0.1667           |
| 3    | 0.1429           |
| 4    | 0.1000           |

## 4. Discussion
Nodes in the center of the graph have higher centrality index values, reflecting their shorter average distance to all other nodes. This measure is closely related to closeness centrality, but is one of the earliest formalizations of the idea.

## References
Sabidussi, G. (1966). The centrality index of a graph. Psychometrika, 31(4), 581–603. https://doi.org/10.1007/BF02289527
