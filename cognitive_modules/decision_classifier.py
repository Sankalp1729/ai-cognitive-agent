import random

class DecisionClassifier:
    ACTIONS = ["Reply", "Archive", "Later", "Forward", "Add to Calendar", "Tag"]

    def classify(self, item):
        content = item["content"].lower()
        action = "Archive"
        reason = ""

        # Simple keyword-based decision
        if "meeting" in content or "schedule" in content or "appointment" in content:
            action = "Add to Calendar"
            reason = "Detected scheduling keywords"
        elif "offer" in content or "discount" in content:
            action = "Archive"
            reason = "Promotional content"
        elif item["type"] == "tasks":
            action = "Later"
            reason = "Detected as task"
        elif item["type"] == "notes":
            action = "Tag"
            reason = "Detected as note"
        else:
            action = random.choice(self.ACTIONS)
            reason = "Random fallback"

        confidence = round(random.uniform(0.7, 0.99), 2)
        return {"action": action, "confidence": confidence, "reason": reason}

