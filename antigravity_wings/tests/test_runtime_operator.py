from antigravity_wings.operators.dual_runtime import DualRuntimeOperator
from antigravity_wings.profiles.client_profile import ClientProfile
from antigravity_wings.api.models import (
    TomographyGraph,
    TomographyNode,
    TomographyEdge,
    MarioReport,
    LuigiReport,
    NotebookSummary,
    NumericEvidence,
    MotorOutput,
    RuntimeDecisionRequest,
    RuntimeDecision,
    NodeType,
)
from datetime import datetime


def test_dual_runtime_operator_import_and_evaluate_minimal_profile():
    # Minimal, self-consistent profile (no external motor calls)
    node = TomographyNode(
        id="node-1",
        label="Demo Node",
        node_type=NodeType.PROCESS,
        metadata={},
    )
    edge = TomographyEdge(
        id="edge-1",
        from_id="node-1",
        to_id="node-1",
        edge_type="sync_call",
        metadata={},
    )
    tomography = TomographyGraph(client_id="demo", nodes=[node], edges=[edge])

    mario_report = MarioReport(
        client_id="demo",
        strengths=[],
        redundancies=[],
        safe_zones=[],
        notes=[],
    )
    luigi_report = LuigiReport(
        client_id="demo",
        risks=[],
        fragile_dependencies=[],
        no_return_points=[],
        notes=[],
    )
    notebook_summary = NotebookSummary(
        client_id="demo",
        condensed_summary="",
        key_points=[],
        source_refs=[],
    )
    numeric_evidence = NumericEvidence(
        client_id="demo",
        normative=[0.5, 0.5, 0.5, 0.5],
        representational=[0.5, 0.5, 0.5, 0.5],
        informational=[0.5, 0.5, 0.5, 0.5],
        physical=[0.1, 0.1, 0.1, 0.1],
        metadata={},
    )

    profile = ClientProfile(
        client_id="demo",
        profile_version="0.0",
        created_at=datetime.fromisoformat("2026-01-06T00:00:00"),
        consolidated_summary="",
        tomography=tomography,
        light_report=mario_report,
        shadow_report=luigi_report,
        notebook_summary=notebook_summary,
        numeric_evidence=numeric_evidence,
        fuse_specs=[],
        motor_output=MotorOutput(client_id="demo", scores={}, ranges={}, config_blob={}),
    )

    operator = DualRuntimeOperator(profile=profile)

    req = RuntimeDecisionRequest(
        client_id="demo",
        node_id="node-1",
        trace_id="trace-1",
        timestamp="2026-01-06T00:00:00Z",
        payload={},
        context={},
    )

    resp = operator.evaluate(req)

    assert resp.client_id == "demo"
    assert resp.node_id == "node-1"
    assert resp.decision in {RuntimeDecision.GO, RuntimeDecision.DEGRADE, RuntimeDecision.ESCALATE, RuntimeDecision.STOP}
    # Ensure dual fields exist and are valid
    assert resp.mario_decision in RuntimeDecision
    assert resp.luigi_decision in RuntimeDecision
