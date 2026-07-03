import json
from enum import Enum
from datetime import datetime
from dataclasses import is_dataclass, asdict
from typing import Any

class AGWJsonEncoder(json.JSONEncoder):
    """Encoder JSON para tipos de Antigravity Wings (Enum, Datetime, Dataclass)."""
    def default(self, obj: Any) -> Any:
        if isinstance(obj, Enum):
            return obj.value
        if isinstance(obj, datetime):
            return obj.isoformat()
        if is_dataclass(obj) and not isinstance(obj, type):
            return asdict(obj)
        return super().default(obj)

def agw_dumps(obj: Any, indent: int = 2) -> str:
    """Helper para serializar objetos AGW a string JSON."""
    return json.dumps(obj, cls=AGWJsonEncoder, indent=indent)

def agw_loads(s: str) -> Any:
    """Helper para deserializar (wrapper estándar por ahora)."""
    return json.loads(s)
