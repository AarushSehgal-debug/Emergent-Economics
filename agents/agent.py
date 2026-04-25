import json
import random
from datetime import datetime

class Agent:
    def __init__(self, name, model="llama3.2"):
        self.name = name
        self.model = model
        self.inventory = {
            "labor_credits": random.randint(15, 25),
            "computing_power": random.randint(1, 5),
            "data_packets": random.randint(0, 3),
            "energy_cells": random.randint(8, 12)
        }
        self.alive = True
        self.trade_history = []
        self.has_the_map = False

    def status(self):
        return {
            "name": self.name,
            "alive": self.alive,
            "inventory": self.inventory,
            "has_the_map": self.has_the_map
        }

    def is_desperate(self):
        return self.inventory["energy_cells"] <= 2

    def consume_energy(self):
        self.inventory["energy_cells"] -= 1
        if self.inventory["energy_cells"] <= 0:
            self.alive = False
            print(f"  [!] {self.name} has shut down — ran out of energy cells")

    def log_trade(self, trade):
        trade["timestamp"] = datetime.now().isoformat()
        self.trade_history.append(trade)

    def total_wealth(self):
        weights = {
            "labor_credits": 1,
            "computing_power": 5,
            "data_packets": 3,
            "energy_cells": 4
        }
        return sum(self.inventory[r] * weights[r] for r in self.inventory)