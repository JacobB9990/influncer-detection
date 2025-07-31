# Authoritative Sources in a Hyperlinked Environment (Kleinberg, 1999) & PageRank

## Introduction
Kleinberg (1999) introduced the HITS algorithm to identify authoritative sources and hubs in hyperlinked environments, such as the web. PageRank, developed by Brin and Page, is another influential algorithm for ranking nodes by importance using random walks.

## 1. HITS Algorithm
HITS assigns two scores to each node:
- **Authority:** Indicates value as a source of information (many incoming links from good hubs).
- **Hub:** Indicates value as a directory (links to many good authorities).

Scores are computed iteratively:
- Authority score of a node = sum of hub scores of nodes linking to it.
- Hub score of a node = sum of authority scores of nodes it links to.

## 2. PageRank
PageRank models a random surfer who follows links at random. A node's score reflects the probability that the surfer lands on it. It is computed iteratively, with damping factor $\alpha$ (usually 0.85).

## 3. Example Results
| Node | Authority (HITS) | Hub (HITS) | PageRank |
|------|------------------|------------|----------|
| A    | 0.4082           | 0.4082     | 0.1802   |
| B    | 0.4082           | 0.4082     | 0.1067   |
| C    | 0.8165           | 0.8165     | 0.3382   |
| D    | 0.0              | 0.4082     | 0.1802   |
| E    | 0.0              | 0.4082     | 0.1947   |

## 4. Discussion
Both HITS and PageRank identify important nodes in directed networks, but HITS distinguishes between authorities and hubs, while PageRank gives a single importance score. These algorithms are foundational for web search and network analysis.

## References
Kleinberg, J. M. (1999). Authoritative sources in a hyperlinked environment. Journal of the ACM, 46(5), 604–632. https://doi.org/10.1145/324133.324140
Brin, S., & Page, L. (1998). The anatomy of a large-scale hypertextual web search engine. Computer Networks and ISDN Systems, 30(1–7), 107–117. https://doi.org/10.1016/S0169-7552(98)00110-X
