import logging
import uuid
from typing import Dict, Any
import numpy as np
from datetime import datetime
from antigravity_wings.api.models import (
    RuntimeDecisionResponse,
    RuntimeDecision,
    ReasonDetail,
    MotorOutput,
    RuntimeDecisionRequest,
    NotebookSummary
)
from antigravity_wings.observation.registry import SourceRegistry
from antigravity_wings.observation.observer import SystemObserver, ObservationConfig
from antigravity_wings.tomography.builder import TomographyBuilder
from antigravity_wings.dual_agents.mario import MarioAgent
from antigravity_wings.dual_agents.luigi import LuigiAgent
from antigravity_wings.dual_agents.arbiter import DualArbiter
from antigravity_wings.notebook_bridge.client import NotebookClient
from antigravity_wings.numeric.translator import NumericTranslator
# MockMotor import removed from production path. Only real components used.
from antigravity_wings.resilience.circuit_breaker import CircuitBreaker
from antigravity_wings.fuse_config.generator import FuseConfigGenerator
from antigravity_wings.profiles.client_profile import ClientProfile
from antigravity_wings.operators.dual_runtime import DualRuntimeOperator

logger = logging.getLogger(__name__)

class MasterOrchestrator:
    def __init__(
        self, 
        use_real_motor: bool = True,   # BRUTAL: default to 100% real, no mocks
        motor_url: str = "http://localhost:8000",
        use_real_llm: bool = False,
        force_http_real: bool = False  # For full stack validation: force RealMotor over LocalCanonical
    ):
        self.fuse_generator = FuseConfigGenerator()
        self.registry = SourceRegistry()
        self.observer = SystemObserver("default", ObservationConfig(), self.registry)
        self.tomo_builder = TomographyBuilder()
        self.mario = MarioAgent()
        self.luigi = LuigiAgent()
        self.arbiter = DualArbiter()
        self.notebook = NotebookClient(
            notebook_id="default_nb", 
            use_real_llm=use_real_llm
        )
        self.translator = NumericTranslator()
        
        # Initialize CCA observer
        try:
            import sys
            from pathlib import Path
            core_path = Path(__file__).resolve().parents[3] / "core"
            if str(core_path) not in sys.path:
                sys.path.insert(0, str(core_path))
            from kernel_1240421 import CCA
            self.cca = CCA()
        except Exception as e:
            self.cca = None
            logger.warning(f"Failed to load CCA in MasterOrchestrator: {e}")
        
        # BRUTAL MODE: Default to 100% real. Local canonical preferred unless force_http_real.
        # This allows full stack validation with the real 4R2 HTTP motor service.
        if use_real_motor:
            if force_http_real:
                from antigravity_wings.motor_bridge.real_motor import RealMotor
                self.motor = RealMotor(base_url=motor_url)
                print("[INFO] Forcing RealMotor (HTTP) for full stack validation")
            else:
                try:
                    # Use canonical kernel directly - 100% real
                    import sys
                    from pathlib import Path
                    core_path = Path(__file__).resolve().parents[3] / "core"
                    sys.path.insert(0, str(core_path))
                    from kernel_1240421 import create_kernel, LayerState, Regime

                    class LocalCanonicalMotor:
                        """100% real wrapper using the canonical kernel directly."""
                        def __init__(self):
                            self._kernel = create_kernel()
                            self.version = "canonical-5.2-local-real"

                        def evaluate(self, evidence):
                            state = LayerState(
                                normative=np.asarray(evidence.normative),
                                representational=np.asarray(evidence.representational),
                                informational=np.asarray(evidence.informational),
                                physical=np.asarray(evidence.physical)
                            )
                            
                            regime_dict = evidence.metadata.get("regime") if evidence.metadata else None
                            if regime_dict:
                                regime = Regime(
                                    theta=regime_dict.get("theta", 0.35),  # ADR-0006 angular scale
                                    lambda_landauer=regime_dict.get("lambda_landauer", 0.05),
                                    mode=regime_dict.get("mode", "B"),
                                    criticality=regime_dict.get("criticality", 0.0),
                                    intent_level=regime_dict.get("intent_level", "EXPLORATORY")
                                )
                                C_total, result = self._kernel.compute_with_regime(state, regime)
                                breakdown = result.get("breakdown", {})
                                passes_gate = result.get("passes_gate", True)
                                adjusted_landauer = result.get("adjusted_landauer", 0.0)
                                cca_influence = result.get("cca_influence", 0.0)
                            else:
                                C_total, breakdown = self._kernel.compute_coherence_total(state)
                                passes_gate = C_total <= 0.5  # default gate threshold
                                adjusted_landauer = self._kernel.compute_landauer_cost(1)
                                cca_influence = 0.0

                            return MotorOutput(
                                client_id=evidence.client_id,
                                scores={
                                    "global": float(C_total),
                                    "C_NR": float(breakdown.get("C_NR", 0)),
                                    "C_RI": float(breakdown.get("C_RI", 0)),
                                    "C_IF": float(breakdown.get("C_IF", 0)),
                                    "passes_gate": float(1.0 if passes_gate else 0.0),
                                    "adjusted_landauer": float(adjusted_landauer),
                                    "cca_influence": float(cca_influence)
                                },
                                config_blob={
                                    "engine": self.version,
                                    "weights": {k: float(v) for k, v in breakdown.get("weights", {}).items()} if isinstance(breakdown.get("weights"), dict) else {},
                                    "path": "direct-canonical-no-mock",
                                    "passes_gate": bool(passes_gate),
                                    "active_domain_weights": {k: float(v) for k, v in self._kernel.domain_weights.items()} if hasattr(self._kernel, 'domain_weights') else {"w_NR": 1/21, "w_RI": 4/21, "w_IF": 16/21}
                                }
                            )

                    self.motor = LocalCanonicalMotor()
                except Exception as e:
                    from antigravity_wings.motor_bridge.real_motor import RealMotor
                    self.motor = RealMotor(base_url=motor_url)
                    print(f"[INFO] Local canonical failed, using real HTTP motor: {e}")
        else:
            from antigravity_wings.motor_bridge.real_motor import RealMotor
            self.motor = RealMotor(base_url=motor_url)
            
        self.cb = CircuitBreaker("motor_analysis")

    def execute_full_analysis(self, client_id: str, metadata: Dict[str, Any]) -> RuntimeDecisionResponse:
        trace_id = str(uuid.uuid4())
        logger.info(f"Starting full analysis cycle for {client_id} (Trace: {trace_id})", extra={"client_id": client_id, "trace_id": trace_id, "stage": "start"})
        
        try:
            # 1. Observación
            snapshot = self.observer.build_snapshot()
            snapshot.client_id = client_id
            
            # 2. Tomografía
            graph = self.tomo_builder.build(snapshot)
            
            # 3. Agentes Duales
            mario_rep = self.mario.analyze(graph)
            luigi_rep = self.luigi.analyze(graph)
            consolidated = self.arbiter.consolidate(graph, mario_rep, luigi_rep)
            
            # 4. Notebook context (Real o Mock según config)
            summary = self.notebook.summarize(consolidated)
            
            # 5. Traducción Numérica
            evidence = self.translator.to_evidence(consolidated, summary)
            
            # Inferencia del PSC/Regime usando CCA
            regime_dict = None
            if self.cca:
                # Observe input context
                input_text = metadata.get("input_text", f"Client analysis cycle for {client_id}")
                output_text = summary.condensed_summary if summary else ""
                telemetry = self.cca.observe(input_text, output_text)
                regime = self.cca.to_regime(telemetry)
                # Save regime to dict representation
                regime_dict = {
                    "theta": float(regime.theta),
                    "lambda_landauer": float(regime.lambda_landauer),
                    "mode": str(regime.mode),
                    "criticality": float(regime.criticality),
                    "intent_level": str(regime.intent_level)
                }
                # Attach to evidence metadata
                if not evidence.metadata:
                    evidence.metadata = {}
                evidence.metadata["regime"] = regime_dict
            
            # 6. Motor (Protegido por CB)
            motor_out = self.cb.call(self.motor.evaluate, evidence)
            
            # 7. Generación Dinámica de Fusibles y Evaluación con Operador Dual
            target_node = metadata.get("node_id", "decision_1")
            specs = self.fuse_generator.generate(motor_out, node_id=target_node)
            
            profile = ClientProfile(
                client_id=client_id,
                profile_version="1.0",
                created_at=datetime.utcnow(),
                tomography=graph,
                light_report=mario_rep,
                shadow_report=luigi_rep,
                consolidated_summary=summary.condensed_summary if summary else "",
                notebook_summary=summary if summary else NotebookSummary(client_id=client_id, condensed_summary="", key_points=[], source_refs=[]),
                numeric_evidence=evidence,
                motor_output=motor_out,
                fuse_specs=specs
            )
            
            operator = DualRuntimeOperator(profile=profile)
            
            req = RuntimeDecisionRequest(
                trace_id=trace_id,
                client_id=client_id,
                node_id=target_node,
                mode=metadata.get("mode", "shadow"),
                payload=metadata.get("payload", {}),
                context=metadata.get("context", {})
            )
            
            op_res = operator.evaluate(req)
            
            logger.info(
                f"Analysis complete for {client_id}. Decision: {op_res.decision.value}", 
                extra={
                    "client_id": client_id, 
                    "trace_id": trace_id, 
                    "stage": "complete", 
                    "decision": op_res.decision.value, 
                    "global_score": motor_out.scores.get("global", 0)
                }
            )
            
            return RuntimeDecisionResponse(
                trace_id=trace_id,
                client_id=client_id,
                node_id=target_node,
                decision=op_res.decision,
                reasons=op_res.reasons if op_res.reasons else [ReasonDetail(
                    fuse_id="master_fuse", 
                    node_id=target_node, 
                    severity="low", 
                    rule_type="coherence", 
                    message=f"Consolidated score: {motor_out.scores.get('global')}. Evaluated dynamically."
                )],
                scores=motor_out.scores,
                state_color=op_res.state_color,
                cost_level=op_res.cost_level,
                mario_decision=op_res.mario_decision,
                luigi_decision=op_res.luigi_decision,
                meta={
                    "meta_version": "1.0",
                    "engine": self.motor.version, 
                    "state": "audit-grade",
                    "regime": regime_dict,
                    "operator_meta": op_res.meta
                }
            )
            
        except Exception as e:
            logger.error(f"Orchestration failure: {e}")
            return RuntimeDecisionResponse(
                trace_id=trace_id,
                client_id=client_id,
                node_id="system",
                decision=RuntimeDecision.STOP,
                reasons=[ReasonDetail(
                    fuse_id="emergency_stop",
                    node_id="system",
                    severity="critical",
                    rule_type="failure",
                    message=f"System error: {str(e)}"
                )],
                meta={"error": True, "fallback": True}
            )

