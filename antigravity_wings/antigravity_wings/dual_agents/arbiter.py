"""
Árbitro Dual:
Combina informes de Mario y Luigi en un ConsolidatedReport.
Mantiene trazabilidad de desacuerdo sin mezclar conclusiones.
"""

from antigravity_wings.api.models import (
    TomographyGraph,
    MarioReport,
    LuigiReport,
    ConsolidatedReport,
)


class DualArbiter:
    def consolidate(
        self,
        graph: TomographyGraph,
        mario: MarioReport,
        luigi: LuigiReport
    ) -> ConsolidatedReport:
        """
        Real consolidation logic: combines Mario (strengths) and Luigi (risks)
        without averaging. Produces traceable summary for NRIF translation.
        """
        node_count = len(graph.nodes)
        edge_count = len(graph.edges)
        risk_count = len(luigi.risks)
        strength_count = len(mario.strengths)

        summary = (
            f"Client {graph.client_id}: {node_count} nodes, {edge_count} edges. "
            f"Mario identified {strength_count} strengths and {len(mario.safe_zones)} safe zones. "
            f"Luigi flagged {risk_count} risks and {len(luigi.no_return_points)} no-return points. "
            "Consolidation preserves disagreement for audit."
        )
        references = ["mario_report", "luigi_report", "tomography_graph"]
        return ConsolidatedReport(
            client_id=graph.client_id,
            summary=summary,
            mario=mario,
            luigi=luigi,
            references=references
        )


# ============================================================================
# V7.7 "Fusion" Fases 3-4-5 — Autoridad de escritura, Juez y cola de recalibracion
# ----------------------------------------------------------------------------
# Resolucion de una contradiccion del handoff: Fase 3 pedia "Arbitro = unico
# escritor de FuseSpec" y Fase 4 pedia "Juez = unico escritor de FuseSpec". No
# pueden coexistir dos escritores exclusivos. Se unifican: ArbiterAuthority es el
# UNICO objeto que muta FuseSpec; el Arbitro *consolida* la decision (regla
# conservadora, desacuerdo preservado) y el Juez es la *compuerta de confianza*
# que autoriza (o no) la escritura mediante un token. El Juez emite el token; sin
# token valido, write_fuse() lanza. Asi el invariante "unico escritor" es real.
# ============================================================================

import uuid as _uuid
from dataclasses import dataclass, field as _dc_field
from typing import Optional, Dict, Any, List, Tuple

from antigravity_wings.api.models import RuntimeDecision, FuseSpec

# Orden de severidad de decisiones (NO es el orden del Enum): mas alto = mas
# restrictivo. La regla conservadora toma el maximo, nunca promedia.
_DECISION_RANK: Dict[RuntimeDecision, int] = {
    RuntimeDecision.GO: 0,
    RuntimeDecision.DEGRADE: 1,
    RuntimeDecision.ESCALATE: 2,
    RuntimeDecision.STOP: 3,
}


@dataclass
class DisagreementRecord:
    """Trazabilidad del desacuerdo Mario/Luigi (no se promedia, se registra)."""
    mario: RuntimeDecision
    luigi: RuntimeDecision
    final: RuntimeDecision
    disagreement: bool
    rule: str = "conservative_max"


@dataclass
class JudgeVerdict:
    """Resultado de la evaluacion del Juez sobre una solicitud de recalibracion."""
    authorized: bool
    confidence: float
    threshold: float
    reason: str
    write_token: Optional[str] = None


class ArbiterAuthority:
    """Fase 3 — consolidacion con decision + UNICO escritor de FuseSpec.

    - `arbitrate(mario, luigi)`: aplica la regla conservadora (el mas restrictivo
      gana) y devuelve un DisagreementRecord con el desacuerdo preservado.
    - `write_fuse(...)`: unica via para mutar un FuseSpec. Exige un token emitido
      por el Juez (Fase 4). Sin token valido -> PermissionError.
    """

    def __init__(self) -> None:
        self._valid_tokens: set[str] = set()

    # -- Fase 3: consolidacion conservadora ------------------------------
    @staticmethod
    def arbitrate(mario: RuntimeDecision, luigi: RuntimeDecision) -> DisagreementRecord:
        final = mario if _DECISION_RANK[mario] >= _DECISION_RANK[luigi] else luigi
        return DisagreementRecord(
            mario=mario,
            luigi=luigi,
            final=final,
            disagreement=(mario != luigi),
        )

    # -- Fase 4: registro de tokens emitidos por el Juez -----------------
    def _register_token(self, token: str) -> None:
        self._valid_tokens.add(token)

    # -- Fase 3/4: unica escritura de FuseSpec ---------------------------
    def write_fuse(self, fuse: FuseSpec, new_parameters: Dict[str, Any], token: str) -> FuseSpec:
        """Recalibra un FuseSpec. SOLO ejecuta con token valido del Juez."""
        if token not in self._valid_tokens:
            raise PermissionError(
                "write_fuse requiere un token autorizado por el Juez "
                "(ArbiterAuthority es el unico escritor de FuseSpec)."
            )
        self._valid_tokens.discard(token)  # token de un solo uso
        merged = dict(fuse.parameters)
        merged.update(new_parameters)
        return fuse.model_copy(update={"parameters": merged})


