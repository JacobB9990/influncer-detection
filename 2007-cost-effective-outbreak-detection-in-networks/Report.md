# 2007 Cost-Effective Outbreak Detection in Networks

## Introduction
How can we put "sensors" to quickly detect something spreading. This is one of the central questions asked in the 2007 paper *Cost-Effective Outbreak Detection in Networks*. From contamination in a water network, a disease in a social network, or even a computer virus. How can we choose a couple of locations to detect that spread and as **early** and **efficiently** as possible while having limited resources. This is the motivation of the paper. Sensors or monitors can cost a pretty penny. While contamination, disease, and computer viruses seem like different problems all together; they share a common mathematical structure. The authors realized that the benefit from placing sensors has **diminishing returns**.

### What is "Diminishing Returns?"
If you were a farmer you might fertilize your field to yield more crops. The initial fertilization might dramatically increase your crop yield. You might want to keep adding more fertilizer. The you might get a increase in crop yield, but it would be smaller each time. Then the fertilizer would be too excessive and start to produce smaller yields or even start to kill the plants. This is the essence of **submodularity**. The authors proved that outbreak detection objectives are **submodular**. This part is crucial to allow near-optimal solutions using greedy methods that are *efficient*. As these problems are **NP-hard** a greedy algorithm at least can guarantee a  $(1 - 1/e) \approx 63\% $ optimal solution. 

To formalize this optimization problem we have the equation: $$\max_{A \subseteq V} R(A) \hspace{0.15in} \text{subject to } c(A) \leq B,$$
where:
- $R(A)$ = expected benefit (e.g., faster detection, fewer affected people)
- $c(A)$ = cost of chosen nodes (e.g., sensor)
- $B$ = total budget 

They then improve on this with a faster, cost-sensitive algorithm called **CELF (Cost-Effective Lazy Forward selection)**, which is:
- Up to **700× faster** than the naive greedy method.
- Guaranteed to achieve at least half of the optimal benefit fractionally.

### Cost-Effective Lazy Forward (CELF)
The goal of CELF is to pick $k$ nodes that can detect or cover as much of the networks "spread" as possible, given a cost budget. In my chosen data set a SNAP Facebook network we will try to find the best nodes to 

## References
- Leskovec, Jure, et al. “Cost-effective Outbreak Detection in Networks.” *Proceedings of the 13th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (KDD ’07)*, 12-15 Aug. 2007, San Jose, California. Carnegie Mellon University, 2007. [https://www.cs.cmu.edu/~jure/pubs/detect-kdd07.pdf](https://www.cs.cmu.edu/~jure/pubs/detect-kdd07.pdf).
- Leskovec, Jure, and Julian J. McAuley. *Facebook Ego Network*. Stanford Network Analysis Project (SNAP), Stanford University, Sept. 2012, [https://snap.stanford.edu/data/ego-Facebook.html](https://snap.stanford.edu/data/ego-Facebook.html).