# Optional PSC/MOSEF/CCA layer (from backup42final v5.2 high-value).
# This adds "dynamic coexistence" on top of immutable kernel (no math change).
# Use in __init__ or evaluate for LLM/agent mode (B from v5.2).
# PSC: inferred context for dynamic fuses.
# MOSEF: enforcement (ties to our 4R2_FUSES).
# CCA: observer (e.g., log C_total per cycle).

class OptionalPSC:
    """Lightweight PSC layer (optional, for dynamic mode)."""
    def __init__(self, mode="B"):  # A static, B dynamic
        self.mode = mode
        self.psc = {"identity": "default", "intention": "project", "gravity": 0.5, "reversibility": True}

    def infer_psc(self, context):
        # Simple inference; in full, CCA would do this continuously.
        self.psc["gravity"] = context.get("risk", 0.5)
        return self.psc

    def apply_mosef(self, decision, psc):
        """V7.7 Fase 4 — REESCRITO. El apply_mosef original hacia:
            if gravity>0.8 and not reversibility: return "BLOCK"
        Red-team de esa version (ver docstring de Judge en dual_agents.arbiter):
          - BLOCK duro viola "redirigir, nunca cortar".
          - `reversibility` binario y default True -> casi nunca disparaba.
          - Sin umbral de confianza -> recalibraria por ruido.
          - Usaba una heuristica (context['risk']) en vez del acumulador termico.
        Ahora NO bloquea: delega en el Juez, que exige confianza minima y consume
        la RecalibrationRequest del acumulador termico (Fase 1). Devuelve un
        JudgeVerdict; la escritura real de FuseSpec solo ocurre via
        ArbiterAuthority.write_fuse con el token del veredicto.
        """
        from antigravity_wings.dual_agents.arbiter import ArbiterAuthority, Judge
        authority = ArbiterAuthority()
        judge = Judge(authority)
        # `decision` puede portar una RecalibrationRequest (thermal) en .context
        # o el llamador pasarla directamente; se acepta el objeto request tal cual.
        request = psc.get("recal_request") if isinstance(psc, dict) else None
        if request is None:
            # Sin senal termica no hay recalibracion (fail-safe: no ruido).
            return {"authorized": False, "reason": "sin RecalibrationRequest termica"}
        verdict = judge.assess(request, luigi_corroborates=bool(psc.get("luigi_corroborates", False)))
        return verdict
        return decision
