# Influential Nodes in a Diffusion Model for Social Networks (Kempe, David, Jon Kleinberg, and Éva Tardos)

This work was implemented in: `/2003-maximizing-the-spread-of-influence-through-a-social-network`. In this paper they formal introduced the Decreasing Cascade Model, which is a family of models. The core intuition/motivation stems from the recognition that individuals decisions are **strongly influenced** by their social contacts. They say targeting **specific set** of people to spread influence. Hopefully triggering a **cascade** effect.

This paper formal address the Influencing Maximization Problem, which is defined as:
- **Goal**: Choose a set $A$ of $k$ individuals (nodes) to initially activate ("target")
- **Objective**: Maximize the expected size, $\sigma(A)$, of the final set of active nodes after the influence cascade finishes

The authors introduce the **Decreasing Cascade Model** to describe how influence spreads through a network. In this model, a node becomes **less likely** to be activated as more of its neighbors have already tried to influence it, a way to capture the idea of “marketing saturation.” Because finding the **optimal set** of initial influencers is **NP-hard**, the authors focus on a practical solution: a greedy algorithm that repeatedly adds the node giving the **biggest** increase in the expected spread, denoted by $\sigma(A)$. They prove that this simple method achieves about 63% of the optimal spread (a $(1 - 1/e)$ approximation). This result holds because the spread function $\sigma(A)$ is both **monotone** (adding more seeds never reduces influence) and **submodular**, meaning each additional node provides smaller marginal gains, a reflection of diminishing returns in the diffusion process.

## References 
Kempe, David, Jon Kleinberg, and Éva Tardos. "Influential Nodes in a Diffusion Model for Social Networks." *Automata, Languages and Programming: 32nd International Colloquium, ICALP 2005, Lisbon, Portugal, July 11-15, 2005. Proceedings*. Ed. Lars Arge, Christian Cachin, Tomasz Jurdziński, and Andrzei Tarlecki. Springer, 2005, pp. 1127–1138.