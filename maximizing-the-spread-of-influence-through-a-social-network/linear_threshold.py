# This is for the Linear Threshold Model
import networkx as nx
import random
from matplotlib import pyplot as plt
from typing import List, Set, Optional


def generate_graph(n: int = 100, m: int = 2) -> nx.DiGraph:
    G = nx.barabasi_albert_graph(n, m)
    directed_G = G.to_directed()

    for node in directed_G.nodes():
        in_edges = list(directed_G.in_edges(node))
        total = len(in_edges)
        for source_node, target_node in in_edges:
            if total > 0:
                directed_G[source_node][target_node]["weight"] = 1 / total
            else:
                directed_G[source_node][target_node]["weight"] = 0.0

    return directed_G


def run_lt(G: nx.DiGraph, seeds: set[int]) -> Set[int]:
    active = set(seeds)
    thresholds = {}

    for node in G.nodes():
        thresholds[node] = random.uniform(0, 1)

    influences = {node: 0 for node in G.nodes()}
    newly_active = set(seeds)

    while newly_active:
        next_active = set()
        for node in newly_active:
            for neighbor in G.successors(node):
                if neighbor not in active:
                    weight = G[node][neighbor].get("weight", 0.1)
                    influences[neighbor] += weight

                    if influences[neighbor] >= thresholds[neighbor]:
                        next_active.add(neighbor)

        newly_active = next_active
        active.update(newly_active)

    return active


def estimate_spread(G: nx.DiGraph, seeds: set[int], simulations: int = 1000) -> float:
    total_spread = 0

    for _ in range(simulations):
        active = run_lt(G, seeds)
        total_spread += len(active)

    return total_spread / simulations


def greedy_select(G: nx.DiGraph, k: int, simulations: int) -> Set[int]:
    selected: Set[int] = set()
    all_nodes: Set[int] = set(G.nodes())

    for _ in range(k):
        best_node = None
        best_gain = -1

        for node in all_nodes - selected:
            temp_seed = selected | {node}
            gain = estimate_spread(G, temp_seed, simulations)

            if gain > best_gain:
                best_gain = gain
                best_node = node
        if best_node is not None:
            selected.add(best_node)
            print(f"Selected: {best_node} | Estimated Spread: {best_gain:.2f}")
        else:
            print("No more nodes to select.")
            break

    return selected


def run_simulation(n: int = 100, m: int = 2, k: int = 5, simulations: int = 1000, G: Optional[nx.DiGraph] = None):
    if G is None:
        G = generate_graph(n, m)

    seeds = greedy_select(G, k, simulations)
    print("Final seed set:", seeds)

    spread = estimate_spread(G, seeds, simulations)
    print("Final estimated spread:", spread)

# If you are going to run this file directly, uncomment the following lines:
# if __name__ == "__main__":
#     run_simulation(n=100, m=2, k=5, simulations=1000)
