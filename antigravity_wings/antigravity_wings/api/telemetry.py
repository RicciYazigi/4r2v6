import logging
import time
import json
from datetime import datetime
from typing import Dict, Any

logger = logging.getLogger(__name__)

class HealthMonitor:
    def __init__(self):
        self.start_time = time.time()
        self.metrics = {
            "requests_total": 0,
            "errors_total": 0,
            "last_decision": None
        }

    def record_request(self, success: bool = True):
        self.metrics["requests_total"] += 1
        if not success:
            self.metrics["errors_total"] += 1

    def record_decision(self, decision: str):
        self.metrics["last_decision"] = decision

    def get_status(self) -> Dict[str, Any]:
        uptime = time.time() - self.start_time
        return {
            "status": "UP",
            "uptime_sec": round(uptime, 2),
            "metrics": self.metrics,
            "timestamp": datetime.utcnow().isoformat()
        }

    def export_metrics(self, path: str = "runtime_data/system_status.json"):
        """Exporta métricas a un archivo para monitoreo externo."""
        try:
            with open(path, "w") as f:
                json.dump(self.get_status(), f, indent=2)
        except Exception as e:
            logger.error(f"Failed to export metrics: {e}")
