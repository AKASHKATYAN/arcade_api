import json
import os

def load_data():
    if not os.path.exists("records.json"):
        return []

    with open("records.json", "r") as f:
        content = f.read().strip()
        if not content:
            return []
        return json.loads(content)

def write_data(data):
    with open("records.json", "w") as f:
        json.dump(data, f, indent=4)

       