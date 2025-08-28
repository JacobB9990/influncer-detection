# simulate_sir.py
import random
from typing import Set
from kcore_analysis import load_and_rank_graph 

def simulate_sir(G, seed: int, beta=0.05, mu=0.01, steps=50) -> int:
    susceptible = set(G.nodes()) - {seed}
    infected: Set[int] = {seed}
    recovered: Set[int] = set()

    for _ in range(steps):
        new_infected: Set[int] = set()
        new_recovered: Set[int] = set()

        for node in infected:
            for neighbor in G.neighbors(node):
                if neighbor in susceptible and random.random() < beta:
                    new_infected.add(neighbor)
            if random.random() < mu:
                new_recovered.add(node)

        infected = (infected | new_infected) - new_recovered
        susceptible -= new_infected
        recovered |= new_recovered

        if not infected:
            break

    return len(recovered)

if __name__ == "__main__":
    G, core_numbers, degree_numbers, sorted_nodes = load_and_rank_graph("Identification-of-infuentail-spreaders-in-complex-networks/data/email-Eu-core.txt")

    seeds = sorted_nodes[:10]
    results = {}

    for seed in seeds:
        total_recovered = 0
        runs = 20
        for _ in range(runs):
            total_recovered += simulate_sir(G, seed, beta=0.05, mu=0.01, steps=50)
        avg_recovered = total_recovered / runs
        results[seed] = avg_recovered
        print(f"Seed {seed}: Average outbreak size over {runs} runs = {avg_recovered:.2f}")
