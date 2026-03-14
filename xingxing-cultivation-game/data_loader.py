import json
import os

def load_json(filename):
    with open(f"data/{filename}", "r", encoding="utf-8") as f:
        return json.load(f)

def load_all():
    return {
        "realms": load_json("realms.json"),
        "characters": load_json("characters.json"),
        "techniques": load_json("techniques.json"),
        "enemies": load_json("enemies.json"),
        "items": load_json("items.json")
    }
