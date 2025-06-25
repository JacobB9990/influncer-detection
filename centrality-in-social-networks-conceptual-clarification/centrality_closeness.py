# Goal: find degree closeness centrality.

from typing import Dict, List
from collections import deque

Graph = Dict[str, List[str]]

G_star: Graph = {
    "A": ["B", "C", "D", "E"],
    "B": ["A"],
    "C": ["A"],
    "D": ["A"],
    "E": ["A"],
}

G_chain: Graph = {
    "A": ["B"],
    "B": ["A", "C"],
    "C": ["B", "D"],
    "D": ["C", "E"],
    "E": ["D"],
}

G_clique: Graph = {
    "A": ["B", "C", "D"],
    "B": ["A", "C", "D"],
    "C": ["A", "B", "D"],
    "D": ["A", "B", "C"],
}


def bfs_distances(G: Graph, start: str):
    dist = {node: float("inf") for node in G}
    dist[start] = 0
    queue = deque([start])

    while queue:
        v = queue.popleft()
        for neighbor in G[v]:
            if dist[neighbor] == float("inf"):
                dist[neighbor] = dist[v] + 1
                queue.append(neighbor)
    return dist


def closeness_centrality(G: Graph) -> Dict[str, float]:
    n = len(G)
    centrality = {}

    for node in G:
        dist = bfs_distances(G, node)
        total_dist = sum(d for d in dist.values() if d < float("inf") and d > 0)
        if total_dist > 0:
            centrality[node] = (n - 1) / total_dist
        else:
            centrality[node] = 0.0
    return centrality

print("Closeness Centrality Results:")
for name, G in [("Star", G_star), ("Chain", G_chain), ("Clique", G_clique)]:
    print(f"\n{name} graph:")
    results = closeness_centrality(G)
    for node, centrality in results.items():
        print(f"Node {node}: {centrality:.2f}")
