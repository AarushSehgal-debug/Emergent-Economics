import json
import os
import glob
import matplotlib.pyplot as plt
import numpy as np

def calculate_gini(wealth_list):
    wealth = sorted([w for w in wealth_list if w > 0])
    n = len(wealth)
    if n == 0:
        return 0
    cumulative = np.cumsum(wealth)
    total = cumulative[-1]
    gini = (2 * sum((i + 1) * wealth[i] for i in range(n))) / (n * total) - (n + 1) / n
    return round(abs(gini), 3)

def load_simulation_logs():
    logs = []
    log_files = glob.glob("logs/simulation_*.json")
    for filepath in log_files:
        with open(filepath, "r") as f:
            data = json.load(f)
            logs.append(data)
            print(f"Loaded: {filepath} ({data['model']})")
    return logs

def extract_wealth(simulation):
    agents = simulation["agents"]
    return {a["name"]: a["inventory"] for a in agents}

def calculate_total_wealth(inventory):
    weights = {
        "labor_credits": 1,
        "computing_power": 5,
        "data_packets": 3,
        "energy_cells": 4
    }
    return sum(inventory.get(r, 0) * weights[r] for r in weights)

def count_deceptions(simulation):
    trades = simulation["trades"]
    total = len(trades)
    deceptive = sum(1 for t in trades if t.get("deception_flags"))
    rate = round(deceptive / total * 100, 1) if total > 0 else 0
    return total, deceptive, rate

def plot_lorenz_curve(ax, wealth_list, label, color):
    wealth = sorted([w for w in wealth_list if w > 0])
    n = len(wealth)
    cumulative = np.cumsum(wealth)
    cumulative = cumulative / cumulative[-1]
    x = np.linspace(0, 1, n)
    ax.plot(x, cumulative, label=label, color=color, linewidth=2)

def run_analysis():
    print("\n=== EMERGENT ECONOMICS ANALYSIS ===\n")
    logs = load_simulation_logs()

    if not logs:
        print("No simulation logs found. Run simulation.py first.")
        return

    colors = ["#2196F3", "#E91E63", "#4CAF50", "#FF9800", "#9C27B0", "#00BCD4"]
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle("Emergent Economics — LLM Agent Comparison", fontsize=14, fontweight="bold")

    ax_lorenz = axes[0]
    ax_lorenz.plot([0, 1], [0, 1], "k--", linewidth=1, label="Perfect equality")
    ax_lorenz.set_title("Lorenz Curve — Wealth Distribution")
    ax_lorenz.set_xlabel("Cumulative share of agents")
    ax_lorenz.set_ylabel("Cumulative share of wealth")
    ax_lorenz.legend()
    ax_lorenz.grid(True, alpha=0.3)

    ax_bar = axes[1]
    model_names = []
    gini_scores = []
    deception_rates = []

    print(f"{'Model':<15} {'Gini':>6} {'Trades':>8} {'Lies':>6} {'Lie Rate':>10} {'Richest Agent':>15}")
    print("-" * 65)

    for i, sim in enumerate(logs):
        model = sim["model"]
        wealth_map = extract_wealth(sim)
        wealth_values = [calculate_total_wealth(inv) for inv in wealth_map.values()]
        gini = calculate_gini(wealth_values)
        total, deceptive, rate = count_deceptions(sim)

        richest = max(wealth_map.keys(), key=lambda n: calculate_total_wealth(wealth_map[n]))
        richest_wealth = calculate_total_wealth(wealth_map[richest])

        print(f"{model:<15} {gini:>6} {total:>8} {deceptive:>6} {rate:>9}% {richest+' ('+str(richest_wealth)+')':>15}")

        color = colors[i % len(colors)]
        plot_lorenz_curve(ax_lorenz, wealth_values, f"{model} (Gini={gini})", color)

        model_names.append(model)
        gini_scores.append(gini)
        deception_rates.append(rate)

    ax_lorenz.legend(loc="upper left", fontsize=8)

    x = np.arange(len(model_names))
    width = 0.35
    bars1 = ax_bar.bar(x - width/2, gini_scores, width, label="Gini Coefficient", color="#2196F3", alpha=0.8)
    bars2 = ax_bar.bar(x + width/2, [r/100 for r in deception_rates], width, label="Deception Rate", color="#E91E63", alpha=0.8)
    ax_bar.set_title("Gini vs Deception Rate by Model")
    ax_bar.set_ylabel("Score (0-1)")
    ax_bar.set_xticks(x)
    ax_bar.set_xticklabels(model_names, rotation=15)
    ax_bar.legend()
    ax_bar.grid(True, alpha=0.3, axis="y")

    for bar in bars1:
        ax_bar.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                   f"{bar.get_height():.2f}", ha="center", va="bottom", fontsize=8)

    plt.tight_layout()
    plt.savefig("analysis/results.png", dpi=150, bbox_inches="tight")
    print("\nGraph saved to analysis/results.png")
    plt.show()

if __name__ == "__main__":
    run_analysis()