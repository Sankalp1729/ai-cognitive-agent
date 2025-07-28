import json
import os

class DecisionClassifier:
    def __init__(self):
        self.weights_file = "weights.json"
        self.default_weights = {
            "Schedule": 1.0,
            "Ignore": 1.0,
            "Mark Important": 1.0,
            "Summarize": 1.0
        }
        self.action_weights = self.load_weights()

    def load_weights(self):
        if os.path.exists(self.weights_file):
            with open(self.weights_file, "r") as f:
                return json.load(f)
        return self.default_weights.copy()

    def save_weights(self):
        with open(self.weights_file, "w") as f:
            json.dump(self.action_weights, f, indent=4)

    def classify(self, item):
        text = item["content"].lower()
        action = "Ignore"
        reason = "Default rule applied"
        base_confidence = 0.5

        if "meeting" in text or "schedule" in text:
            action, base_confidence, reason = "Schedule", 0.8, "Detected meeting keywords"
        elif "discount" in text or "offer" in text:
            action, base_confidence, reason = "Ignore", 0.7, "Detected promotional content"
        elif "report" in text or "project" in text:
            action, base_confidence, reason = "Mark Important", 0.85, "Detected project-related content"
        elif "http" in text or "link" in text:
            action, base_confidence, reason = "Summarize", 0.6, "Detected external link for summary"

        # Adjust confidence using RL weights
        adjusted_confidence = base_confidence * self.action_weights[action]

        return {
            "action": action,
            "confidence": round(adjusted_confidence, 2),
            "reason": reason
        }

    def update_weights(self, old_action, new_action):
        if old_action == new_action:
            # Positive feedback: Increase confidence
            self.action_weights[new_action] *= 1.05
        else:
            # Negative feedback: Penalize old, boost new
            self.action_weights[old_action] *= 0.95
            self.action_weights[new_action] *= 1.10

        # Normalize weights (optional to prevent runaway growth)
        for k in self.action_weights:
            if self.action_weights[k] > 2.0:
                self.action_weights[k] = 2.0
            if self.action_weights[k] < 0.5:
                self.action_weights[k] = 0.5

        self.save_weights()

