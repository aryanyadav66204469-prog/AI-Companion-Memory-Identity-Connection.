import json

FILE = "data/memories.json"

def load_memories():
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_memory(memory):
    memories = load_memories()
    memories.append(memory)

    with open(FILE, "w") as f:
        json.dump(memories, f, indent=4)