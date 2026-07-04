import httpx
import logging
from typing import Dict, Any
from antigravity_wings.motor_bridge.interface import MotorInterface
from antigravity_wings.api.models import NumericEvidence, MotorOutput
from antigravity_wings.resilience.circuit_breaker import CircuitBreaker

logger = logging.getLogger(__name__)

class RealMotor(MotorInterface):
    """
    Cliente oficial para el Motor 4R2 (Kernel 1240421).
    Se conecta vía HTTP al backend de Redbull Wings.
    """
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip("/")
        self._version = "4R2-Master-1240421"
        self.cb = CircuitBreaker("real_motor_http")  # Hardened CB for HTTP path

    @property
    def version(self) -> str:
        return self._version

    def get_capabilities(self) -> Dict[str, Any]:
        return {
            "modes": ["http"],
            "features": ["coherence", "landauer"],
            "endpoint": self.base_url
        }

    def evaluate(self, evidence: NumericEvidence) -> MotorOutput:
        payload = {
            "normative": evidence.normative,
            "representational": evidence.representational,
            "informational": evidence.informational,
            "physical": evidence.physical
        }
        
        regime_dict = evidence.metadata.get("regime") if evidence.metadata else None
        if regime_dict:
            payload["regime"] = regime_dict
            
        url = f"{self.base_url}/api/coherence/measure"
        
        def _http_call():
            try:
                logger.info(f"Calling Real Motor 4R2 at {url}", extra={"url": url, "client_id": evidence.client_id})
                with httpx.Client(timeout=10.0) as client:
                    response = client.post(
                        url, 
                        json=payload,
                        headers={"Authorization": "Bearer real-test-token"}
                    )
                    response.raise_for_status()
                    data = response.json()
                    
                    scores = {
                        "global": data.get("C_total", 0.0),
                        "C_NR": data.get("C_NR", 0.0),
                        "C_RI": data.get("C_RI", 0.0),
                        "C_IF": data.get("C_IF", 0.0)
                    }
                    
                    if "passes_gate" in data and data["passes_gate"] is not None:
                        scores["passes_gate"] = float(1.0 if data["passes_gate"] else 0.0)
                    if "adjusted_landauer" in data and data["adjusted_landauer"] is not None:
                        scores["adjusted_landauer"] = float(data["adjusted_landauer"])
                    if "cca_influence" in data and data["cca_influence"] is not None:
                        scores["cca_influence"] = float(data["cca_influence"])
                        
                    # Mapeo de la respuesta real del motor 4R2 al modelo de Antigravity
                    return MotorOutput(
                        client_id=evidence.client_id,
                        scores=scores,
                        ranges=data.get("ranges", {}), 
                        config_blob={
                            "engine": self.version,
                            "raw_response": data,
                            "passes_gate": data.get("passes_gate")
                        }
                    )
            except Exception as e:
                logger.error(f"Failed to evaluate evidence with Real Motor: {e}", extra={"url": url, "client_id": evidence.client_id, "error": str(e)})
                raise RuntimeError(f"Real Motor Unreachable: {e}")

        # Wrapped with CB for production hardening
        return self.cb.call(_http_call)
