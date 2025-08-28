import networkx as nx
import numpy as np
from typing import Tuple, Dict, Hashable, Mapping

def hits_algorithm(
    graph: nx.DiGraph, max_iter: int = 100, tol: float = 1e-8
) -> Tuple[Dict[str, float], Dict[str, float]]:
    
    nodes = list(graph.nodes())
    n = len(nodes)
    authority = np.ones(n)
    hub = np.ones(n)

    for _ in range(max_iter):
        updated_authority = np.array([
            sum(hub[nodes.index(neighbor)] for neighbor in graph.predecessors(node))
            for node in nodes
        ])
        updated_hub = np.array([
            sum(authority[nodes.index(neighbor)] for neighbor in graph.successors(node))
            for node in nodes
        ])

        norm_auth = np.linalg.norm(updated_authority)
        norm_hub = np.linalg.norm(updated_hub)
        updated_authority /= norm_auth if norm_auth > 0 else 1
        updated_hub /= norm_hub if norm_hub > 0 else 1

        if np.allclose(authority, updated_authority, atol=tol) and np.allclose(hub, updated_hub, atol=tol):
            break

        authority = updated_authority
        hub = updated_hub

    return dict(zip(nodes, authority)), dict(zip(nodes, hub))

def pagerank(
    graph: nx.DiGraph, alpha: float = 0.85, max_iter: int = 100, tol: float = 1e-8
) -> Mapping[Hashable, float]:
    
    return nx.pagerank(graph, alpha=alpha, max_iter=max_iter, tol=tol)

graph: nx.DiGraph = nx.DiGraph()

edges = [
    ("A", "B"),
    ("A", "C"),
    ("B", "C"),
    ("C", "A"),
    ("D", "C"),
    ("E", "C"),
    ("E", "D")
]
graph.add_edges_from(edges)

print("Nodes:", graph.nodes())
print("HITS Authority Scores:")
authority, hub = hits_algorithm(graph)

for node in graph.nodes():
    print(f"Node {node}: Authority = {authority[node]:.4f}, Hub = {hub[node]:.4f}")

print("\nPageRank Scores:")
pagerank_scores = pagerank(graph)

print("\nPageRank Scores:")
for node, score in pagerank_scores.items():
    print(f"Node {node}: PageRank = {score:.4f}")