from matplotlib import pyplot as plt
import networkx as nx
from typing import Dict

def centrality_index(graph: nx.Graph) -> Dict[int, float]:
    centrality = {}
    for node in graph.nodes():
        path_lengths = nx.single_source_shortest_path_length(graph, node)
        total_length = sum(path_lengths.values())
        centrality[node] = 1 / total_length if total_length > 0 else 0.0
    return centrality

graph: nx.Graph = nx.path_graph(5)

nx.draw(graph, with_labels=True)
plt.show()

print("Nodes:", graph.nodes())
print("Centrality Index:")
for node, value in centrality_index(graph).items():
    print(f"Node {node}: {value:.4f}")
