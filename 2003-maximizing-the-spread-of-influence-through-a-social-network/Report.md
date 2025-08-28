# Maximizing Spread Report

## Introduction
Influence maximization is the problem where selecting influential nodes, we call seeds, that can maximize the spread of influence through out a network. This is widly important for companies that want to sell their product/service to users. In the paper the authors, used two diffusion models, **Independent Cascade (IC)** model and the **Linear Threshold (LT)** model. This report will explain these models, the greedy approach to seed selection, and our results on a Barabási–Albert network. 

*Note: The use of a generated network rather than a real-world network. Is because real datasets are often huge and I wanted to keep it nice and simple. Also, Monte Carlo Simulations can take be slow without parallelization.*

### 1. Independent Cascade Model (IC)
The IC model has influence spreads in discrete steps. Each node gets one chance to activate each inactive neighbor with a certain probabiity. Each Activation attempt are independent. We start with a seed set of active nodes. Each step, a newly activated nodes try to activate each inactive neighbor. Again, the edge weights represent influence probabilites. We just continue the proces until no new activations occur.

Think of it as this: you are trying to influence two friends. One you talk to a lot the other is just an acquaintance. You're more likely to successfully influence the close friend, which corresponds to a higher activation probability on that edge.

#### Formal Definition
Let $G = (V, E)$ be a directed graph where each edge $(u, v) \in E$ has a probability $p_{uv}$ of activating node $v$ if node $u$ becomes active.

- At time $t = 0$, the seed set $S \subseteq V$ is activated.
- At each time step $t \geq 1$, any node $u$ activated at time $t - 1$ attempts to activate each currently inactive neighbor $v$ with probability $p_{uv}$.
- Each node has **only one chance** to activate each neighbor.
- The process continues until no more nodes are activated.

### 2. Linear Threshold Model (LT)
The Linear Threshold (LT) model simulates influence spread based on total influence from neighbors. Each node is assigned a **threshold** $\theta_v \in [0, 1]$, representing how much total influence it needs from its neighbors before becoming active. Influence spreads step by step. At each step, if the **sum of the incoming weights** from already active neighbors meets or is greater than a node’s threshold, that node becomes active. The process continues until no further activations occur.

Imagine a student deciding whether to attend a study group. They might go only if enough of their trusted classmates (i.e., ones who have influence over them) are already going. Once that “influence sum” exceeds their internal threshold, they decide to join.

#### Formal Definition:

Let $G = (V, E)$ be a directed graph. Each edge $(u, v) \in E$ has an influence weight $b_{uv} \geq 0$, with the condition:

$$
\sum_{u \in N_v} b_{uv} \leq 1
$$

where $N_v$ is the set of in-neighbors of node $v$.

Each node $v$ independently selects a threshold $\theta_v \sim \text{Uniform}(0, 1)$.

- At time $t = 0$, a seed set $S \subseteq V$ is activated.
- At time $t \geq 1$, an inactive node $v$ becomes active if:

$$
\sum_{\substack{u \in N_v \\ u \text{ is active}}} b_{uv} \geq \theta_v
$$

- The process repeats until no new activations occur.

## 3. Seed Selection via Greedy Algorithm
Our goal is to select **k** nodes maximizing the expected influence spread. We will itertively add the node with highest marginal gain to teh current seed set. The marginal gain is estimated by running Monte Carlo simulations of the diffusion model multiple times. These simulations become computationally expensive, but yield near-optimal results. The greedy algorithm guarantees a $1-1/e \approx 63\%$ to the optimal spread.

## 4. Results

| Model                    | Seed Set         | Estimated Spread (Avg) |
| ------------------------ | ---------------- | ---------------------- |
| Independent Cascade (IC) | {0, 17, 9, 8}    | 40.449                 |
| Linear Threshold (LT)    | {0, 17, 9, 8}    | 49.727                 |
| PageRank (IC)            | {17, 11, 26, 50} | 31.517                 |

*Example with a Barabási–Albert graph (n=100, m=2), k=4 seeds, 1000 simulations.*

*All diffusion models and heuristics were tested on the same underlying network to ensure consistency in evaluation and fair comparison.*

### Discussion
It’s interesting that both the Independent Cascade (IC) and Linear Threshold (LT) models picked the same seed set in this experiment, but the estimated spreads were different. This shows that while the greedy algorithm often finds similar key nodes the way influence actually spreads depends on the model.

In many runs, the seed sets overlapped, but sometimes they differed because the models spread influence differently. IC spreads influence probabilistically along edges, while LT depends on the neighboring nodes combined influence crossing a threshold. So, some nodes work better as seeds in one model than the other, depending on the network and weights.

I also threw PageRank in there to show that even finding the nodes with the high importance does not always mean the greatest spread. 

## References

Kempe, D., Kleinberg, J., & Tardos, É. (2003). Maximizing the spread of influence through a social network. *Proceedings of the ninth ACM SIGKDD international conference on Knowledge discovery and data mining*, 137–146. [https://doi.org/10.1145/956750.956769](https://doi.org/10.1145/956750.956769)
