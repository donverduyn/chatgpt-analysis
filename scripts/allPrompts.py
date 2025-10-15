# allPrompts.py
import json
import pandas as pd

def load_prompts(json_path="../assets/conversations.json"):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    prompts = []

    def traverse_mapping(mapping, node_id, parent_id=None):
        node = mapping[node_id]
        message = node.get("message")

        if message and message.get("author", {}).get("role") == "user":
            parts = message.get("content", {}).get("parts", [])
            text = "".join(parts) if parts else ""
            prompts.append({
                "node_id": node_id,
                "parent_id": parent_id,
                "text": text,
                "create_time": message.get("create_time"),
                "update_time": message.get("update_time")
            })

        for child_id in node.get("children", []):
            traverse_mapping(mapping, child_id, parent_id=node_id)

    all_prompts = []
    for convo in data:
        mapping = convo["mapping"]
        root_nodes = [nid for nid, n in mapping.items() if n.get("parent") is None]
        for root_id in root_nodes:
            traverse_mapping(mapping, root_id)
        all_prompts.extend(prompts)
        prompts.clear()

    df = pd.DataFrame(all_prompts)
    return df