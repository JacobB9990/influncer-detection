import networkx as nx
import heapq
import random
from typing import Set, List, Dict, Tuple
from tqdm import tqdm
import matplotlib.pyplot as plt

random.seed(42)

# Load the SNAP Facebook network
G = nx.read_edgelist(
    "2007-cost-effective-outbreak-detection-in-networks/facebook_combined.txt",
    create_using=nx.Graph(),
    nodetype=int,
)


# Independent Cascade
def run_ic(G: nx.Graph, seeds: Set[int], p: float = 0.1, steps: int = 5) -> Set[int]:
    active: Set[int] = set(seeds)
    newly_active: Set[int] = set(seeds)
    for _ in range(steps):
        next_active: Set[int] = {
            nbr
            for node in newly_active
            for nbr in G.neighbors(node)
            if nbr not in active and random.random() < p
        }
        if not next_active:
            break
        active.update(next_active)
        newly_active = next_active
    return active


def node_cost(G: nx.Graph, node: int) -> float:
    return 1 + 0.01 * G.degree(node)


def total_cost(G: nx.Graph, S: Set[int]) -> float:
    return sum(node_cost(G, n) for n in S)


def expected_spread(G: nx.Graph, seeds: List[int], simulations: int = 5, p: float = 0.1, steps: int = 5) -> float:
    if not seeds:
        return 0.0
    return (
        sum(len(run_ic(G, set(seeds), p, steps)) for _ in range(simulations))
        / simulations
    )


# CELF Algorithm
def celf(G: nx.Graph, k: int = 10, budget: float = 50, p: float = 0.1, simulations: int = 5) -> Tuple[list[int], float]:
    
    selected: List[int] = []
    costs: Dict[int, float] = {n: node_cost(G, n) for n in G.nodes()}
    gains: List[tuple[float, int, float, int]] = []

    print("Computing initial gains...")
    for node in tqdm(G.nodes(), desc="Initial gain computation"):
        gain: float = expected_spread(G, [node], simulations=simulations, p=p)
        heapq.heappush(gains, (-gain / costs[node], node, gain, 0))  # max-heap

    total_selected_cost: float = 0
    iteration = 1
    pbar = tqdm(total=k, desc="Selecting nodes", position=0)
    while gains and len(selected) < k and total_selected_cost < budget:
        ratio, node, gain, last_update = heapq.heappop(gains)
        if last_update < iteration:
            current_spread = expected_spread(G, selected, simulations=simulations, p=p)
            new_gain = expected_spread(G, selected + [node], simulations=simulations, p=p) - current_spread
            heapq.heappush(gains, (-new_gain / costs[node], node, new_gain, iteration))
        else:
            if total_selected_cost + costs[node] > budget:
                break
            selected.append(node)
            total_selected_cost += costs[node]
            iteration += 1
            pbar.update(1)
    pbar.close()
    return selected, total_selected_cost


# Run CELF
chosen_nodes, total = celf(G, k=10, budget=50, p=0.1, simulations=50)
print("\nChosen nodes:", chosen_nodes)
print("Total cost:", total)
print("Expected coverage:", expected_spread(G, chosen_nodes, simulations=50))

# Annotate and save graph
nx.set_node_attributes(G, {n: n in chosen_nodes for n in G.nodes()}, "flag")
nx.write_graphml(
    G,
    "./2007-cost-effective-outbreak-detection-in-networks/facebook_network_annotated.graphml",
)

# Plot
pos = nx.spring_layout(G, seed=42)
plt.figure(figsize=(12, 8))
nx.draw_networkx_edges(G, pos, alpha=0.05, width=0.3)
nx.draw_networkx_nodes(G, pos, node_size=10, node_color="lightblue", alpha=0.7)
nx.draw_networkx_nodes(G, pos, nodelist=chosen_nodes, node_color="red", node_size=80)
plt.title("CELF-Selected Nodes for Outbreak Detection (Facebook Network)")
plt.axis("off")
plt.tight_layout()
plt.savefig("./2007-cost-effective-outbreak-detection-in-networks/FacebookGraph.png")
plt.close()