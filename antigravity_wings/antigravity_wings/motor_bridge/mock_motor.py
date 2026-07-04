"""
Motor MOCK para pruebas de la tubería.
No representa lógica real.
"""

from typing import Dict, Any
from antigravity_wings.api.models import NumericEvidence, MotorOutput
from antigravity_wings.motor_bridge.interface import MotorInterface


class MockMotor(MotorInterface):
    def evaluate(self, evidence: NumericEvidence) -> MotorOutput:
        # Mock de cálculo basado en la suma de NRIF
        score = (sum(evidence.normative) + sum(evidence.representational)) / 10.0
        return MotorOutput(
            client_id=evidence.client_id,
            scores={"global": min(score, 1.0), "mock": 1.0},
            ranges={"min": 0, "max": 1, "status": "simulated"},
            config_blob={"engine": self.version}
        )

    def get_capabilities(self) -> Dict[str, Any]:
        return {"modes": ["shadow", "soft", "hard"], "features": ["coherence", "entropy"]}

    @property
    def version(self) -> str:
        return "1.0.0-mock"
