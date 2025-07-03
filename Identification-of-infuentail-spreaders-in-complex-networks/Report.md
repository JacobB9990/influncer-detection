# Complex Influential Spreaders

## Introduction
Influential spreaders in complex networks are nodes that can maximize the spread of information, ideas, or epidemics through a network. This is important for understanding viral marketing, disease outbreaks, and social influence.  
The paper by Kitsak et al. (2010) introduces the concept of using **k-core decomposition** to identify such influential nodes, arguing that nodes in higher cores tend to be better spreaders than nodes with simply high degree.  

## 1. K-core Decomposition and Degree Centrality

### K-core Decomposition
K-core decomposition recusively removes nodes with degree less than k, revealing nested layers, cores, in the network. The **core number** of a node is the highest k-core it belongs to. Nodes in higher cores are often more central to spreading processes.

### Degree Centrality
As I stated in a previous report. Degree Centrality is the simplest measure, counting the number of direct connections a node has.

## 2. Data
I analyze the email-Eu-core network, representing email communication in a European research institution.  
- Nodes: 1005  
- Edges: 25571  
- Undirected and unweighted

Note we had to remove self loops.

## 3. SIR Diffusion Model

We simulated a epidemic spreading with the **SIR (Susceptible-Infected-Recovered)** model:
- **Susceptible (S):** Nodes that can become infected.  
- **Infected (I):** Nodes that can infect susceptible neighbors.  
- **Recovered (R):** Nodes that are immune and no longer spread infection.

**Steps**:
- Start with a seed node infected, all others susceptible.  
- At each time step:  
  - Each infected node infects susceptible neighbors with probability β = 0.05.  
  - Each infected node recovers with probability μ = 0.01.  
- Simulation runs for 50 steps or until no infected remain.

Then average the final outbreak size.

## 4. Results
| Seed Node | Average Outbreak Size (20 runs) |
| --------- | ------------------------------- |
| 160       | 342.35                          |
| 121       | 342.10                          |
| 82        | 345.25                          |
| 107       | 338.70                          |
| 86        | 341.20                          |
| 62        | 342.40                          |
| 434       | 341.80                          |
| 166       | 336.55                          |
| 183       | 338.00                          |
| 64        | 337.80                          |

These results confirm that nodes with high k-core and degree centrality values correspond to influential spreaders in the network.

## 5. Discussion
Our simulation results support the paper’s claim that k-core decomposition effectively identifies influential spreaders in complex networks. Nodes in the highest cores consistently triggered the largest outbreaks in the SIR model. While degree centrality captures local connectivity, it does not fully reflect a node’s position within the broader network structure. It is important to understand that considering a node's overall position in the network, rather than just direct connections, to identify key spreaders in real-world networks.

## References 
Kitsak, M., Gallos, L.K., Havlin, S., Liljeros, F., Muchnik, L., Stanley, H.E., & Makse, H.A. (2010). Identification of influential spreaders in complex networks. *Nature Physics*, 6(11), 888–893. https://doi.org/10.1038/nphys1746

SNAP Datasets: Email-Eu-core network. Stanford Large Network Dataset Collection. https://snap.stanford.edu/data/email-Eu-core.html
