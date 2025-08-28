# Goal: measure betweenness centrality.

from typing import Dict, List
from collections import deque, defaultdict
from itertools import combinations

Graph = Dict[str, List[str]]

G_star: Graph = {
    'A': ['B', 'C', 'D', 'E'],
    'B': ['A'],
    'C': ['A'],
    'D': ['A'],
    'E': ['A']
}

G_chain: Graph = {
    'A': ['B'],
    'B': ['A', 'C'],
    'C': ['B', 'D'],
    'D': ['C', 'E'],
    'E': ['D'],
}

G_clique: Graph = {
    "A": ["B", "C", "D"],
    "B": ["A", "C", "D"],
    "C": ["A", "B", "D"],
    "D": ["A", "B", "C"],
}


def bfs_shortest_paths(graph: Graph, start: str):
    queue = deque([[start]])
    shortest_paths = defaultdict(list)
    shortest_paths[start].append([start])
    visited_depth = {start: 0}

    while queue:
        path = queue.popleft()
        current = path[-1]
        for neighbor in graph[current]:
            depth = len(path)
            if neighbor not in visited_depth or depth < visited_depth[neighbor]:
                visited_depth[neighbor] = depth
                shortest_paths[neighbor] = [path + [neighbor]]
                queue.append(path + [neighbor])
            elif depth == visited_depth[neighbor]:
                shortest_paths[neighbor].append(path + [neighbor])
    return shortest_paths


def degree_betweenness(graph: Graph, normalize: bool = False):
    centrality = {node: 0.0 for node in graph}
    nodes = list(graph.keys())

    for s, t in combinations(nodes, 2):
        all_paths = bfs_shortest_paths(graph, s)[t]
        total_paths = len(all_paths)
        if total_paths == 0:
            continue
        for path in all_paths:
            for node in path[1:-1]:  
                centrality[node] += 1 / total_paths
    if normalize:
        n = len(graph)
        for node in centrality:
            centrality[node] /= (n - 1) * (n - 2) / 2
    return centrality

print("Degree Betweenness Centrality Results:")
for name, G in [("Star", G_star), ("Chain", G_chain), ("Clique", G_clique)]:
    print(f"\n{name} graph:")
    results = degree_betweenness(G, normalize=False)
    for node, centrality in results.items():
        print(f"Node {node}: {centrality:.2f}")
