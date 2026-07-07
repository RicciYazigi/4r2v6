"""
Gate B — V7.7 Fusion Fase 2: vector de reroute.

Escenario guardia-perro-ambulancia: un evento con necesidad innegociable
(la ambulancia DEBE pasar) contra un camino bloqueado (un fusible critico que
en modo hard dispara STOP). Con una ruta de reroute registrada para el nodo,
la respuesta debe traer >=1 reroute_option en vez de STOP puro; sin ruta
registrada, STOP se mantiene (fail-closed).

Sin dependencias del kernel sellado.
"""
from datetime import datetime

from antigravity_wings.operators.dual_runtime import DualRuntimeOperator
from antigravity_wings.profiles.client_profile import ClientProfile
from antigravity_wings.api.models import (
    TomographyGraph, TomographyNode, TomographyEdge,
    MarioReport, LuigiReport, NotebookSummary, NumericEvidence, MotorOutput,
    RuntimeDecisionRequest, RuntimeDecision, RerouteOption, FuseSpec, NodeType,
)

NODE = "ambulance_gate"


def _profile_with_blocking_fuse():
    """Perfil minimo con un fusible threshold critico sobre NODE."""
    node = TomographyNode(id=NODE, label="Ambulance Gate", node_type=NodeType.PROCESS, metadata={})
    edge = TomographyEdge(id="e1", from_id=NODE, to_id=NODE, edge_type="sync_call", metadata={})
    tomo = TomographyGraph(client_id="demo", nodes=[node], edges=[edge])
    # fusible critico: si payload["threat"] > 0.5 -> reason critical -> STOP en hard
    blocking = FuseSpec(
        id="guard_dog", node_id=NODE, enabled=True, type="threshold", severity="critical",
        mode_scope=["shadow", "soft", "hard"],
        parameters={"field": "threat", "threshold": 0.5},
    )
    return ClientProfile(
        client_id="demo", profile_version="0.0",
        created_at=datetime.fromisoformat("2026-01-06T00:00:00"),
        consolidated_summary="", tomography=tomo,
        light_report=MarioReport(client_id="demo"),
        shadow_report=LuigiReport(client_id="demo"),
        notebook_summary=NotebookSummary(client_id="demo", condensed_summary=""),
        numeric_evidence=NumericEvidence(
            client_id="demo",
            normative=[0.5]*4, representational=[0.5]*4,
            informational=[0.5]*4, physical=[0.1]*4, metadata={},
        ),
        fuse_specs=[blocking],
        motor_output=MotorOutput(client_id="demo", scores={}, ranges={}, config_blob={}),
    )


def _blocking_request():
    return RuntimeDecisionRequest(
        client_id="demo", node_id=NODE, trace_id="amb-1",
        mode="hard", payload={"threat": 0.9}, context={},
    )


def test_pure_stop_when_no_reroute_registered():
    """Fail-closed: sin ruta registrada, el fusible critico corta en STOP puro."""
    op = DualRuntimeOperator(profile=_profile_with_blocking_fuse())
    resp = op.evaluate(_blocking_request())
    assert resp.decision == RuntimeDecision.STOP
    assert resp.reroute_options == []


def test_reroute_offered_instead_of_pure_stop():
    """Ambulancia: con ruta registrada, la respuesta ofrece reroute, no STOP puro."""
    reroute = RerouteOption(
        route_id="side_alley",
        description="Ruta lateral que evita al guardia sin abandonar la urgencia",
        preserves_need="la ambulancia llega al paciente",
        estimated_friction=0.3,
        target_node="hospital_entry",
    )
    op = DualRuntimeOperator(
        profile=_profile_with_blocking_fuse(),
        reroute_registry={NODE: [reroute]},
    )
    resp = op.evaluate(_blocking_request())
    # ya no es STOP puro
    assert resp.decision != RuntimeDecision.STOP
    assert resp.decision == RuntimeDecision.ESCALATE
    assert len(resp.reroute_options) >= 1
    opt = resp.reroute_options[0]
    assert opt.route_id == "side_alley"
    assert opt.preserves_need  # preserva la necesidad original
    # la razon del bloqueo sigue registrada (trazabilidad, no se oculta)
    assert any(r.severity == "critical" for r in resp.reasons)


def test_reroute_only_triggers_on_stop_not_on_go():
    """La capa de reroute no altera decisiones que no eran STOP."""
    op = DualRuntimeOperator(
        profile=_profile_with_blocking_fuse(),
        reroute_registry={NODE: [RerouteOption(route_id="x")]},
    )
    safe = RuntimeDecisionRequest(
        client_id="demo", node_id=NODE, trace_id="safe-1",
        mode="hard", payload={"threat": 0.1}, context={},  # bajo umbral -> GO
    )
    resp = op.evaluate(safe)
    assert resp.decision == RuntimeDecision.GO
    assert resp.reroute_options == []


def test_reroute_field_is_additive_default_empty():
    """El campo reroute_options es aditivo: default vacio, no rompe schema previo."""
    from antigravity_wings.api.models import RuntimeDecisionResponse
    r = RuntimeDecisionResponse(
        trace_id="t", client_id="c", node_id="n", decision=RuntimeDecision.GO,
    )
    assert r.reroute_options == []
