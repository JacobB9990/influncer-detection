# Goal: measure degree centrality.

from typing import Dict, List

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
    'A': ['B', 'C', 'D'],
    'B': ['A', 'C', 'D'],
    'C': ['A', 'B', 'D'],
    'D': ['A', 'B', 'C'],
}

def degree_centrality(graph: Graph, normalize: bool = False) -> Dict[str, float]:
    n = len(graph)
    centrality = {}
    for node in graph:
        degree: int = len(graph[node])
        if normalize:
            degree_norm = degree / (n - 1)
            centrality[node] = degree_norm
        else:
            centrality[node] = degree
    return centrality


for name, G in [('Star', G_star), ('Chain', G_chain), ('Clique', G_clique)]:
    print(f'\n{name} graph:')
    results = degree_centrality(G, normalize=True)
    for node, centrality in results.items():
        print(f'Node {node}: {centrality:.2f}')
