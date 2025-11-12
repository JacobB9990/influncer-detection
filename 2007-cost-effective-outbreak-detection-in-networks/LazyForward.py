import networkx as nx
import heapq
from typing import Set
import random
from tqdm import tqdm

# Load the SNAP Facebook network
G = nx.read_edgelist(
    "2007-cost-effective-outbreak-detection-in-networks/facebook_combined.txt",
    create_using=nx.Graph(),
    nodetype=int,
)

# Independent Cascade
def run_ic(G, seeds, p=0.1, steps=5):
    active: Set[int] = set(seeds)
    newly_active: Set[int] = set(seeds)

    for _ in range(steps):
        next_active: Set[int] = set()
        for node in newly_active:
            for neighbor in G.neighbors(node):
                if neighbor not in active and random.random() < p:
                    next_active.add(neighbor)
        if not next_active:
            break
        active.update(next_active)
        newly_active = next_active
    return active

def node_cost(G, node):
    return 1 + 0.01 * G.degree(node)

def total_cost(G, S):
    return sum(node_cost(G, n) for n in S)

def expected_spread(G, seeds, simulations=5, p=0.1, steps=5):
    if not seeds:
        return 0
    total = 0
    for _ in range(simulations):
        total += len(run_ic(G, seeds, p, steps))
    return total / simulations


# CELF Algorithm
def celf(G, k, budget, p=0.1, simulations=5):
    selected = []
    costs = {n: node_cost(G, n) for n in G.nodes()}
    gains = []

    print("Computing initial gains...")
    for node in tqdm(G.nodes(), desc="Initial gain computation"):
        gain = expected_spread(G, [node], simulations=simulations, p=p)
        heapq.heappush(gains, (-gain / costs[node], node, gain, 0))  # max-heap

    total_cost = 0
    iteration = 1

    pbar = tqdm(total=k, desc="Selecting nodes", position=0)
    while gains and len(selected) < k and total_cost < budget:
        ratio, node, gain, last_update = heapq.heappop(gains)

        if last_update < iteration:
            new_gain = (
                expected_spread(G, selected + [node], simulations=simulations, p=p)
                - expected_spread(G, selected, simulations=simulations, p=p)
            )
            heapq.heappush(gains, (-new_gain / costs[node], node, new_gain, iteration))
        else:
            if total_cost + costs[node] > budget:
                break
            selected.append(node)
            total_cost += costs[node]
            iteration += 1
            pbar.update(1)

    pbar.close()
    return selected, total_cost

chosen_nodes, total = celf(G, k=10, budget=50, p=0.1, simulations=3)
print("\nChosen nodes:", chosen_nodes)
print("Total cost:", total)
print("Expected coverage:", expected_spread(G, chosen_nodes, simulations=5))

print("Working On Graph")

nx.set_node_attributes(G, {n: n in chosen_nodes for n in G.nodes()}, "flag")
nx.write_graphml(G, "./2007-cost-effective-outbreak-detection-in-networks/facebook_network_annotated.graphml")
# pos = nx.spring_layout(G, seed=42)
# plt.figure(figsize=(12, 8))
# nx.draw_networkx_edges(G, pos, alpha=0.05, width=0.3)
# nx.draw_networkx_nodes(G, pos, node_size=10, node_color='lightblue', alpha=0.7)
# nx.draw_networkx_nodes(G, pos, nodelist=chosen_nodes, node_color='red', node_size=80)
# plt.title("CELF-Selected Nodes for Outbreak Detection (Facebook Network)")
# plt.axis("off")
# plt.tight_layout()
# plt.show()
# plt.savefig("./2007-cost-effective-outbreak-detection-in-networks/FacebookGraph.png")
