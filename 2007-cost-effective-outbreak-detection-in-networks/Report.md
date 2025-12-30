# 2007 Cost-Effective Outbreak Detection in Networks

## Introduction
How can we put "sensors" to quickly detect something spreading? This is one of the central questions asked in the 2007 paper *Cost-Effective Outbreak Detection in Networks*. From contamination in a water network, a disease in a social network, or even a computer virus, how can we choose a few locations to detect that spread as **early** and **efficiently** as possible while having limited resources? This is the motivation of the paper. Sensors or monitors can be expensive. While contamination, disease, and computer viruses seem like different problems altogether, they share a common mathematical structure. The authors realized that the benefit from placing sensors has **diminishing returns**.

### What is "Diminishing Returns?"
If you were a farmer, you might fertilize your field to yield more crops. The initial fertilization might dramatically increase your crop yield. You might want to keep adding more fertilizer, but the increase in crop yield would get smaller each time. Eventually, too much fertilizer would produce minimal gains or even harm the plants. This is the essence of **submodularity**. The authors proved that outbreak detection objectives are submodular. This is crucial because it allows near-optimal solutions using greedy methods that are *efficient*. Since the optimal solution is computationally unmanageable for large networks, we must use approximation algorithms to get the best estimates. A greedy algorithm can guarantee a $(1 - 1/e) \approx 63\%$ optimal solution.

## Mathematical Foundations & Problem Formulation

### Magic of Submodularity
As stated earlier, outbreak detection follows a precise mathematical pattern called **submodularity**. Formally, a set function $R$ is submodular if for every $A \subseteq B \subseteq V$ and every sensor $s \in V \setminus B$:

$$
R(A \cup \{s\}) - R(A) \geq R(B \cup \{s\}) - R(B)
$$

**In plain English:** Adding a sensor to a small set gives more "*bang for your buck*" than adding it to a large set. This perfectly captures the intuition about diminishing returns.

### What Are We Actually Optimizing?
The authors define three practical objectives that all turn out to be submodular. The first is **Detection Likelihood (DL)**, where the goal is to catch as many outbreaks as possible. The penalty function $\pi_i(t)$ is 0 if the outbreak is detected and 1 if missed, essentially answering "Did we detect this contamination or not?" The second is **Detection Time (DT)**, aiming to detect outbreaks as quickly as possible, with $\pi_i(t) = \min\{t, T_{\max}\}$, representing "How many hours until we sound the alarm?" The third objective is **Population Affected (PA)**, where the goal is to minimize the number of people affected before detection, and the penalty $\pi_i(t)$ counts the number of infected individuals at time $t", essentially answering "How much damage occurs before we detect it?"

### The Reward Function
The clever part is how the objectives are framed as **penalty reduction**:

$$
R(A) = \sum_{i \in I} P(i) \cdot [\pi_i(\infty) - \pi_i(T(i,A))]
$$

where $T(i,A) = \min_{s \in A} T(i,s)$ is the earliest detection time, $\pi_i(\infty)$ is the worst-case penalty (never detecting), and $\pi_i(T(i,A))$ is the actual penalty based on detection time. This formulation guarantees $R(A)$ is submodular, allowing greedy algorithms to provide strong approximation guarantees.

### The Optimization Problem
The optimization problem is formalized as:

$$
\max_{A \subseteq V} R(A) \quad \text{subject to } c(A) \leq B
$$

where $R(A)$ is the expected benefit (faster detection or fewer affected people), $c(A)$ is the cost of chosen nodes, and $B$ is the total budget. The authors then introduce a faster, cost-sensitive algorithm called **CELF (Cost-Effective Lazy Forward selection)**, which can be up to **700× faster** than the basic greedy method while guaranteeing at least half of the best possible result. The framework applies to both water contamination detection and network monitoring once the submodular pattern is recognized, enabling CELF to be both fast and provably near-optimal.



## Algorithms Implemented

### Naive Greedy Baseline
The naive greedy algorithm recomputes the full marginal gain for all candidate nodes in every iteration. While conceptually simple, this approach is computationally expensive because it repeatedly evaluates all nodes even when most of them are unlikely to be selected. Its time complexity grows linearly with the number of nodes times the number of Monte Carlo simulations.

### Cost-Effective Lazy Forward (CELF)
CELF aims to select $k$ nodes that maximize coverage or early detection given a cost budget. The algorithm starts by computing all solo gains once, then enters a **lazy loop**, where only the top candidate's gain is recomputed at each round. CELF runs two variants: one that optimizes the benefit-to-cost ratio and another that ignores costs. The solution with the higher spread is chosen. The key efficiency comes from avoiding redundant computations: by recomputing only the most promising candidates, CELF achieves up to **700× speedup** compared to naive greedy. Implementations are provided as [CELF cost](CELF_Cost.py) and [CELF with a set k](CELF_SET_K.py).

## Dataset Description
We will use the Facebook Ego Network dataset from the **S**tanford **N**etwork **A**nalysis **P**roject (SNAP). It contains 10 ego-centric networks collected from Facebook, where each network includes a central user, their friends, and the friendship connections among those friends. Combined, the dataset contains 4,039 nodes and 88,234 undirected edges. Its realistic social structure and manageable size make it fit for evaluating outbreak detection and influence-based sensor placement methods.

