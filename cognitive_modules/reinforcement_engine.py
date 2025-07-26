import json
import os

class ReinforcementEngine:
    def __init__(self, q_table_path="logs/q_table.json"):
        self.q_table_path = q_table_path
        self.q_table = self.load_q_table()

    def load_q_table(self):
        if os.path.exists(self.q_table_path):
            try:
                with open(self.q_table_path, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}  # If file is empty or invalid
        return {}

    def save_q_table(self):
        with open(self.q_table_path, "w") as f:
            json.dump(self.q_table, f, indent=4)

    def update(self, state, action, reward):
        # Ensure state exists
        if state not in self.q_table:
            self.q_table[state] = {}
        # Update action value
        current_value = self.q_table[state].get(action, 0)
        self.q_table[state][action] = current_value + reward
        self.save_q_table()

    def choose_action(self, state):
        if state in self.q_table and self.q_table[state]:
            return max(self.q_table[state], key=self.q_table[state].get)
        return None
