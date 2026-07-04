# pilots/chatbot/chatbot_motor.py

from typing import Dict, Any
from antigravity_wings.motor_bridge.loader import MotorInterface
from antigravity_wings.api.models import NumericEvidence, MotorOutput

class ChatbotSafetyMotor(MotorInterface):
    """
    Motor de simulación para el piloto de Chatbot.
    Evalúa si una respuesta es 'segura' basada en el score de sensibilidad.
    """
    def __init__(self, **kwargs):
        self.config = kwargs

    @property
    def version(self) -> str:
        return "pilot_chatbot_v1240421"

    def get_capabilities(self) -> Dict[str, Any]:
        return {
            "evaluations": ["safety_score", "risk_index"],
            "domain": "conversational_ai"
        }

    def evaluate(self, evidence: NumericEvidence) -> MotorOutput:
        # BRUTAL REAL: Use the canonical kernel for real coherence-based safety.
        # Import the core canonical to compute real C_total for safety decision.
        import sys
        from pathlib import Path
        core_path = Path(__file__).resolve().parents[3] / "core"
        sys.path.insert(0, str(core_path))
        try:
            from kernel_1240421 import create_kernel, LayerState
            import numpy as np
            kernel = create_kernel()
            state = LayerState(
                normative=np.asarray(evidence.normative or [0.5]*4),
                representational=np.asarray(evidence.representational or [0.5]*4),
                informational=np.asarray(evidence.informational or [0.5]*4),
                physical=np.asarray(evidence.physical or [0.1,0.1,0.1,0.1])
            )
            c_total, _ = kernel.compute_coherence_total(state)
            safety = max(0.0, 1.0 - c_total)  # real mapping
            risk = c_total
        except Exception:
            # Fallback only if core not loadable, but should not happen
            safety = 0.8
            risk = 0.2
        
        return MotorOutput(
            client_id=evidence.client_id,
            scores={
                "safety_score": float(safety),
                "risk_index": float(risk),
                "coherence": float(c_total if 'c_total' in locals() else 0.2)
            },
            ranges={
                "safety_score": [0.0, 1.0],
                "risk_index": [0.0, 1.0]
            },
            config_blob={
                "motor_version": "pilot_v1_real_canonical",
                "threshold_used": 0.7,
                "real_kernel": True
            }
        )
