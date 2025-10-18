import json
from pathlib import Path
from typing import Optional

import pandas as pd


class ChatGPTConversation:
    """Access ChatGPT JSON conversations as a single pandas DataFrame."""

    def __init__(self, json_path: str | Path):
        self.json_path = Path(json_path)
        self._data: Optional[list] = None
        self._df: Optional[pd.DataFrame] = None

    def _load_json(self):
        if self._data is None:
            if not self.json_path.exists():
                raise FileNotFoundError(f"{self.json_path} not found")
            with open(self.json_path, "r", encoding="utf-8") as f:
                self._data = json.load(f)
            if not isinstance(self._data, list):
                raise ValueError("Expected JSON root to be an array of conversations")
        return self._data

    def _build_dataframe(self):
        if self._df is not None:
            return self._df

        data = self._load_json()
        rows = []

        for conv_index, conv in enumerate(data):
            mapping = conv.get("mapping", {})
            visited = set()
            root_nodes = [
                nid for nid, node in mapping.items() if node.get("parent") is None
            ]
            stack = list(reversed(root_nodes))

            while stack:
                node_id = stack.pop()
                if node_id in visited:
                    continue
                visited.add(node_id)

                node = mapping[node_id]
                msg = node.get("message")
                if msg:
                    parts = msg.get("content", {}).get("parts", [])
                    text = " ".join(part for part in parts if isinstance(part, str))
                    rows.append(
                        {
                            "conv_index": conv_index,
                            "conversation_title": conv.get("title", ""),
                            "node_id": node_id,
                            "role": msg.get("author", {}).get("role"),
                            "text": text,
                            "create_time": msg.get("create_time"),
                            "update_time": msg.get("update_time"),
                        }
                    )

                stack.extend(reversed(node.get("children", [])))

        self._df = pd.DataFrame(rows)
        return self._df

    # --- Public API ---

    def get_dataframe(self) -> pd.DataFrame:
        """Return the full DataFrame of all messages."""
        return self._build_dataframe()

    def get_conversations(self) -> pd.DataFrame:
        """Return a DataFrame of conversation summaries."""
        df = self._build_dataframe()
        summary = (
            df.groupby("conv_index")
            .agg(
                conversation_title=("conversation_title", "first"),
                message_count=("text", "count"),
            )
            .reset_index()
        )
        return summary

    def get_messages_by_conv(self, conv_index: int) -> pd.DataFrame:
        """Return all messages for a specific conversation."""
        df = self._build_dataframe()
        return df[df["conv_index"] == conv_index].reset_index(drop=True)

    def search_messages(
        self, query: str, conv_index: Optional[int] = None
    ) -> pd.DataFrame:
        """Search messages, optionally within a conversation."""
        df = self._build_dataframe()
        df_search = df[df["text"].str.contains(query, case=False, na=False)]
        if conv_index is not None:
            df_search = df_search[df_search["conv_index"] == conv_index]
        return df_search.reset_index(drop=True)
