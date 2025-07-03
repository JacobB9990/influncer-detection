import independent_cascade
import linear_threshold 
import page_rank
from matplotlib import pyplot as plt
import networkx as nx
import threading


def generate_graph(n: int = 100, m: int = 2) -> nx.DiGraph:
    G = nx.barabasi_albert_graph(n, m)
    directed_G = G.to_directed()

    for node in directed_G.nodes():
        in_edges = list(directed_G.in_edges(node))
        total = len(in_edges)
        for u, v in in_edges:
            if total > 0:
                directed_G[u][v]["weight"] = 1 / total
            else:
                directed_G[u][v]["weight"] = 0.0

    return directed_G

def display_graph(G: nx.DiGraph) -> None:
    plt.figure(figsize=(10, 10))
    pos = nx.spring_layout(G)
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color="lightblue",
        edge_color="gray",
        node_size=500,
        font_size=10,
        font_color="black",
    )
    plt.show()


if __name__ == "__main__":
    # You can adjust these parameters as needed, but be careful with large values
    # as they can lead to long computation times. I will add parallelization later.
    n = 100
    m = 2
    k = 4
    simulations = 1000

    try:
        G = generate_graph(n, m)
        
        print("Independent Cascade Model Simulation: ")
        independent_cascade.run_simulation(n, m, k, simulations, G)
        print("\nLinear Threshold Model Simulation: ")
        linear_threshold .run_simulation(n, m, k, simulations, G)
        print("\nPageRank Model Simulation: ")
        page_rank.run_simulation(n, m, k, simulations, G)
        
        display_graph(G)
        
        
    except KeyboardInterrupt:
        print("Simulation interrupted by user.")
    # except Exception as e:
    #     print(f"An error occurred: {e}")
