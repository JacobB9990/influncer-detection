import numpy as np
import heapq
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
def run_IC(flat_adj, start_idx, seeds, seeds_len, p):
    n = len(start_idx) - 1
    active = np.zeros(n, dtype=np.uint8)
    queue = np.empty(n, dtype=np.int32)
    q_len = 0
    
    for i in range(seeds_len):
        s = seeds[i]
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
            if active[v] == 0 and np.random.random() <= p:
                active[v] = 1
                queue[q_len] = v
                q_len += 1
    return active.sum()

@njit
def estimate_spread(flat_adj, start_idx, seeds, seeds_len, MC, p):
    total = 0
    for _ in range(MC):
        total += run_IC(flat_adj, start_idx, seeds, seeds_len, p)
    return total / MC

def node_cost(start_idx, u):
    if u < 0 or u >= len(start_idx) - 1:
        raise IndexError("node index out of range")
    deg = int(start_idx[u + 1] - start_idx[u])
    return 1.0 + 0.01 * deg

def compute_init_gains(flat_adj, start_idx, MC, p):
    n = len(start_idx) - 1
    heap = []
    seed_array = np.zeros(1, dtype=np.int32)
    
    for v in tqdm(range(n), desc="Computing initial gains"):
        seed_array[0] = v
        gain = estimate_spread(flat_adj, start_idx, seed_array, 1, MC, p)
        cost = node_cost(start_idx, v)
        ratio = gain / cost
        heapq.heappush(heap, (-ratio, v, gain, cost, 0))
    
    return heap

def CELF_C(flat_adj, start_idx, budget=30.0, MC_init=10, MC_final=100, p=0.1):
    n = len(start_idx) - 1
    selected = []
    current_spread = 0.0
    total_cost = 0.0
    
    max_seeds = min(int(budget) + 10, n)
    seed_array = np.zeros(max_seeds, dtype=np.int32)
    
    heap = compute_init_gains(flat_adj, start_idx, MC_init, p)
    
    while total_cost < budget and heap:
        neg_ratio, v, gain, cost, last_updated = heapq.heappop(heap)
        
        if v in selected:
            continue
        
        if total_cost + cost > budget:
            continue

        if last_updated < len(selected):
            temp_len = len(selected) + 1
            for i, node in enumerate(selected):
                seed_array[i] = node
            seed_array[len(selected)] = v
            
            spread_with_v = estimate_spread(flat_adj, start_idx, seed_array, temp_len, MC_init, p)
            marginal_gain = spread_with_v - current_spread
            ratio = marginal_gain / cost

            heapq.heappush(heap, (-ratio, v, marginal_gain, cost, len(selected)))
            continue
        
        selected.append(v)
        seed_array[len(selected) - 1] = v
        total_cost += cost
        
        current_spread = estimate_spread(flat_adj, start_idx, seed_array, len(selected), MC_final, p)
        
        print(f"Selected {v}, marginal gain = {gain:.2f}, current spread = {current_spread:.2f}")
    
    return set(selected), total_cost, current_spread

def main(path, budget = 30.0, MC_init = 100, MC_final = 1000, p = 0.1):
    path_to_list = path

    print("Building adjacency list...")
    start_time = time.time()
    adj = build_adj_list(path_to_list)
    flat_adj, start_idx = flatten_adj_list(adj)

    print("Running CELF-C...")
    chosen_nodes, total_cost, spread = CELF_C(flat_adj, start_idx, budget, MC_init, MC_final, p)

    print("\nChosen nodes:", chosen_nodes)
    print(f"Total cost: {total_cost:.2f}")
    print(f"Estimated spread: {spread:.2f}")
    print(f"Elapsed time: {time.time() - start_time:.2f} seconds")
    
if __name__ == "__main__": # I have it this way to make a benchmark later on.
    np.random.seed(42)
    path = "2007-cost-effective-outbreak-detection-in-networks/facebook_combined.txt"
    # Parameters
    budget = 30.0      # Total budget
    MC_init = 100      # MC for lazy recomputations
    MC_final = 1000   # MC for final spread estimates
    p = 0.1            # Transmission probability

    path_to_list = path

    print("Building adjacency list...")
    start_time = time.time()
    adj = build_adj_list(path_to_list)
    flat_adj, start_idx = flatten_adj_list(adj)

    print("Running CELF-C...")
    chosen_nodes, total_cost, spread = CELF_C(flat_adj, start_idx, budget, MC_init, MC_final, p)

    print("\nChosen nodes:", chosen_nodes)
    print(f"Total cost: {total_cost:.2f}")
    print(f"Estimated spread: {spread:.2f}")
    print(f"Elapsed time: {time.time() - start_time:.2f} seconds")