## Diffusion / Outbreak Model
We implemented the Independent Cascade (IC) model, a probabilistic diffusion model in which each active node has one chance to activate each of its inactive neighbors with a fixed probability. The process continues in discrete steps until no more activations occur. In our simulations, the transmission probability is set to $p = 0.1$. In practice, this probability would usually be estimated from historical data or interaction patterns between nodes.

## Cost Model
Node costs in `CELF_Cost.py` are proportional to their degree, reflecting the intuition that more connected nodes are more “expensive” to monitor. Based on the highest node cost, a budget of 30.0 was chosen, which allows selection of a meaningful number of nodes without exceeding the budget.

**Implementation:** 
```py
cost(node) = 1.0 + 0.01 × node.degree
```

**Node cost statistics (for our dataset):**
```
Highest cost: 11.45
Lowest cost: 1.01
Average cost: 1.44
Elapsed time: 0.08 seconds
```
In real world applications, resources are limited, and a cost-aware approach like CELF Cost allows selecting the most influential or critical nodes to maximize coverage or resilience within a fixed budget.

## Implementation Details
Although these algorithms are often implemented in C/C++ for maximum speed, we implemented them in Python for readability and access to high-level libraries like `numpy` and `numba`. Python allows fast prototyping while still achieving competitive performance through just-in-time compilation and efficient array operations.

The implementation relies on several key data structures. An adjacency list (`adj`) stores neighbors for each node, while a flattened adjacency array (`flat_adj`) and start indices (`start_idx`) allow fast access in Numba JIT-compiled functions. The `seed_array` holds currently selected seeds, and `active` nodes along with a `queue` manage BFS-style propagation in Monte Carlo simulations. A priority queue (`heap`) implements CELF’s lazy evaluation, storing nodes with their gain-to-cost ratio, cost, and last update iteration for efficient extraction of the best candidate.

Monte Carlo optimization techniques include lazy evaluation of marginal gains and a two-level simulation strategy, with `MC_init` for intermediate updates and `MC_final` for final spread estimation. Numba compilation ensures repeated simulations are feasible. Additional caching strategies include heap-based lazy updates and precomputed node degrees for cost calculations. Overall, this design balances readability, maintainability, and performance, allowing testing on large graphs without low-level languages.

## Experimental Setup
Experiments were conducted on an AMD Ryzen 5 5600X using a single core. Two-level Monte Carlo simulations were used, with `MC_init = 100` for intermediate lazy updates and `MC_final = 1000` for final spread estimation. Random seed `np.random.seed(42)` ensures reproducibility. Evaluation metrics include estimated spread (number of activated nodes), total cost of selected seeds, and runtime. Transmission probability was set at $p = 0.1$, with a budget of 30.0, and the cost function was proportional to node degree. If you are running `CELF_SET_K.py` then the program stops after choosing $k$ nodes.

## Results

```bash
$ python /2007-cost-effective-outbreak-detection-in-networks/CELF_SET_K.py
Building adjacency list...
Running CELF-K...
Computing initial gains: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 4039/4039 [02:55<00:00, 23.08it/s] 
Selected 2398, marginal gain = 2939.17, current spread = 2912.20
Selected 697, marginal gain = 108.72, current spread = 3009.00
Selected 254, marginal gain = 31.67, current spread = 3022.57
Selected 3824, marginal gain = 25.50, current spread = 3035.37
Selected 3523, marginal gain = 18.18, current spread = 3039.91

Chosen nodes: {3523, 3824, 254, 697, 2398}
Estimated spread: 3039.91
Elapsed time: 450.31 seconds
```

```bash
python /2007-cost-effective-outbreak-detection-in-networks/Naive_Algo.py
Building adjacency list...
█████████████████████████████████████████████████████████████████████████████| 4039/4039 [02:54<00:00, 23.13it/s]
Selected 2381, marginal gain = 2941.93, current spread = 2908.05
Iteration 2/5: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 4039/4039 [04:08<00:00, 16.26it/s]
Selected 805, marginal gain = 119.90, current spread = 3013.61
Iteration 3/5: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 4039/4039 [04:13<00:00, 15.93it/s]
Selected 303, marginal gain = 29.44, current spread = 3023.16
Iteration 4/5: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 4039/4039 [04:09<00:00, 16.22it/s] 
Selected 3702, marginal gain = 26.97, current spread = 3048.83
Iteration 5/5: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 4039/4039 [04:06<00:00, 16.38it/s]
Selected 4034, marginal gain = 6.85, current spread = 3048.10

Chosen nodes: {4034, 805, 2381, 303, 3702}
Estimated spread: 3048.10
Elapsed time: 1172.47 seconds
```

### Detection Performance


### Runtime Performance


## Analysis & Discussion


## Limitations


## Conclusion


## References
- Leskovec, Jure, et al. "Cost-effective Outbreak Detection in Networks." *Proceedings of the 13th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (KDD '07)*, 12-15 Aug. 2007, San Jose, California. Carnegie Mellon University, 2007. [https://www.cs.cmu.edu/~jure/pubs/detect-kdd07.pdf](https://www.cs.cmu.edu/~jure/pubs/detect-kdd07.pdf).
- Leskovec, Jure, and Julian J. McAuley. *Facebook Ego Network*. Stanford Network Analysis Project (SNAP), Stanford University, Sept. 2012, [https://snap.stanford.edu/data/ego-Facebook.html](https://snap.stanford.edu/data/ego-Facebook.html).