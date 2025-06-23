# Centrality Measures Report

## Introduction
Centrality measures in social networks help identify the most important, or influential, nodes within a network. Freeman’s paper points out three types of centrality: **degree**, **closeness**, and **betweeness** centrality. This report explores these measures in the context of three simple graph structures: a **star** graph, a **chain** graph, and a **clique** graph.


### 1. Degree Centrality
Is the simplest measure, counting the number of direct connections a node has.

#### Formula:
$$
C_D(p_k) = \sum_{i=1}^{n} a(p_i, p_k)
$$

where $ a(p_i, p_k) $ is 1 if nodes $ p_i $ and $ p_k $ are connected, else 0.

---

### 2. Closeness Centrality
Is a measure of how close a node is to all other nodes in the network. It is defined as the inverse of the average distance from a node to all other nodes.
#### Formula:

$$
C_C(p_k) = \frac{n-1}{\sum_{i=1}^{n} d(p_i, p_k)}
$$

where $ d(p_i, p_k) $ is the shortest path distance.

---

### 3. Betweenness Centrality
Is a measure of how often a node acts as a bridge along the shortest path between two other nodes. It is defined as the sum of the fraction of all-pairs shortest paths that pass through a given node.
#### Formula:

$$
C_B(p_k) = \sum_{\substack{i,j=1 \\ i \neq j \neq k}}^{n} \frac{g_{ij}(p_k)}{g_{ij}}
$$

where $ g_{ij} $ is the number of shortest paths between $ p_i $ and $ p_j $, and $ g_{ij}(p_k) $ is the number passing through $ p_k $.


## References

Freeman, L. C. (1979). *Centrality in social networks: Conceptual clarification*. **Social Networks, 1**(3), 215–239. [https://doi.org/10.1016/0378-8733(78)90021-7](https://doi.org/10.1016/0378-8733(78)90021-7)
