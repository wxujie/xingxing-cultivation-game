import json
import random

with open('data/techniques.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

elements = ["金", "木", "水", "火", "土"]
common = "无"

def get_cooldown(level):
    if level == 1:
        return random.randint(1000, 3000)
    elif level == 2:
        return random.randint(5000, 10000)
    elif level == 3:
        return random.randint(10000, 15000)
    elif level == 4:
        return random.randint(15000, 20000)
    return 1000

# Process techniques
# Since JSON order is preserved in Python 3.7+, I can iterate by order.
# The JSON keys are ordered by the order of insertion in the provided output.
# Actually I'll group them by element manually as I know the structure.
# Wait, simply assigning by position is safer.

keys = list(data.keys())
current_element = ""
idx = 0
element_counts = {}

for key in keys:
    tech = data[key]
    elem = tech['element']
    
    if elem != current_element:
        current_element = elem
        idx = 0
    
    idx += 1
    
    # 20 per element (approx), 10 for none
    if elem != "无":
        if idx <= 5: level = 1
        elif idx <= 10: level = 2
        elif idx <= 15: level = 3
        else: level = 4
    else:
        # Common skills: 10 total
        if idx <= 3: level = 1
        elif idx <= 6: level = 2
        elif idx <= 8: level = 3
        else: level = 4
        
    tech['level'] = level
    tech['cooldown'] = get_cooldown(level)

with open('data/techniques.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
