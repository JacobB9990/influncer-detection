import networkx as nx
from typing import Dict

Graph = nx.DiGraph
PageRankScores = Dict[int, float]


def create_sample_graph() -> Graph:
    # Create a sample directed graph similar to the web.
    G = nx.scale_free_graph(1000, seed=42)
    return nx.DiGraph(G)


def pagerank(graph: Graph, alpha: float = 0.85, max_iter: int = 100, tol: float = 1.0e-6) -> PageRankScores:
    N: int = graph.number_of_nodes()
    # Initialize scores uniformly
    PR: PageRankScores = {v: 1.0 / N for v in graph.nodes()}

    for _ in range(max_iter):
        newPR: PageRankScores = {v: (1 - alpha) / N for v in graph.nodes()}

        for u in graph.nodes():
            out_degree: int = graph.out_degree(u)
            if out_degree == 0:
                for v in graph.nodes():
                    newPR[v] += alpha * PR[u] / N
            else:
                share: float = PR[u] / out_degree
                for v in graph.successors(u):
                    newPR[v] += alpha * share

        diff: float = sum(abs(newPR[v] - PR[v]) for v in graph.nodes())
        PR = newPR
        if diff < tol:
            break

    # Normalize
    norm: float = sum(PR.values())
    for v in PR:
        PR[v] /= norm

    return PR


if __name__ == "__main__":
    G: Graph = create_sample_graph()
    pagerank_scores: PageRankScores = pagerank(G)

    top_nodes = sorted(pagerank_scores.items(), key=lambda x: x[1], reverse=True)[:10]
    print("Top 10 nodes by PageRank:")
    for node, score in top_nodes:
        print(f"Node {node}: {score:.6f}")