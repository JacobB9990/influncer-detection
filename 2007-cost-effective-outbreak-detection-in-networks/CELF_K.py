import igraph as ig
import random
import heapq
from tqdm import tqdm
import matplotlib.pyplot as plt


def generate_graph(N: int, p_er: float, rnd_seed: int) -> ig.Graph:
    random.seed(rnd_seed)
    G = ig.Graph.Erdos_Renyi(n=N, p=p_er, directed=False, loops=False)
    return G

def Independent_Cascade(G: ig.Graph, seeds: list[int], p: float = 0.1) -> int:
    active = set(seeds)
    newly_active = set(seeds)

    while newly_active:
        next_active = set()
        for u in newly_active:
            for v in G.neighbors(u):
                if v not in active and random.random() <= p:
                    next_active.add(v)

        newly_active = next_active
        active |= next_active

    return len(active)

def estimate_spread(
    G: ig.Graph, seeds: list[int], MC: int = 5, p: float = 0.1
) -> float:
    if not seeds:
        return 0.0
    total = 0
    for _ in range(MC):
        total += Independent_Cascade(G, seeds, p)
    return total / MC


# CELF algorithm
def CELF_K(G: ig.Graph, k: int = 5, p: float = 0.1, simulations: int = 100) -> set[int]:
    selected: set[int] = set()
    heap: list = []

    # Initial marginal gains
    print("Computing initial gains...")
    for node in tqdm(range(G.vcount()), desc="Initial gain computation"):
        gain = estimate_spread(G, [node], MC=simulations, p=p)
        flag = 0
        heapq.heappush(heap, (-gain, node, flag))

    pbar = tqdm(total=k, desc="Selecting nodes", position=0)
    while len(selected) < k:
        neg_gain, node, flag = heapq.heappop(heap)

        # If the gain is outdated, recompute
        if flag < len(selected):
            new_gain = estimate_spread(
                G, list(selected) + [node], MC=simulations, p=p
            ) - estimate_spread(G, list(selected), MC=simulations, p=p)
            heapq.heappush(heap, (-new_gain, node, len(selected)))
        else:
            selected.add(node)
            pbar.update(1)

    pbar.close()
    return selected


if __name__ == "__main__":
    print("=" * 30)
    print("Generate Graph...")

    rnd_seed = 42
    G = ig.Graph.Read_Edgelist(
        "2007-cost-effective-outbreak-detection-in-networks/facebook_combined.txt",
        directed=False,
    )

    print("Generated graph with", G.vcount(), "nodes and", G.ecount(), "edges")

    # Parameters
    random.seed(42)
    k = 5  # Select k nodes
    MC = 20  # Monte Carlo simulations
    active_p = 0.1  # Probability of activation

    # Run CELF
    print("Running CELF...")
    chosen_nodes = CELF_K(G, k, active_p, MC)
    print("Chosen nodes:", chosen_nodes)
    print(f"Estimated spread: {estimate_spread(G, list(chosen_nodes), 100, active_p)}")

    # Visualization
    layout = G.layout("fr")
    colors = ["yellow" if v.index in chosen_nodes else "skyblue" for v in G.vs]

    ig.plot(
        G,
        layout=layout,
        vertex_size=5,
        vertex_color=colors,
        edge_color="gray",
        bbox=(800, 800),
        margin=40,
    )

    print("Plot saved.")
