"""
Context Coexistence Agent (CCA) - v5.2
Extraído y reforzado desde Brain_Artifacts/CCA_Design_v1.0.md y Protocolo_Streaming_Pulse.md

Rol: Observador clínico pasivo.
No decide. Emite telemetría (semantic_risk, operational_risk, action_verb, intent_shift, etc.)
para que el Regente ajuste el Régimen de Coherencia Contextual (RCC: Θ, λ).

Uso:
    cca = CCA()
    tel = cca.observe(user_input, ai_output)
    regime = cca.to_regime(tel)
    c_total, result = kernel.compute_with_regime(state, regime)
"""
from typing import Dict, Any
import hashlib

class CCA:
    """
    Context Coexistence Agent.
    Implementación alineada con el canon v5.2 del backup.
    """
    def __init__(self, session_id: str = "default"):
        self.session_id = session_id
        self.history = []
        self.last_checkpoint = None

    def observe(self, user_input: str, ai_output: str = "", 
                authority_level: int = 1, project_link: str = None) -> Dict[str, Any]:
        """
        Observa el flujo y genera telemetría.
        Basado en: semantic_risk, operational_risk, action_verb_detected, intent_shift_detected.
        """
        combined = (user_input + " " + ai_output).lower()
        
        action_verbs = ["ejecuta", "borra", "transfiere", "firma", "pago", "desplaza"]
        action_verb_detected = any(v in combined for v in action_verbs)
        
        operational_risk = 0.8 if action_verb_detected or "dinero" in combined or "ip" in combined else 0.3
        semantic_risk = min(1.0, len(combined.split()) / 80.0)
        intent_shift = 0.75 if project_link or "proyecto" in combined else 0.3
        
        telemetry = {
            "trace_id": hashlib.md5(combined.encode()).hexdigest()[:12],
            "session_id": self.session_id,
            "semantic_risk": round(semantic_risk, 3),
            "operational_risk": round(operational_risk, 3),
            "action_verb_detected": action_verb_detected,
            "intent_shift_detected": intent_shift > 0.5,
            "authority_level": authority_level,
            "project_link": project_link,
            "intent_vector": [0.2, round(operational_risk, 2), round(semantic_risk, 2)]
        }
        self.history.append(telemetry)
        return telemetry

    def to_regime(self, telemetry: Dict[str, Any]) -> 'Regime':
        """Mapea telemetría a Régimen (RCC)."""
        from tests.kernel_1240421 import Regime  # import local para evitar ciclos
        
        crit = max(telemetry.get("operational_risk", 0), telemetry.get("semantic_risk", 0))
        irr = 1.0 if telemetry.get("action_verb_detected") else 0.0
        
        theta = 0.25 if crit > 0.7 else 0.35  # ADR-0006: angular scale, critical tightens
        lam = max(0.05, 0.25 - irr * 0.15)
        
        weights = {'w_NR': 0.25, 'w_RI': 0.25, 'w_IF': 0.50}
        if crit > 0.6:
            weights['w_IF'] = 0.60
        
        mode = "B"  # Convivencia
        return Regime(theta=theta, lambda_landauer=lam, weights=weights, 
                      mode=mode, criticality=crit)

    def flash_pulse(self, reason: str = "irreversibility"):
        """Simula Flash Pulse para recalibración inmediata."""
        return {"pulse_type": "FLASH", "reason": reason, "force_recalc": True}