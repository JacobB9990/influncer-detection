# 2007 Cost-Effective Outbreak Detection in Networks

## Introduction
How can we put "sensors" to quickly detect something spreading. This is one of the central questions asked in the 2007 paper *Cost-Effective Outbreak Detection in Networks*. From contamination in a water network, a disease in a social network, or even a computer virus. How can we choose a couple of locations to detect that spread and as **early** and **efficiently** as possible while having limited resources. This is the motivation of the paper. Sensors or monitors can cost a pretty penny. While contamination, disease, and computer viruses seem like different problems all together; they share a common mathematical structure. The authors realized that the benefit from placing sensors has **diminishing returns**.

### What is "Diminishing Returns?"
If you were a farmer you might fertilize your field to yield more crops. The initial fertilization might dramatically increase your crop yield. You might want to keep adding more fertilizer. The you might get a increase in crop yield, but it would be smaller each time. Then the fertilizer would be too excessive and start to produce smaller yields or even start to kill the plants. This is the essence of **submodularity**. The authors proved that outbreak detection objectives are **submodular**. This part is crucial to allow near-optimal solutions using greedy methods that are *efficient*. As these problems are **NP-hard** a greedy algorithm at least can guarantee a  $(1 - 1/e) \approx 63\% $ optimal solution. Since the optimal solution is computationally unmanageable for large networks we must use approximation algorithms to get the best estimates.

## Mathematical Foundations & Problem Formulation

### Magic of Submodularity
As I stated earlier outbreak detection follows a precise mathematical pattern called **submodularity**. Formally, a set function $R$ is submodular if for every $A \subseteq B \subseteq V$ and every sensor $s \in V \setminus B$:

$$
R(A \cup \{s\}) - R(A) \geq R(B \cup \{s\}) - R(B)
$$

**In plain English:** Adding a sensor to a small set gives you more "*bang for your buck*" than adding it to a large set. This perfectly captures our intuition about diminishing returns.

### What Are We Actually Optimizing?
The authors define three practical objectives that all turn out to be submodular:

#### 1. Detection Likelihood (DL)
- **Goal:** Catch as many outbreaks as possible
- **Penalty:** $\pi_i(t) = 0$ if detected, $\pi_i(\infty) = 1$ if missed
- **Translation:** "Did we detect this contamination or not?"

#### 2. Detection Time (DT)  
- **Goal:** Detect outbreaks as quickly as possible
- **Penalty:** $\pi_i(t) = \min\{t, T_{\max}\}$
- **Translation:** "How many hours until we sound the alarm?"

#### 3. Population Affected (PA)
- **Goal:** Minimize how many people are affected before detection
- **Penalty:** $\pi_i(t)$ = number of infected blogs/people at time $t$
- **Translation:** "How much damage occurs before we detect it?"

### The Reward Function
The clever part is how they frame everything as **penalty reduction**:

$$
R(A) = \sum_{i \in I} P(i) \cdot [\pi_i(\infty) - \pi_i(T(i,A))]
$$

Where:
- $T(i,A) = \min_{s \in A} T(i,s)$ is the earliest detection time
- $\pi_i(\infty)$ is the worst-case penalty (never detecting)
- $\pi_i(T(i,A))$ is the actual penalty based on detection time

**Why this matters:** This formulation guarantees $R(A)$ is submodular, which means we can apply greedy algorithms with strong guarantees!

### The Optimization Problem
#### Mathematically 

To formalize this optimization problem we have the equation: $$\max_{A \subseteq V} R(A) \hspace{0.15in} \text{subject to } c(A) \leq B,$$
where:
- $R(A)$ = expected benefit (e.g., faster detection, fewer affected people)
- $c(A)$ = cost of chosen nodes (e.g., sensor)
- $B$ = total budget 

They then improve on this with a faster, cost-sensitive algorithm called **CELF (Cost-Effective Lazy Forward selection)**, which is:
- Up to **700× faster** than the basic greedy method.
- Guaranteed to get at least half of the best possible result.

The mathematical beauty here is that the same framework works for both water contamination detection and net monitoring, the structure is **identical** once you recognize the submodular pattern. This foundation is what enables CELF to be both fast and provably near-optimal. 

## Cost-Effective Lazy Forward (CELF)
The goal of CELF is to pick $k$ nodes that can detect or cover as much of the networks "spread" as possible, given a cost budget. In my chosen data set a **S**tanford **N**etwork **A**nalysis **P**latform (SNAP) Facebook network we have *4,039* **Nodes** and *88,234* **Edges**. We want to find the node, a user, who would be the best at covering the networks spread while introducing a cost budget. 

### The Algorithm Steps 
1. **Initialize**: Compute all solo gains once
2. **Lazy Loop**: Only recompute **top** candidate's gain each round
3. **Two Strategies**: Run greedy with AND without cost consideration  
4. **Pick Best**: Choose the solution with higher spread

The key here is recomputing the **top** candidate's gain rather than all of them like in the basic greedy algorithm. this is what makes this algorithm **700x** faster. This dramatic speed up comes from avoiding redundant calculations. CELF only chooses the most promising candidates.

CELF actually runs two greedy variants, one that optimizes benefit-cost ratio, and another that ignores costs entirely, then selects the better solution.

### Technical


### Guarantees


## References
- Leskovec, Jure, et al. "Cost-effective Outbreak Detection in Networks." *Proceedings of the 13th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (KDD '07)*, 12-15 Aug. 2007, San Jose, California. Carnegie Mellon University, 2007. [https://www.cs.cmu.edu/~jure/pubs/detect-kdd07.pdf](https://www.cs.cmu.edu/~jure/pubs/detect-kdd07.pdf).
- Leskovec, Jure, and Julian J. McAuley. *Facebook Ego Network*. Stanford Network Analysis Project (SNAP), Stanford University, Sept. 2012, [https://snap.stanford.edu/data/ego-Facebook.html](https://snap.stanford.edu/data/ego-Facebook.html).