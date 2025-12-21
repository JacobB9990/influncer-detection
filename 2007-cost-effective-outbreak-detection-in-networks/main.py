import CELF_SET_K
import CELF_Cost  # Your budget version
import matplotlib.pyplot as plt
import time
import numpy as np
from datetime import datetime

def benchmark_celf_k(path, k_values, MC_init, MC_final, p):
    """Benchmark CELF with fixed k values"""
    results = {
        'k': [],
        'spread': [],
        'runtime': [],
        'nodes': [],
        'marginal_gain': [],
    }
    
    print("="*70)
    print(f"CELF-K BENCHMARK (Fixed K) - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    print(f"Graph: {path}")
    print(f"MC_init: {MC_init}, MC_final: {MC_final}, p: {p}")
    print(f"Testing k values: {k_values}")
    print("="*70 + "\n")
    
    total_start = time.time()
    
    for i, k in enumerate(k_values):
        print(f"\n[{i+1}/{len(k_values)}] Running CELF for k={k}...")
        print("-" * 70)
        
        start = time.time()
        chosen_nodes, spread = CELF_SET_K.main(path, k, MC_init, MC_final, p)
        runtime = time.time() - start
        
        marginal = spread if i == 0 else spread - results['spread'][-1]
        
        results['k'].append(k)
        results['spread'].append(spread)
        results['runtime'].append(runtime)
        results['nodes'].append(list(chosen_nodes))
        results['marginal_gain'].append(marginal)
        
        print(f"✓ k={k:2d} completed in {runtime:6.2f}s")
        print(f"  Spread: {spread:7.2f} | Marginal: {marginal:+6.2f} | Nodes: {sorted(list(chosen_nodes))[:5]}...")
        print("-" * 70)
    
    total_time = time.time() - total_start
    print("\n" + "="*70)
    print(f"CELF-K BENCHMARK COMPLETE - Total time: {total_time:.2f}s")
    print("="*70 + "\n")
    
    return results

def benchmark_celf_budget(path, budgets, MC_init, MC_final, p):
    """Benchmark CELF with budget constraints"""
    results = {
        'budget': [],
        'actual_cost': [],
        'k': [],
        'spread': [],
        'runtime': [],
        'nodes': [],
        'cost_effectiveness': [],
    }
    
    print("="*70)
    print(f"CELF-BUDGET BENCHMARK - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    print(f"Graph: {path}")
    print(f"MC_init: {MC_init}, MC_final: {MC_final}, p: {p}")
    print(f"Testing budgets: {budgets}")
    print("="*70 + "\n")
    
    total_start = time.time()
    
    for i, budget in enumerate(budgets):
        print(f"\n[{i+1}/{len(budgets)}] Running CELF-BUDGET for budget={budget}...")
        print("-" * 70)
        
        start = time.time()
        chosen_nodes, actual_cost, spread = CELF_Cost.main(path, budget, MC_init, MC_final, p)
        runtime = time.time() - start
        
        cost_effectiveness = spread / actual_cost if actual_cost > 0 else 0
        
        results['budget'].append(budget)
        results['actual_cost'].append(actual_cost)
        results['k'].append(len(chosen_nodes))
        results['spread'].append(spread)
        results['runtime'].append(runtime)
        results['nodes'].append(list(chosen_nodes))
        results['cost_effectiveness'].append(cost_effectiveness)
        
        print(f"✓ Budget={budget:.1f} completed in {runtime:6.2f}s")
        print(f"  Used: {actual_cost:.2f} | Seeds: {len(chosen_nodes)} | Spread: {spread:.2f}")
        print(f"  Cost-effectiveness: {cost_effectiveness:.2f} spread/cost")
        print(f"  Nodes: {sorted(list(chosen_nodes))[:5]}...")
        print("-" * 70)
    
    total_time = time.time() - total_start
    print("\n" + "="*70)
    print(f"CELF-BUDGET BENCHMARK COMPLETE - Total time: {total_time:.2f}s")
    print("="*70 + "\n")
    
    return results

def plot_k_results(results, save_path="celf_k_benchmark.png"):
    """Visualize k-constrained CELF results"""
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
    
    k_vals = results['k']
    spreads = results['spread']
    runtimes = results['runtime']
    marginals = results['marginal_gain']
    
    # 1. Spread vs k
    ax1 = fig.add_subplot(gs[0, :])
    ax1.plot(k_vals, spreads, marker='o', linewidth=2.5, markersize=8, 
             color='#2E86AB', label='Total Spread')
    ax1.set_xlabel("k (number of seeds)", fontsize=13)
    ax1.set_ylabel("Estimated Spread", fontsize=13)
    ax1.set_title("CELF-K: Influence Spread vs Seed Set Size", fontsize=15, fontweight='bold')
    ax1.grid(True, alpha=0.3, linestyle='--')
    ax1.legend()
    
    # 2. Marginal gains
    ax2 = fig.add_subplot(gs[1, 0])
    colors = ['#A23B72' if m >= 0 else '#D32F2F' for m in marginals]
    ax2.bar(k_vals, marginals, color=colors, alpha=0.7, edgecolor='black', linewidth=0.5)
    ax2.set_xlabel("k (number of seeds)", fontsize=11)
    ax2.set_ylabel("Marginal Gain", fontsize=11)
    ax2.set_title("Marginal Gain per Additional Seed", fontsize=13, fontweight='bold')
    ax2.grid(True, alpha=0.3, linestyle='--', axis='y')
    ax2.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
    
    # 3. Runtime per k
    ax3 = fig.add_subplot(gs[1, 1])
    ax3.plot(k_vals, runtimes, marker='s', linewidth=2, markersize=6, 
             color='#F18F01', label='Runtime')
    ax3.set_xlabel("k (number of seeds)", fontsize=11)
    ax3.set_ylabel("Runtime (seconds)", fontsize=11)
    ax3.set_title("Computation Time per k", fontsize=13, fontweight='bold')
    ax3.grid(True, alpha=0.3, linestyle='--')
    ax3.legend()
    
    # 4. Cumulative spread percentage
    ax4 = fig.add_subplot(gs[2, 0])
    max_spread = spreads[-1]
    spread_pct = [s / max_spread * 100 for s in spreads]
    ax4.plot(k_vals, spread_pct, marker='d', linewidth=2, markersize=6, 
             color='#06A77D')
    ax4.set_xlabel("k (number of seeds)", fontsize=11)
    ax4.set_ylabel("% of Max Spread", fontsize=11)
    ax4.set_title("Cumulative Spread Progress", fontsize=13, fontweight='bold')
    ax4.grid(True, alpha=0.3, linestyle='--')
    ax4.set_ylim([0, 105])
    
    # 5. Efficiency metrics
    ax5 = fig.add_subplot(gs[2, 1])
    spread_per_sec = [s / t if t > 0 else 0 for s, t in zip(spreads, runtimes)]
    ax5.plot(k_vals, spread_per_sec, marker='^', linewidth=2, markersize=6, 
             color='#C73E1D')
    ax5.set_xlabel("k (number of seeds)", fontsize=11)
    ax5.set_ylabel("Spread per Second", fontsize=11)
    ax5.set_title("Computational Efficiency", fontsize=13, fontweight='bold')
    ax5.grid(True, alpha=0.3, linestyle='--')
    
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    print(f"📊 K-benchmark plots saved to: {save_path}")
    plt.show()

def plot_budget_results(results, save_path="celf_budget_benchmark.png"):
    """Visualize budget-constrained CELF results"""
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
    
    budgets = results['budget']
    actual_costs = results['actual_cost']
    k_vals = results['k']
    spreads = results['spread']
    runtimes = results['runtime']
    cost_eff = results['cost_effectiveness']
    
    # 1. Spread vs Budget
    ax1 = fig.add_subplot(gs[0, :])
    ax1.plot(budgets, spreads, marker='o', linewidth=2.5, markersize=8, 
             color='#2E86AB', label='Spread')
    ax1.set_xlabel("Budget", fontsize=13)
    ax1.set_ylabel("Estimated Spread", fontsize=13)
    ax1.set_title("CELF-BUDGET: Influence Spread vs Budget", fontsize=15, fontweight='bold')
    ax1.grid(True, alpha=0.3, linestyle='--')
    ax1.legend()
    
    # 2. Seeds selected vs Budget
    ax2 = fig.add_subplot(gs[1, 0])
    ax2.plot(budgets, k_vals, marker='s', linewidth=2, markersize=7, 
             color='#A23B72', label='Seeds Selected')
    ax2.set_xlabel("Budget", fontsize=11)
    ax2.set_ylabel("Number of Seeds (k)", fontsize=11)
    ax2.set_title("Seeds Selected vs Budget", fontsize=13, fontweight='bold')
    ax2.grid(True, alpha=0.3, linestyle='--')
    ax2.legend()
    
    # 3. Budget utilization
    ax3 = fig.add_subplot(gs[1, 1])
    utilization = [ac / b * 100 if b > 0 else 0 for ac, b in zip(actual_costs, budgets)]
    ax3.bar(range(len(budgets)), utilization, color='#F18F01', alpha=0.7)
    ax3.set_xlabel("Budget Level", fontsize=11)
    ax3.set_ylabel("Budget Utilized (%)", fontsize=11)
    ax3.set_title("Budget Utilization", fontsize=13, fontweight='bold')
    ax3.set_xticks(range(len(budgets)))
    ax3.set_xticklabels([f"${b:.0f}" for b in budgets], rotation=45)
    ax3.grid(True, alpha=0.3, linestyle='--', axis='y')
    ax3.set_ylim([0, 105])
    
    # 4. Cost-effectiveness
    ax4 = fig.add_subplot(gs[2, 0])
    ax4.plot(budgets, cost_eff, marker='d', linewidth=2, markersize=6, 
             color='#06A77D')
    ax4.set_xlabel("Budget", fontsize=11)
    ax4.set_ylabel("Spread per Unit Cost", fontsize=11)
    ax4.set_title("Cost-Effectiveness (Spread / Cost)", fontsize=13, fontweight='bold')
    ax4.grid(True, alpha=0.3, linestyle='--')
    
    # 5. Runtime
    ax5 = fig.add_subplot(gs[2, 1])
    ax5.plot(budgets, runtimes, marker='^', linewidth=2, markersize=6, 
             color='#C73E1D')
    ax5.set_xlabel("Budget", fontsize=11)
    ax5.set_ylabel("Runtime (seconds)", fontsize=11)
    ax5.set_title("Computation Time vs Budget", fontsize=13, fontweight='bold')
    ax5.grid(True, alpha=0.3, linestyle='--')
    
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    print(f"📊 Budget-benchmark plots saved to: {save_path}")
    plt.show()

def print_k_summary(results):
    """Print summary table for k-constrained results"""
    print("\n" + "="*90)
    print("CELF-K: DETAILED RESULTS TABLE")
    print("="*90)
    print(f"{'k':>3} | {'Spread':>8} | {'Marginal':>9} | {'% of k=1':>9} | {'Runtime':>9} | {'Top Nodes'}")
    print("-"*90)
    
    for i in range(len(results['k'])):
        k = results['k'][i]
        spread = results['spread'][i]
        marginal = results['marginal_gain'][i]
        pct = (marginal / results['spread'][0] * 100) if i > 0 and results['spread'][0] > 0 else 100.0
        runtime = results['runtime'][i]
        nodes = results['nodes'][i][:3]
        
        violation = "⚠️" if marginal < -0.5 else ""
        print(f"{k:3d} | {spread:8.2f} | {marginal:+9.2f} | {pct:8.2f}% | {runtime:8.2f}s | {nodes} {violation}")
    
    print("="*90 + "\n")

def print_budget_summary(results):
    """Print summary table for budget-constrained results"""
    print("\n" + "="*100)
    print("CELF-BUDGET: DETAILED RESULTS TABLE")
    print("="*100)
    print(f"{'Budget':>8} | {'Used':>8} | {'Util%':>6} | {'Seeds':>5} | {'Spread':>8} | {'Cost-Eff':>9} | {'Runtime':>9} | {'Top Nodes'}")
    print("-"*100)
    
    for i in range(len(results['budget'])):
        budget = results['budget'][i]
        cost = results['actual_cost'][i]
        util = cost / budget * 100 if budget > 0 else 0
        k = results['k'][i]
        spread = results['spread'][i]
        eff = results['cost_effectiveness'][i]
        runtime = results['runtime'][i]
        nodes = results['nodes'][i][:3]
        
        print(f"{budget:8.1f} | {cost:8.2f} | {util:5.1f}% | {k:5d} | {spread:8.2f} | {eff:9.3f} | {runtime:8.2f}s | {nodes}")
    
    print("="*100 + "\n")

def main():
    path = "2007-cost-effective-outbreak-detection-in-networks/facebook_combined.txt"
    
    # Shared parameters
    MC_init = 5
    MC_final = 10
    p = 0.1
    
    print("\n" + "="*70)
    print("CELF BENCHMARK SUITE")
    print("="*70)
    print("\nChoose benchmark mode:")
    print("  1) K-constrained CELF (fixed number of seeds)")
    print("  2) Budget-constrained CELF (fixed budget)")
    print("  3) Both (compare K vs Budget)")
    print("="*70)
    
    choice = input("\nEnter choice (1/2/3): ").strip()
    
    if choice == "1":
        # K-constrained benchmark
        k_values = list(range(1, 11))  # k=1 to k=10
        results = benchmark_celf_k(path, k_values, MC_init, MC_final, p)
        print_k_summary(results)
        plot_k_results(results)
        
    elif choice == "2":
        # Budget-constrained benchmark
        budgets = [5, 10, 15, 20, 30, 40, 50]  # Different budget levels
        results = benchmark_celf_budget(path, budgets, MC_init, MC_final, p)
        print_budget_summary(results)
        plot_budget_results(results)
        
    elif choice == "3":
        # Both - run and compare
        print("\n🔵 Running K-constrained CELF...")
        k_values = list(range(1, 11))
        k_results = benchmark_celf_k(path, k_values, MC_init, MC_final, p)
        print_k_summary(k_results)
        plot_k_results(k_results)
        
        print("\n🟢 Running Budget-constrained CELF...")
        budgets = [5, 10, 15, 20, 30, 40, 50]
        budget_results = benchmark_celf_budget(path, budgets, MC_init, MC_final, p)
        print_budget_summary(budget_results)
        plot_budget_results(budget_results)
        
        # Comparison plot
        fig, ax = plt.subplots(1, 1, figsize=(10, 6))
        ax.plot(k_results['k'], k_results['spread'], 
                marker='o', linewidth=2.5, markersize=8, 
                color='#2E86AB', label='K-constrained')
        ax.plot(budget_results['k'], budget_results['spread'], 
                marker='s', linewidth=2.5, markersize=8, 
                color='#A23B72', label='Budget-constrained')
        ax.set_xlabel("Number of Seeds (k)", fontsize=12)
        ax.set_ylabel("Estimated Spread", fontsize=12)
        ax.set_title("Comparison: K-constrained vs Budget-constrained CELF", 
                     fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.legend(fontsize=11)
        plt.tight_layout()
        plt.savefig("celf_comparison.png", dpi=150, bbox_inches='tight')
        print(f"📊 Comparison plot saved to: celf_comparison.png")
        plt.show()
        
    else:
        print("❌ Invalid choice!")
        return
    
    print("\n✅ Benchmark complete!")

if __name__ == "__main__":
    main()