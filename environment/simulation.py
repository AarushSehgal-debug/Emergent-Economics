import sys
import os
import json
import random
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.agent import Agent
from environment.negotiate import negotiate

def run_simulation(model="llama3.2", rounds=20, num_agents=6):
    print(f"\n{'='*50}")
    print(f"EMERGENT ECONOMICS SIMULATION")
    print(f"Model: {model} | Rounds: {rounds} | Agents: {num_agents}")
    print(f"{'='*50}")

    names = ["Ara", "Ben", "Cal", "Dia", "Eve", "Fox"]
    agents = [Agent(name, model) for name in names[:num_agents]]

    random.choice(agents).has_the_map = True
    map_holder = [a for a in agents if a.has_the_map][0]
    print(f"\n[THE MAP] {map_holder.name} starts with The Map")

    all_logs = []

    for round_num in range(1, rounds + 1):
        print(f"\n--- ROUND {round_num} ---")

        for agent in agents:
            if agent.alive:
                agent.consume_energy()
                if agent.inventory["computing_power"] > 0:
                    bonus = agent.inventory["computing_power"] * 2
                    agent.inventory["labor_credits"] += bonus

        alive_agents = [a for a in agents if a.alive]
        if len(alive_agents) < 2:
            print("\n[SIMULATION ENDED] Not enough agents alive to trade")
            break

        random.shuffle(alive_agents)
        for i in range(0, len(alive_agents) - 1, 2):
            agent_a = alive_agents[i]
            agent_b = alive_agents[i + 1]
            log = negotiate(agent_a, agent_b)
            log["round"] = round_num
            all_logs.append(log)

        print(f"\n[WEALTH SNAPSHOT - Round {round_num}]")
        for agent in agents:
            status = "DEAD" if not agent.alive else ""
            print(f"  {agent.name}: {agent.total_wealth()} wealth points {status}")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"logs/simulation_{model}_{timestamp}.json"
    with open(log_filename, "w") as f:
        json.dump({
            "model": model,
            "rounds": rounds,
            "agents": [a.status() for a in agents],
            "trades": all_logs
        }, f, indent=2)

    print(f"\n[SAVED] Log written to {log_filename}")
    return all_logs, agents

if __name__ == "__main__":
    run_simulation(model="gemma3", rounds=10)
