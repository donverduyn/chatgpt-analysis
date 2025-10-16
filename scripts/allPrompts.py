"""allPrompts.py

Robust, non-recursive extractor for user prompts from the OpenAI-style
conversation export structure. Handles nested/structured "parts" entries by
normalizing them to text, avoids recursion by using an explicit stack, and
protects against cycles with a visited set and a traversal cap.
"""

import json
from typing import Any, Dict, List

import pandas as pd


def load_prompts(json_path: str = "../assets/conversations.json") -> pd.DataFrame:
    """Load prompts from the conversation JSON and return a DataFrame.

    The function expects the JSON to be a list of conversations where each
    conversation has a `mapping` dict of nodes. Each node may contain a
    `message` object and `children` list. Only messages whose author role is
    "user" are collected.
    """
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    def _extract_text_from_parts(parts: List[Any]) -> str:
        """Normalize a `parts` list into a single string.

        Handles items that are strings, dicts with common text keys, or nested
        parts. Falls back to json.dumps for unknown dict shapes.
        """
        texts: List[str] = []
        for p in parts:
            if isinstance(p, str):
                texts.append(p)
            elif isinstance(p, dict):
                # common keys that may hold textual content
                if isinstance(p.get("text"), str):
                    texts.append(p.get("text"))
                elif isinstance(p.get("content"), str):
                    texts.append(p.get("content"))
                elif isinstance(p.get("parts"), list):
                    texts.append(_extract_text_from_parts(p.get("parts")))
                else:
                    texts.append(json.dumps(p, ensure_ascii=False))
            else:
                texts.append(str(p))
        return "".join(texts)

    all_prompts: List[Dict[str, Any]] = []

    for convo in data:
        mapping: Dict[str, Dict[str, Any]] = convo.get("mapping", {})
        convo_title = convo.get("title") or convo.get("metadata", {}).get("title")

        # per-conversation structures
        prompts: List[Dict[str, Any]] = []
        visited = set()

        def traverse_mapping(start_node_id: str, parent_id: str = None) -> None:
            """Iterative DFS with cycle protection and node cap."""
            stack = [(start_node_id, parent_id)]
            node_count = 0
            max_nodes = 1_000_000
            while stack:
                node_count += 1
                if node_count > max_nodes:
                    raise RuntimeError("traversal aborted: exceeded max node limit")

                node_id, parent = stack.pop()
                if node_id in visited:
                    continue
                visited.add(node_id)

                node = mapping.get(node_id)
                if not node:
                    continue

                message = node.get("message")
                if message and message.get("author", {}).get("role") == "user":
                    parts = message.get("content", {}).get("parts", [])
                    text = _extract_text_from_parts(parts) if parts else ""
                    prompts.append(
                        {
                            "node_id": node_id,
                            "parent_id": parent,
                            "text": text,
                            "title": convo_title,
                            "create_time": message.get("create_time"),
                            "update_time": message.get("update_time"),
                        }
                    )

                children = node.get("children", []) or []
                # push children in reverse so the natural order is preserved
                for child_id in reversed(children):
                    if child_id not in visited:
                        stack.append((child_id, node_id))

        root_nodes = [nid for nid, n in mapping.items() if n.get("parent") is None]
        for root_id in root_nodes:
            traverse_mapping(root_id)

        all_prompts.extend(prompts)

    df = pd.DataFrame(all_prompts)
    return df
