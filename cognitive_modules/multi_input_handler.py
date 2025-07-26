import json
import os
import uuid

class MultiInputHandler:
    def __init__(self, input_dir="inputs"):
        self.input_dir = input_dir

    def load_inputs(self):
        all_data = []
        for file_name in os.listdir(self.input_dir):
            if file_name.endswith(".json"):
                path = os.path.join(self.input_dir, file_name)
                with open(path, "r") as f:
                    data = json.load(f)
                    input_type = file_name.replace("sample_", "").replace(".json", "")
                    all_data.extend(self.normalize_data(data, input_type))
        return all_data

    def normalize_data(self, data_list, input_type):
        normalized = []
        for item in data_list:
            content = self.extract_content(item)
            normalized.append({
                "id": str(uuid.uuid4()),
                "type": input_type,
                "content": content,
                "metadata": item
            })
        return normalized

    def extract_content(self, item):
        if "body" in item:  # Emails
            return item.get("subject", "") + " " + item.get("body", "")
        if "title" in item and "content" in item:  # Notes/Articles
            return item["title"] + " " + item["content"]
        if "title" in item:  # Tasks
            return item["title"]
        return str(item)
