"""
Genera FuseSpec a partir de la salida del Motor.

Política por defecto (genérica, pública):

- Crea un fusible de tipo "threshold" para el nodo crítico "decision_1".
- Usa el score global del motor como threshold genérico.
- Asume por defecto que ese threshold se aplica sobre el campo "amount"
  del payload (si existe); si no existe, el fusible queda como metadata.
"""

from typing import List
from antigravity_wings.api.models import MotorOutput, FuseSpec


class FuseConfigGenerator:
    def generate(self, motor_output: MotorOutput, node_id: str = "decision_1") -> List[FuseSpec]:
        specs: List[FuseSpec] = []

        global_score = motor_output.scores.get("global", 0.5)

        # Determinar severidad y fusibles específicos por banda de coherencia
        if global_score < 0.35:
            # ZONA VERDE: Alta confianza (C_total < 0.35)
            severity = "medium"
            # Se genera el fusible estricto VerificationGuard (VER)
            specs.append(FuseSpec(
                id="fuse_4r2_ver",
                node_id=node_id,
                type="VER",
                parameters={
                    "threshold": 0.9,
                    "field": "coherence",
                    "description": "4R2 VerificationGuard: block if val<0.9 on high"
                },
                severity="high"
            ))
        elif 0.28 <= global_score <= 0.39:
            # ZONA GRIS (escala angular ADR-0006): 0.28 <= C_total <= 0.39
            # (equivalente a 0.35-0.65 en la escala 1-cos anterior:
            #  d_new = arccos(1 - d_old) / pi)
            severity = "medium"
            specs.append(FuseSpec(
                id="fuse_4r2_gray_warning",
                node_id=node_id,
                type="GRAY_WARNING",
                parameters={
                    "description": "4R2 Gray Zone Warning: moderate risk of drift / uncertainty zone."
                },
                severity="medium"
            ))
        else:
            # ZONA ROJA (escala angular ADR-0006): C_total > 0.39
            severity = "critical" if global_score > 0.55 else "high"
            specs.append(FuseSpec(
                id="fuse_4r2_red_critical",
                node_id=node_id,
                type="RED_CRITICAL",
                parameters={
                    "description": f"4R2 Red Zone Critical: critical coherence degradation ({global_score:.4f})"
                },
                severity=severity
            ))

        # Add AsymmetryBreaker for risk contexts (pilot example, required for verify_pilot.py)
        specs.append(FuseSpec(
            id="fuse_4r2_asym",
            node_id=node_id,
            type="ASYM",
            parameters={
                "risk_field": "risk",
                "action_field": "action",
                "description": "4R2 AsymmetryBreaker: veto EXISTENTIAL+PASSIVE"
            },
            severity=severity
        ))

        # PriorityBreaker example
        specs.append(FuseSpec(
            id="fuse_4r2_prio",
            node_id=node_id,
            type="PRIO",
            parameters={
                "max_rank": 100,
                "description": "4R2 PriorityBreaker: veto high rank"
            },
            severity=severity
        ))

        # Generic threshold fallback (original)
        specs.append(FuseSpec(
            id="fuse_decision_1_threshold",
            node_id=node_id,
            type="threshold",
            parameters={
                "field": "amount",
                "threshold": global_score,
                "description": (
                    "Generic threshold fuse based on global score. "
                    "If payload['amount'] > threshold → warn/fail según severidad."
                )
            },
            severity=severity
        ))

        return specs
