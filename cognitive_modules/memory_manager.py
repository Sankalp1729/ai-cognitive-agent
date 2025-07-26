import json
import os

class MemoryManager:
    def __init__(self, memory_path="logs/memory.json"):
        self.memory_path = memory_path
        self.memory = self.load_memory()

    def load_memory(self):
        if os.path.exists(self.memory_path):
            with open(self.memory_path, "r") as f:
                return json.load(f)
        return {"senders": {}, "patterns": {}}

    def update_sender(self, sender):
        self.memory["senders"][sender] = self.memory["senders"].get(sender, 0) + 1
        self.save_memory()

    def save_memory(self):
        with open(self.memory_path, "w") as f:
            json.dump(self.memory, f, indent=4)
