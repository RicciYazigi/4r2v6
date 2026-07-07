"""
Gate B — V7.7 Fusion Fase 3: desacople Mario/Luigi + Árbitro conservador.

Fuerza el desacuerdo Mario=GO / Luigi=STOP y verifica que el Árbitro aplica la
regla conservadora (STOP gana) Y registra la trazabilidad del desacuerdo (no solo
el resultado final). No se promedia.
"""
from datetime import datetime

from antigravity_wings.operators.dual_runtime import DualRuntimeOperator
from antigravity_wings.dual_agents.arbiter import ArbiterAuthority, DisagreementRecord
from antigravity_wings.profiles.client_profile import ClientProfile
from antigravity_wings.api.models import (
    TomographyGraph, TomographyNode, TomographyEdge,
    MarioReport, LuigiReport, NotebookSummary, NumericEvidence, MotorOutput,
    RuntimeDecisionRequest, RuntimeDecision, FuseSpec, NodeType,
)

NODE = "n1"


def _profile_with_high_fuse():
    node = TomographyNode(id=NODE, label="N", node_type=NodeType.PROCESS, metadata={})
    edge = TomographyEdge(id="e", from_id=NODE, to_id=NODE, edge_type="sync_call", metadata={})
    tomo = TomographyGraph(client_id="demo", nodes=[node], edges=[edge])
    high_fuse = FuseSpec(
        id="risk", node_id=NODE, enabled=True, type="threshold", severity="high",
        mode_scope=["shadow", "soft", "hard"], parameters={"field": "risk", "threshold": 0.5},
    )
    return ClientProfile(
        client_id="demo", profile_version="0.0",
        created_at=datetime.fromisoformat("2026-01-06T00:00:00"),
        consolidated_summary="", tomography=tomo,
        light_report=MarioReport(client_id="demo"), shadow_report=LuigiReport(client_id="demo"),
        notebook_summary=NotebookSummary(client_id="demo", condensed_summary=""),
        numeric_evidence=NumericEvidence(client_id="demo", normative=[0.5]*4,
            representational=[0.5]*4, informational=[0.5]*4, physical=[0.1]*4, metadata={}),
        fuse_specs=[high_fuse],
        motor_output=MotorOutput(client_id="demo", scores={}, ranges={}, config_blob={}),
    )


def test_arbitrate_conservative_max_not_average():
    rec = ArbiterAuthority.arbitrate(RuntimeDecision.GO, RuntimeDecision.STOP)
    assert rec.final == RuntimeDecision.STOP       # conservador, no promedio
    assert rec.disagreement is True
    assert rec.rule == "conservative_max"
    # simetrico
    rec2 = ArbiterAuthority.arbitrate(RuntimeDecision.STOP, RuntimeDecision.GO)
    assert rec2.final == RuntimeDecision.STOP


def test_agreement_has_no_disagreement_flag():
    rec = ArbiterAuthority.arbitrate(RuntimeDecision.GO, RuntimeDecision.GO)
    assert rec.disagreement is False
    assert rec.final == RuntimeDecision.GO


def test_runtime_mario_go_luigi_stop_arbiter_stops_and_traces():
    """En modo hard, un fusible 'high' hace Luigi=STOP y Mario=GO. Árbitro=STOP."""
    op = DualRuntimeOperator(profile=_profile_with_high_fuse())
    req = RuntimeDecisionRequest(client_id="demo", node_id=NODE, trace_id="t",
                                 mode="hard", payload={"risk": 0.9}, context={})
    resp = op.evaluate(req)
    assert resp.mario_decision == RuntimeDecision.GO
    assert resp.luigi_decision == RuntimeDecision.STOP
    assert resp.decision == RuntimeDecision.STOP          # regla conservadora
    # trazabilidad del desacuerdo (no solo el resultado)
    assert resp.meta["dual_disagreement"] is True
    assert resp.meta["mario_position"] == "go"
    assert resp.meta["luigi_position"] == "stop"


def test_no_regression_final_equals_canonical():
    """Sin fusibles -> GO; mario/luigi coinciden; sin regresion del contrato."""
    node = TomographyNode(id=NODE, label="N", node_type=NodeType.PROCESS, metadata={})
    tomo = TomographyGraph(client_id="demo", nodes=[node], edges=[])
    prof = ClientProfile(
        client_id="demo", profile_version="0.0",
        created_at=datetime.fromisoformat("2026-01-06T00:00:00"),
        consolidated_summary="", tomography=tomo,
        light_report=MarioReport(client_id="demo"), shadow_report=LuigiReport(client_id="demo"),
        notebook_summary=NotebookSummary(client_id="demo", condensed_summary=""),
        numeric_evidence=NumericEvidence(client_id="demo", normative=[0.5]*4,
            representational=[0.5]*4, informational=[0.5]*4, physical=[0.1]*4, metadata={}),
        fuse_specs=[], motor_output=MotorOutput(client_id="demo", scores={}, ranges={}, config_blob={}),
    )
    op = DualRuntimeOperator(profile=prof)
    resp = op.evaluate(RuntimeDecisionRequest(client_id="demo", node_id=NODE, mode="hard", payload={}, context={}))
    assert resp.decision == RuntimeDecision.GO
    assert resp.mario_decision == RuntimeDecision.GO
    assert resp.luigi_decision == RuntimeDecision.GO
    assert resp.meta["dual_disagreement"] is False
