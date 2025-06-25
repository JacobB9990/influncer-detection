# Centrality Measures Report

## Introduction
Centrality measures in social networks help identify the most important, or influential, nodes within a network. Freeman’s paper points out three types of centrality: **degree**, **closeness**, and **betweeness** centrality. This report explores these measures in the context of three simple graph structures: a **star** graph, a **chain** graph, and a **clique** graph.


### 1. Degree Centrality
Is the simplest measure, counting the number of direct connections a node has.

#### Formula:
$$
C_D(p_k) = \sum_{i=1}^{n} a(p_i, p_k)
$$

where $a(p_i, p_k)$ is 1 if nodes $p_i$ and $p_k$ are connected, else 0.

---

### 2. Closeness Centrality
Is a measure of how close a node is to all other nodes in the network. It is defined as the inverse of the average distance from a node to all other nodes.

#### Formula:

$$
C_C(p_k) = \frac{n-1}{\sum_{i=1}^{n} d(p_i, p_k)}
$$

where $d(p_i, p_k)$ is the shortest path distance.

---

### 3. Betweenness Centrality
Is a measure of how often a node acts as a bridge along the shortest path between two other nodes. It is defined as the sum of the fraction of all-pairs shortest paths that pass through a given node.

#### Formula:

$$
C_B(p_k) = \sum_{\substack{i,j=1 \\ i \neq j \neq k}}^{n} \frac{g_{ij}(p_k)}{g_{ij}}
$$

where $g_{ij}$ is the number of shortest paths between $p_i$ and $p_j$, and $g_{ij}(p_k)$ is the number passing through $p_k$.

---

### 4. Results
The following table summarizes the centrality measures for each graph structure:

#### Star Graph
| Node | Degree (norm) | Degree (raw) | Closeness (norm) | Betweenness (norm) | Betweenness (raw) |
| ---- | ------------- | ------------ | ---------------- | ------------------ | ----------------- |
| A    | 1.00          | 4.00         | 1.00             | 1.00               | 6.00              |
| B    | 0.25          | 1.00         | 0.57             | 0.00               | 0.00              |
| C    | 0.25          | 1.00         | 0.57             | 0.00               | 0.00              |
| D    | 0.25          | 1.00         | 0.57             | 0.00               | 0.00              |
| E    | 0.25          | 1.00         | 0.57             | 0.00               | 0.00              |

##### Interpretation:
Node **A** is the most central node in the star graph, having the highest degree, closeness, and betweenness centrality in all cases. Imagine a star with **A** at the center and **B**, **C**, **D**, and **E** as the outer nodes, or just look at ```./test_graphs/star_graph.md```. The outer nodes have only one connection to the center, making them less central.

#### Chain Graph
| Node | Degree (norm) | Degree (raw) | Closeness (norm) | Betweenness (norm) | Betweenness (raw) |
| ---- | ------------- | ------------ | ---------------- | ------------------ | ----------------- |
| A    | 0.25          | 1.00         | 0.40             | 0.00               | 0.00              |
| B   | 0.50          | 2.00         | 0.57             | 0.50               | 3.00              |
| C    | 0.50          | 2.00         | 0.67             | 0.67               | 4.00              |
| D    | 0.50          | 2.00         | 0.57             | 0.50               | 3.00              |
| E    | 0.25          | 1.00         | 0.40             | 0.00               | 0.00              |

##### Interpretation:
Node **B**, **C**, and **D** have the highest degree and closeness centrality in the chain graph, with **B** and **D** being the endpoints. Node **C** has the highest betweenness centrality, as it lies between **B** and **D**. The chain graph can be visualized as a linear arrangement of nodes, where each node connects to its immediate neighbors.

#### Clique Graph
| Node | Degree (norm) | Degree (raw) | Closeness (norm) | Betweenness (norm) | Betweenness (raw) |
| ---- | ------------- | ------------ | ---------------- | ------------------ | ----------------- |
| A    | 1.00          | 3.00         | 1.00             | 0.00               | 0.00              |
| B    | 1.00          | 3.00         | 1.00             | 0.00               | 0.00              |
| C    | 1.00          | 3.00         | 1.00             | 0.00               | 0.00              |
| D    | 1.00          | 3.00         | 1.00             | 0.00               | 0.00              |

##### Interpretation:
All nodes in the clique graph have equal degree, closeness, and betweenness centrality. This is because every node is connected to every other node, making them equally central. The clique graph can be visualized as a complete graph where each node connects to all others, leading to uniform centrality measures across all nodes.

---
### 5. Discussion
Each centrality measure provides a different perspective on node importance. In the star graph, the center node is clearly the most central, while in the chain graph, nodes in the middle have higher centrality than those at the ends. The clique graph shows uniform centrality due to complete connectivity.

Other than that, each centrality measure provides a unique insight into the structure, dynamics, etc of the network. Degree centrality is pretty straightforward but may overlook the importance of nodes that connect parts of the network. Closeness centrality shows how quickly a node can reach others, while betweenness centrality points out nodes that connect different parts of the network.

---

## References

Freeman, L. C. (1979). *Centrality in social networks: Conceptual clarification*. **Social Networks, 1**(3), 215–239. [https://doi.org/10.1016/0378-8733(78)90021-7](https://doi.org/10.1016/0378-8733(78)90021-7)