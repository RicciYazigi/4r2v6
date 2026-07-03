"""
Tests de contrato para validar la integridad de los modelos de datos en api/models.py.
Asegura que las dataclasses se puedan instanciar correctamente y validen tipos básicos.
"""

from datetime import datetime
from antigravity_wings.api.models import (
    SystemSnapshot,
    TomographyNode,
    TomographyEdge,
    TomographyGraph,
    MarioReport,
    LuigiReport,
    ConsolidatedReport,
    RuntimeDecision,
    ReasonDetail,
    RuntimeDecisionRequest,
    RuntimeDecisionResponse,
    NodeType,
    EdgeType
)

def test_system_snapshot_instantiation():
    snapshot = SystemSnapshot(
        client_id="test_client",
        raw_docs=["doc1", "doc2"],
        observed_flows=[{"step": "login"}]
    )
    assert snapshot.client_id == "test_client"
    assert len(snapshot.raw_docs) == 2
    assert isinstance(snapshot.captured_at, datetime)

def test_tomography_graph_structure():
    node = TomographyNode(
        id="node1",
        label="Start",
        node_type=NodeType.ENTRY
    )
    edge = TomographyEdge(
        id="edge1",
        from_id="node1",
        to_id="node2",
        edge_type=EdgeType.SYNC_CALL
    )
    graph = TomographyGraph(
        client_id="test_client",
        nodes=[node],
        edges=[edge]
    )
    assert len(graph.nodes) == 1
    assert len(graph.edges) == 1
    assert graph.nodes[0].node_type == NodeType.ENTRY

def test_reports_defaults():
    mario = MarioReport(
        client_id="client",
        strengths=[],
        redundancies=[],
        safe_zones=[],
        notes=[]
    )
    luigi = LuigiReport(
        client_id="client",
        risks=[],
        fragile_dependencies=[],
        no_return_points=[],
        notes=[]
    )
    consolidated = ConsolidatedReport(
        client_id="client",
        summary="summary",
        mario=mario,
        luigi=luigi,
        references=[]
    )
    assert consolidated.mario == mario
    assert consolidated.luigi == luigi

def test_runtime_decision_enums():
    assert RuntimeDecision.GO.value == "go"
    assert RuntimeDecision.STOP.value == "stop"

def test_runtime_decision_request_defaults():
    req = RuntimeDecisionRequest()
    assert req.node_id == "decision_1"
    assert req.payload == {}
    assert req.mode == "shadow"

def test_runtime_decision_response_structure():
    reason = ReasonDetail(
        fuse_id="fuse1",
        node_id="node1",
        severity="low",
        rule_type="threshold",
        message="ok"
    )
    resp = RuntimeDecisionResponse(
        trace_id="trace_123",
        client_id="client1",
        node_id="node1",
        decision=RuntimeDecision.GO,
        reasons=[reason]
    )
    assert resp.decision == RuntimeDecision.GO
    assert len(resp.reasons) == 1
    assert resp.reasons[0].fuse_id == "fuse1"
