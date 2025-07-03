# kcore_analysis.py
import networkx as nx
from typing import Dict

def load_and_rank_graph(path: str):
    G = nx.read_edgelist(path, nodetype=int)
    G.remove_edges_from(nx.selfloop_edges(G))

    core_numbers = nx.core_number(G)
    degree_numbers = nx.degree_centrality(G)
    sorted_nodes = sorted(G.nodes(), key=lambda n: (core_numbers[n], degree_numbers[n]), reverse=True)
    return G, core_numbers, degree_numbers, sorted_nodes

if __name__ == "__main__":
    G, core_numbers, degree_numbers, sorted_nodes = load_and_rank_graph("Identification-of-infuentail-spreaders-in-complex-networks/data/email-Eu-core.txt")
    print("Top nodes by Core Number and Degree Centrality:")
    for node in G.nodes():
        print(f"Node {node:2d}: Core = {core_numbers[node]}, Degree Centrality = {degree_numbers[node]:.2f}")
