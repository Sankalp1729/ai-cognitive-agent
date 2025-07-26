import matplotlib.pyplot as plt
import json

class InsightVisualizer:
    def plot_actions(self, log_path="logs/actions.json"):
        with open(log_path, "r") as f:
            logs = json.load(f)
        actions = [log["predicted_action"] for log in logs]
        plt.figure(figsize=(8, 5))
        plt.hist(actions, color="skyblue", edgecolor="black")
        plt.title("Action Distribution")
        plt.show()