class Judge:
    """Fase 4 — Juez (reescritura de OptionalPSC.apply_mosef).

    RED-TEAM del apply_mosef original (`if gravity>0.8 and not reversibility ->
    BLOCK`):
      1. Devolvia BLOCK duro -> viola "redirigir, nunca cortar". El Juez NO
         bloquea: autoriza o niega una *recalibracion*.
      2. `reversibility` binario y default True -> practicamente nunca disparaba.
      3. Sin umbral de confianza -> recalibraria ante cualquier pico (ruido).
      4. Usaba una heuristica nueva (context['risk']) en vez del acumulador
         termico real de la Fase 1.
    Conclusion: se REESCRIBE, no se extiende. El Juez consume la
    RecalibrationRequest del acumulador termico y exige confianza minima antes
    de emitir un token de escritura.

    Confianza (0..1), compuesta y explicable:
      base   = 0.5 si trip_mode=='accumulation' else 0.4  (sostenido algo mas
               fiable que un pico aislado, sin penalizar el pico catastrofico)
      + 0.3  si Luigi corrobora el riesgo (evidencia independiente)
      + 0.2 * min(1, margen sobre T_trip)                 (cuan lejos del umbral)
    """

    def __init__(self, authority: ArbiterAuthority, confidence_threshold: float = 0.6) -> None:
        self.authority = authority
        self.confidence_threshold = confidence_threshold

    @staticmethod
    def _confidence(request, luigi_corroborates: bool) -> float:
        base = 0.5 if getattr(request, "trip_mode", "") == "accumulation" else 0.4
        corro = 0.3 if luigi_corroborates else 0.0
        t_trip = getattr(request, "T_trip", 1.0) or 1.0
        margin = max(0.0, (getattr(request, "temperature", 0.0) - t_trip) / t_trip)
        over = 0.2 * min(1.0, margin)
        return round(min(1.0, base + corro + over), 6)

    def assess(self, request, luigi_corroborates: bool = False) -> JudgeVerdict:
        """Evalua una RecalibrationRequest. Si confianza>=umbral emite token."""
        conf = self._confidence(request, luigi_corroborates)
        if conf >= self.confidence_threshold:
            token = _uuid.uuid4().hex
            self.authority._register_token(token)
            return JudgeVerdict(
                authorized=True, confidence=conf,
                threshold=self.confidence_threshold,
                reason="confianza suficiente: recalibracion autorizada",
                write_token=token,
            )
        return JudgeVerdict(
            authorized=False, confidence=conf,
            threshold=self.confidence_threshold,
            reason="evidencia insuficiente: no se recalibra (posible ruido)",
            write_token=None,
        )


class RecalibrationQueue:
    """Fase 5 — desacople logico del hot path.

    El hot path (Gate deterministico + acumulador termico) SOLO encola la
    RecalibrationRequest (O(1)) y retorna; no corre Mario/Luigi/Arbitro/Juez en
    linea. Un worker de fondo (semilla v8) llama drain() fuera del hot path.
    No usa hilos ni procesos aqui: prueba el desacople sin arriesgar el hot path
    sincrono actual. La infraestructura async real (cola distribuida / proceso
    separado) queda como decision abierta hacia v8.
    """

    def __init__(self) -> None:
        self._pending: List[Any] = []

    def enqueue(self, request) -> None:
        self._pending.append(request)          # O(1), no ejecuta arbitraje

    def __len__(self) -> int:
        return len(self._pending)

    def drain(self, handler) -> List[Any]:
        """Procesa fuera del hot path. `handler(request)->result`."""
        results = [handler(r) for r in self._pending]
        self._pending.clear()
        return results
