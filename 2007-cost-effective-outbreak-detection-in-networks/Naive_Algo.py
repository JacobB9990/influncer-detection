import numpy as np
from numba import njit
from tqdm import tqdm
import time

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


def greedy_naive(flat_adj, start_idx, k=5, MC=100, p=0.1):
    n = len(start_idx) - 1
    nodes = list(range(n))
    selected = []
    current_spread = 0.0

    for step in range(k):
        best_node = -1
        best_gain = -1.0

        for v in tqdm(nodes, desc=f"Iteration {step+1}/{k}"):
            if v in selected:
                continue

            spread_with_v = estimate_spread(
                flat_adj, start_idx, selected + [v], MC, p
            )
            marginal_gain = spread_with_v - current_spread

            if marginal_gain > best_gain:
                best_gain = marginal_gain
                best_node = v

        selected.append(best_node)
        current_spread = estimate_spread(
            flat_adj, start_idx, selected, MC, p
        )

        print(
            f"Selected {best_node}, marginal gain = {best_gain:.2f}, "
            f"current spread = {current_spread:.2f}"
        )

    return set(selected), current_spread


def main(path, k=5, MC=1000, p=0.1):
    print("Building adjacency list...")
    start_time = time.time()

    adj = build_adj_list(path)
    flat_adj, start_idx = flatten_adj_list(adj)

    print("Running Naive Greedy...")
    chosen_nodes, spread = greedy_naive(flat_adj, start_idx, k, MC, p)

    print("\nChosen nodes:", chosen_nodes)
    print(f"Estimated spread: {spread:.2f}")
    print(f"Elapsed time: {time.time() - start_time:.2f} seconds")

    return chosen_nodes, spread


if __name__ == "__main__":
    np.random.seed(2)

    path = "2007-cost-effective-outbreak-detection-in-networks/facebook_combined.txt"

    # Parameters
    k = 5
    MC = 100
    p = 0.1

    main(path, k, MC, p)