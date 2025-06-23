# Goal: measure degree centrality in a star graph.

G = {
    'A': ['B', 'C', 'D', 'E'],
    'B': ['A'],
    'C': ['A'],
    'D': ['A'],
    'E': ['A']
}

def degree_centrality(graph):
    for node in graph:
        degree = len(graph[node])
        print(f"Node {node} has degree centrality: {degree}")
        
degree_centrality(G)