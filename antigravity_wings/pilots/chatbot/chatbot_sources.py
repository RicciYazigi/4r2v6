# pilots/chatbot/chatbot_sources.py

import json
from pathlib import Path
from typing import List, Dict, Any
from antigravity_wings.observation.registry import DataSource

class ChatLogSource(DataSource):
    """Lee logs de conversaciones históricas del chatbot."""
    def __init__(self, log_path: Path):
        self._path = log_path

    @property
    def name(self) -> str:
        return "chat_history_logs"

    def collect(self) -> List[Dict[str, Any]]:
        if not self._path.exists():
            return []
        try:
            with self._path.open("r", encoding="utf-8") as f:
                return [json.loads(line) for line in f if line.strip()]
        except Exception:
            return []

class ChatPolicySource(DataSource):
    """DataSource que expone las políticas sensibles configuradas."""
    def __init__(self, policy_list: List[str]):
        self._policies = policy_list

    @property
    def name(self) -> str:
        return "chat_policies"

    def collect(self) -> List[Dict[str, Any]]:
        # Devuelve las políticas como una lista de diccionarios para el pipeline
        return [{"policy": p, "level": "restricted"} for p in self._policies]
