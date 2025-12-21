import numpy as np
import heapq
from numba import njit, prange
from tqdm import tqdm
import time


# Make our graph
def build_adj_list(edge_list_path):
    edges = np.loadtxt(edge_list_path, dtype=np.int32)
    n = edges.max() + 1
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return adj


def flatten_adj_list(adj):
    n = len(adj)
    start_idx = np.zeros(n + 1, dtype=np.int32)
    total_edges = sum(len(neigh) for neigh in adj)
    flat_adj = np.zeros(total_edges, dtype=np.int32)

    idx = 0
    for i, neigh in enumerate(adj):
        start_idx[i] = idx
        flat_adj[idx : idx + len(neigh)] = neigh
        idx += len(neigh)
    start_idx[n] = idx
    return flat_adj, start_idx


# IC Model
@njit
def run_IC(flat_adj, start_idx, seeds, p):
    n = len(start_idx) - 1
    active = np.zeros(n, dtype=np.uint8)
    queue = np.empty(n, dtype=np.int32)
    q_len = 0

    for s in seeds:
        if active[s] == 0:
            active[s] = 1
            queue[q_len] = s
            q_len += 1

    idx = 0
    while idx < q_len:
        u = queue[idx]
        idx += 1
        for i in range(start_idx[u], start_idx[u + 1]):
            v = flat_adj[i]
            if active[v] == 0 and np.random.rand() <= p:
                active[v] = 1
                queue[q_len] = v
                q_len += 1
    return active.sum()


@njit
def estimate_spread(flat_adj, start_idx, seeds, MC, p):
    total = 0
    for _ in range(MC):
        total += run_IC(flat_adj, start_idx, seeds, p)
    return total / MC


def compute_init_gains(flat_adj, start_idx, nodes, MC, p):
    heap = []
    for v in tqdm(nodes, desc="Computing initial gains"):
        gain = estimate_spread(flat_adj, start_idx, [v], MC, p)
        heapq.heappush(heap, (-gain, v, 0))  # max heap
    return heap


# CELF-K Algo choose how many nodes
def CELF_K(flat_adj, start_idx, k=5, MC_init=10, MC_final=100, p=0.1):
    n = len(start_idx) - 1
    nodes = list(range(n))
    selected = []
    heap = compute_init_gains(flat_adj, start_idx, nodes, MC_init, p)
    current_spread = 0.0

    while len(selected) < k:
        neg_gain, v, last_updated = heapq.heappop(heap)
        if v in selected:
            continue

        if last_updated != len(selected):
            spread_with_v = estimate_spread(
                flat_adj, start_idx, selected + [v], MC_init, p
            )
            marginal_gain = spread_with_v - current_spread
            heapq.heappush(heap, (-marginal_gain, v, len(selected)))
            continue

        selected.append(v)

        current_spread = estimate_spread(flat_adj, start_idx, selected, MC_final, p)
        print(
            f"Selected {v}, marginal gain = {-neg_gain:.2f}, current spread = {current_spread:.2f}"
        )

    return set(selected), current_spread


def main(path, k = 5, MC_init = 100, MC_final = 1000, p = 0.1):
    path_to_list = path

    print("Building adjacency list...")
    start_time = time.time()
    adj = build_adj_list(path_to_list)
    flat_adj, start_idx = flatten_adj_list(adj)

    print("Running CELF-K...")
    chosen_nodes, spread = CELF_K(flat_adj, start_idx, k, MC_init, MC_final, p)

    print("\nChosen nodes:", chosen_nodes)
    print(f"Estimated spread: {spread:.2f}")
    print(f"Elapsed time: {time.time() - start_time:.2f} seconds")
    return chosen_nodes, spread
    
if __name__ == "__main__":
    path = ("2007-cost-effective-outbreak-detection-in-networks/facebook_combined.txt")
    # Parameters
    k = 5                # Number of seeds
    MC_init = 100        # MC for lazy recomputations
    MC_final = 1000      # MC for final spread estimates
    p = 0.1              # Transmission probability
    
    main(path, k, MC_init, MC_final, p)
    