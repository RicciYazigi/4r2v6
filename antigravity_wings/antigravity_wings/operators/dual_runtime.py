"""
Operador Dual en caliente (MARIO / LUIGI).

- Carga un ClientProfile.
- Extrae los FuseSpec para un nodo.
- Evalúa fusibles sobre el payload real de la decisión.
- Mario y Luigi opinan sobre el resultado (LUZ y SOMBRA).
- Árbitro toma decisión final GO/DEGRADE/STOP/ESCALATE.
"""

from datetime import datetime
from typing import List, Tuple, Optional
from antigravity_wings.api.models import (
    RuntimeDecisionRequest,
    RuntimeDecisionResponse,
    RuntimeDecision,
    ReasonDetail,
    FuseSpec,
)
from antigravity_wings.profiles.client_profile import ClientProfile

# Integration of concrete 4R2_FUSES guards (ported from SUPERAGENTTESTPILOT pilots for high-value asymmetry/priority/verification breaking)
try:
    from antigravity_wings.fuses.fuses_4r2 import get_fuse
    HAS_4R2_GUARDS = True
except ImportError:
    HAS_4R2_GUARDS = False


class DualRuntimeOperator:
    """
    Operador Dual por cliente.

    El comportamiento por defecto es genérico:
    - Interpreta fusibles de tipo "threshold" con parámetros:
      - field (str)
      - threshold (float)
    - Si payload[field] > threshold:
      - Si severity == "high" → FAIL
      - Si severity == "medium" → WARN
    - Mario (Luz) tiende a GO/DEGRADE.
    - Luigi (Shadow) tiende a GO/ESCALATE/STOP según riesgo.
    """

    def __init__(self, profile: ClientProfile):
        self.profile = profile

    # ─────────────────────────────────────────────
    # ENTRYPOINT PRINCIPAL
    # ─────────────────────────────────────────────

    def evaluate(self, req: RuntimeDecisionRequest) -> RuntimeDecisionResponse:
        t_start = datetime.utcnow()
        # Cliente equivocado → STOP inmediato (Protocolo de seguridad)
        if req.client_id != self.profile.client_id:
            return RuntimeDecisionResponse(
                trace_id=req.trace_id or "ERR_AUTH",
                decision=RuntimeDecision.STOP,
                reasons=[ReasonDetail(
                    fuse_id="system_auth",
                    node_id=req.node_id,
                    severity="critical",
                    rule_type="custom",
                    message=f"client_mismatch: expected={self.profile.client_id}"
                )],
                client_id=req.client_id or "unknown",
                node_id=req.node_id,
                state_color="red",
                cost_level="high",
                meta={"fallback_used": False, "mode": req.mode}
            )

        # 1) Fusibles relevantes
        node_fuses = self._get_fuses_for_node(req.node_id)

        # 2) Evaluar fusibles
        reasons = self._evaluate_fuses(node_fuses, req.payload, req.context, req.mode)

        # 3) Aplicar Política de Enforcement Canónica (Tabla de Severidad)
        final_decision = self._apply_enforcement_policy(reasons, req.mode)

        latency = (datetime.utcnow() - t_start).total_seconds() * 1000

        # Mapear colores y costos para el cockpit
        state_color, cost_level = self._get_visual_metadata(final_decision)

        return RuntimeDecisionResponse(
            trace_id=req.trace_id or "ND",
            decision=final_decision,
            reasons=reasons,
            scores={
                "risk_score": self._calculate_risk_score(reasons),
                "coherence_total": self._get_coherence_score(),
                "entropy_loss": self._get_entropy_loss()
            },
            meta={
                "engine_version": "1240421",
                "profile_version": self.profile.profile_version,
                "mode": req.mode,
                "latency_ms": latency,
                "fallback_used": False,
                "evidence_ref": f"sessions/{req.client_id}/{req.trace_id}"
            },
            client_id=req.client_id,
            node_id=req.node_id,
            state_color=state_color,
            cost_level=cost_level,
            mario_decision=final_decision, # En este modelo simplificado, el árbitro es directo
            luigi_decision=final_decision
        )

    # ─────────────────────────────────────────────
    # FUSIBLES
    # ─────────────────────────────────────────────

    def _get_fuses_for_node(self, node_id: str) -> List[FuseSpec]:
        return [f for f in self.profile.fuse_specs if f.node_id == node_id and f.enabled]

    def _evaluate_fuses(
        self,
        fuses: List[FuseSpec],
        payload,
        context,
        mode: str
    ) -> List[ReasonDetail]:
        reasons: List[ReasonDetail] = []

        for f in fuses:
            # Verificar si el fusible aplica al modo actual
            if mode not in f.mode_scope:
                continue

            handled = False
            # Support for concrete 4R2_FUSES guards (high-value from pilots: asymmetry, priority, verification breaking, hermetics)
            if HAS_4R2_GUARDS:
                try:
                    f_type_upper = f.type.upper()
                    from antigravity_wings.fuses.fuses_4r2 import FUSE_REGISTRY
                    # Check if the type exists in FUSE_REGISTRY or matches a concrete registered fuse type/name
                    if f_type_upper in FUSE_REGISTRY or any(f_type_upper == inst.name.upper() or f_type_upper == inst.type.upper() for inst in [v() for v in FUSE_REGISTRY.values()]):
                        guard = get_fuse(f.type)
                        res = None
                        evidence = {}
                        msg = "Guard vetoed decision"
                        rule = "4r2_guard"
                        
                        if f_type_upper in ["VER", "VERIFICATIONGUARD"]:
                            # 1. Recuperar el score de coherencia calculado en el servidor
                            val = self.profile.motor_output.scores.get("coherence_score")
                            
                            # Fallback si no está precalculado (convertir la distancia C_total a score de calidad)
                            if val is None:
                                global_distance = self.profile.motor_output.scores.get("global")
                                if global_distance is not None:
                                    val = 1.0 - float(global_distance)
                            
                            # 2. FAIL-CLOSED: Si no se puede validar en el servidor, se bloquea por defecto
                            if val is None:
                                res = "BLOCK"
                                evidence = {"error": "Server-side coherence score missing. Fail-closed triggered."}
                                msg = "VerificationGuard: Blocked due to missing server-side coherence metric"
                            else:
                                # 3. Evaluación real contra el umbral 0.9 del servidor
                                val = float(val)
                                high = f.severity.lower() in ["high", "critical"]
                                res = guard.execute(val, high)
                                evidence = {"server_val": val, "high": high}
                                msg = "VerificationGuard blocked low server-side coherence"
                            
                            rule = "4r2_verification"
                            
                        elif f_type_upper in ["PRIO", "PRIORITYBREAKER"]:
                            rk = float(payload.get("rank", payload.get("priority", 0)))
                            max_rk = float(f.parameters.get("max_rank", 100))
                            res = guard.execute(rk, max_rk)
                            evidence = {"rank": rk, "max": max_rk}
                            msg = "PriorityBreaker vetoed high rank"
                            rule = "4r2_priority"
                            
                        elif f_type_upper in ["ASYM", "ASYMMETRYBREAKER"]:
                            risk = payload.get("risk", "NONE")
                            act = payload.get("action", "NONE")
                            res = guard.execute(risk, act)
                            evidence = {"risk": risk, "action": act}
                            msg = "AsymmetryBreaker vetoed EXISTENTIAL+PASSIVE"
                            rule = "4r2_asymmetry"
                            
                        elif f_type_upper in ["HERMETIC", "HERMETIC_CAUSA", "HERMETICCAUSAEFECTO"]:
                            cause_c = float(payload.get("cause_consistency", 1.0))
                            effect_c = float(payload.get("effect_consistency", payload.get("coherence", 1.0)))
                            theta_kill = float(f.parameters.get("theta_kill", 0.8))
                            res = guard.execute(cause_c, effect_c, theta_kill)
                            evidence = {"cause_consistency": cause_c, "effect_consistency": effect_c, "theta_kill": theta_kill}
                            msg = f"HermeticCausaEfecto vetoed due to low consistency (< {theta_kill})"
                            rule = "hermetic_cause_effect"

                        elif f_type_upper in ["RED_CRITICAL", "REDZONE"]:
                            val = self.profile.motor_output.scores.get("global", 0.8)
                            res = guard.execute(val)
                            evidence = {"global_score": val}
                            msg = f"RedZoneCritical: Critical coherence degradation ({val:.4f})"
                            rule = "4r2_red_critical"
                            
                        elif f_type_upper in ["GRAY_WARNING", "GRAYZONE"]:
                            val = self.profile.motor_output.scores.get("global", 0.5)
                            res = guard.execute(val)
                            evidence = {"global_score": val}
                            msg = f"GrayZoneWarning: Moderate risk of drift / uncertainty zone ({val:.4f})"
                            rule = "4r2_gray_warning"
                            
                        elif f_type_upper in ["CTX", "CONTEXTGUARD"]:
                            res = guard.execute(context, payload.get("decision", "GO"))
                            evidence = {"context": str(context), "decision": payload.get("decision", "GO")}
                            msg = "ContextGuard check executed"
                            rule = "4r2_context"
                            
                        elif f_type_upper in ["TEMP", "TEMPORALGUARD"]:
                            ta = float(payload.get("time_to_action", payload.get("ta", 0.0)))
                            tl = float(f.parameters.get("time_limit", payload.get("tl", 10.0)))
                            res = guard.execute(ta, tl)
                            evidence = {"ta": ta, "tl": tl}
                            msg = "TemporalGuard check executed"
                            rule = "4r2_temporal"
                            
                        elif f_type_upper in ["PHYS", "PHYSICALGUARD"]:
                            res = guard.execute(context, payload.get("decision", "GO"))
                            evidence = {"context": str(context), "decision": payload.get("decision", "GO")}
                            msg = "PhysicalGuard check executed"
                            rule = "4r2_physical"
                        
                        if res in ["VETO", "BLOCK"]:
                            reasons.append(ReasonDetail(
                                fuse_id=f.id,
                                node_id=f.node_id,
                                severity=f.severity,
                                rule_type=rule,
                                message=msg,
                                evidence=evidence
                            ))
                        handled = True
                except Exception as e:
                    # Fallback if guard fails
                    pass

            if not handled:
                if f.type == "threshold":
                    res = self._eval_threshold_fuse(f, payload)
                elif f.type == "range":
                    res = self._eval_range_fuse(f, payload)
                else:
                    raise ValueError(
                        f"CRITICAL CONTRACT BREAK: Unknown/unsupported fuse type '{f.type}' "
                        f"on node '{f.node_id}'. Fail-closed triggered."
                    )
                
                if res:
                    reasons.append(res)

        return reasons

    def _eval_threshold_fuse(self, fuse: FuseSpec, payload) -> Optional[ReasonDetail]:
        field = fuse.parameters.get("field")
        threshold = fuse.parameters.get("threshold")
        value = payload.get(field)

        if field is None or threshold is None or not isinstance(value, (int, float)):
            return None # O loguear error interno

        if value > threshold:
            return ReasonDetail(
                fuse_id=fuse.id,
                node_id=fuse.node_id,
                severity=fuse.severity,
                rule_type="threshold",
                message=f"{field}={value} > threshold={threshold}",
                evidence={"field": field, "value": value, "threshold": threshold}
            )
        return None

    def _eval_range_fuse(self, fuse: FuseSpec, payload) -> Optional[ReasonDetail]:
        field = fuse.parameters.get("field")
        min_v = fuse.parameters.get("min")
        max_v = fuse.parameters.get("max")
        value = payload.get(field)

        if field is None or not isinstance(value, (int, float)):
            return None

        out_of_range = False
        if min_v is not None and value < min_v:
            out_of_range = True
        if max_v is not None and value > max_v:
            out_of_range = True

        if out_of_range:
            return ReasonDetail(
                fuse_id=fuse.id,
                node_id=fuse.node_id,
                severity=fuse.severity,
                rule_type="range",
                message=f"{field}={value} fuera de rango [{min_v}, {max_v}]",
                evidence={"field": field, "value": value, "min": min_v, "max": max_v}
            )
        return None

    # ─────────────────────────────────────────────
    # POLÍTICA DE ENFORCEMENT CANÓNICA
    # ─────────────────────────────────────────────

    def _apply_enforcement_policy(self, reasons: List[ReasonDetail], mode: str) -> RuntimeDecision:
        if mode == "shadow":
            return RuntimeDecision.GO

        severities = [r.severity for r in reasons]
        if not severities:
            return RuntimeDecision.GO

        # Tabla de Enforcement Canónica
        if "critical" in severities:
            return RuntimeDecision.STOP # En SOFT y HARD
        
        if "high" in severities:
            return RuntimeDecision.STOP if mode == "hard" else RuntimeDecision.ESCALATE
        
        if "medium" in severities:
            return RuntimeDecision.ESCALATE if mode == "hard" else RuntimeDecision.DEGRADE
        
        # Low severity
        return RuntimeDecision.GO

    def _get_visual_metadata(self, decision: RuntimeDecision) -> Tuple[str, str]:
        if decision == RuntimeDecision.STOP:
            return "red", "high"
        if decision == RuntimeDecision.GO:
            return "green", "low"
        return "yellow", "medium"

    def _calculate_risk_score(self, reasons: List[ReasonDetail]) -> float:
        if not reasons:
            return 0.0
        weights = {"low": 0.1, "medium": 0.3, "high": 0.7, "critical": 1.0}
        score = sum(weights.get(r.severity, 0.1) for r in reasons)
        return min(1.0, score)

    def _get_coherence_score(self) -> float:
        # Extraer del motor si está disponible
        return self.profile.motor_output.scores.get("global", 1.0)

    def _get_entropy_loss(self) -> float:
        return self.profile.motor_output.config_blob.get("entropy_loss", 0.0)
