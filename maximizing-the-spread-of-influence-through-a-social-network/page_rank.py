import networkx as nx
import random
from typing import List, Set


def generate_graph(
    n: int = 100, m: int = 2
) -> nx.DiGraph:  # This is here just incase/running independently
    G = nx.barabasi_albert_graph(n, m)
    directed_G = G.to_directed()

    for node in directed_G.nodes():
        in_edges = list(directed_G.in_edges(node))
        total = len(in_edges)
        for u, v in in_edges:
            if total > 0:
                directed_G[u][v]["weight"] = 1 / total
            else:
                directed_G[u][v]["weight"] = 0.0

    return directed_G

def run_ic(G: nx.DiGraph, seeds: List[int]) -> Set[int]:
    active = set(seeds)
    newly_active = set(seeds)

    while newly_active:
        next_active = set()
        for node in newly_active:
            for neighbor in G.successors(node):
                if neighbor not in active:
                    p = G[node][neighbor].get("weight", 0.1)
                    if random.random() < p:
                        next_active.add(neighbor)
        newly_active = next_active
        active.update(newly_active)
    return active

def estimate_spread(G: nx.DiGraph, seeds: List[int], simulations: int = 1000) -> float:
    total_spread = 0
    for _ in range(simulations):
        active = run_ic(G, seeds)
        total_spread += len(active)
    return total_spread / simulations


def top_pagerank_nodes(G: nx.DiGraph, k: int) -> Set[int]:
    pr = nx.pagerank(G, alpha=0.85)
    top_k = sorted(pr, key=pr.get, reverse=True)[:k]

    return top_k


def run_simulation(n: int = 100, m: int = 2, k: int = 4, simulations: int = 1000 , G: nx.DiGraph = None) -> None:
    if G is None:
        G = generate_graph(n, m)

    seeds = top_pagerank_nodes(G, k)
    spread = estimate_spread(G, seeds, simulations)

    print("PageRank Seed Set:", seeds)
    print("Estimated Spread (IC):", spread)
