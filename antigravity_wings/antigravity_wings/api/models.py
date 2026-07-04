from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum

class NodeType(str, Enum):
    ENTRY = "entry"
    DECISION = "decision"
    PROCESS = "process"
    EXIT = "exit"

class EdgeType(str, Enum):
    SYNC_CALL = "sync_call"
    ASYNC_EVENT = "async_event"
    HUMAN_HANDOFF = "human_handoff"

class SystemSnapshot(BaseModel):
    client_id: str
    captured_at: datetime = Field(default_factory=datetime.utcnow)
    raw_docs: List[str] = Field(default_factory=list)
    observed_flows: List[Dict[str, Any]] = Field(default_factory=list)

class TomographyNode(BaseModel):
    id: str
    label: str
    node_type: NodeType
    metadata: Dict[str, Any] = Field(default_factory=dict)

class TomographyEdge(BaseModel):
    id: str
    from_id: str
    to_id: str
    edge_type: EdgeType
    metadata: Dict[str, Any] = Field(default_factory=dict)

class TomographyGraph(BaseModel):
    client_id: str
    nodes: List[TomographyNode] = Field(default_factory=list)
    edges: List[TomographyEdge] = Field(default_factory=list)
    source_confidence: Dict[str, float] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class MarioReport(BaseModel):
    client_id: str
    strengths: List[str] = Field(default_factory=list)
    redundancies: List[str] = Field(default_factory=list)
    safe_zones: List[str] = Field(default_factory=list)
    notes: List[str] = Field(default_factory=list)

class LuigiReport(BaseModel):
    client_id: str
    risks: List[str] = Field(default_factory=list)
    fragile_dependencies: List[str] = Field(default_factory=list)
    no_return_points: List[str] = Field(default_factory=list)
    notes: List[str] = Field(default_factory=list)

class ConsolidatedReport(BaseModel):
    client_id: str
    mario: MarioReport
    luigi: LuigiReport
    summary: str
    references: List[str] = Field(default_factory=list)

    @property
    def light(self) -> MarioReport:
        return self.mario

    @property
    def shadow(self) -> LuigiReport:
        return self.luigi

class NotebookSummary(BaseModel):
    client_id: str
    condensed_summary: str
    key_points: List[str] = Field(default_factory=list)
    source_refs: List[str] = Field(default_factory=list)

class NumericEvidence(BaseModel):
    """Arquitectura Tetradimensional N-R-I-F (Canon v1.0)"""
    client_id: str
    normative: List[float] = Field(default_factory=list)
    representational: List[float] = Field(default_factory=list)
    informational: List[float] = Field(default_factory=list)
    physical: List[float] = Field(default_factory=list)
    confidence_score: float = 1.0
    metadata: Dict[str, Any] = Field(default_factory=dict)

class MotorOutput(BaseModel):
    client_id: str
    scores: Dict[str, float] = Field(default_factory=dict)
    ranges: Dict[str, Any] = Field(default_factory=dict)
    config_blob: Dict[str, Any] = Field(default_factory=dict)
    version: str = "1.0.0"

class FuseSpec(BaseModel):
    id: str
    node_id: str
    enabled: bool = True
    type: str = "threshold"
    severity: str = "medium"
    mode_scope: List[str] = Field(default_factory=lambda: ["shadow", "soft", "hard"])
    parameters: Dict[str, Any] = Field(default_factory=dict)

class RuntimeDecisionRequest(BaseModel):
    trace_id: Optional[str] = None
    client_id: str = "default_client"
    node_id: str = "decision_1"
    mode: str = "shadow"
    payload: Dict[str, Any] = Field(default_factory=dict)
    context: Dict[str, Any] = Field(default_factory=dict)

class ReasonDetail(BaseModel):
    fuse_id: str
    node_id: str
    severity: str
    rule_type: str
    message: str
    evidence: Dict[str, Any] = Field(default_factory=dict)

class RuntimeDecision(str, Enum):
    GO = "go"
    DEGRADE = "degrade"
    STOP = "stop"
    ESCALATE = "escalate"

class RuntimeDecisionResponse(BaseModel):
    trace_id: str
    client_id: str
    node_id: str
    decision: RuntimeDecision
    reasons: List[ReasonDetail] = Field(default_factory=list)
    scores: Dict[str, float] = Field(default_factory=dict)
    state_color: str = "green"
    cost_level: str = "low"
    mario_decision: Optional[RuntimeDecision] = None
    luigi_decision: Optional[RuntimeDecision] = None
    meta: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Added to fix import error in client_profile.py and tests (legacy model)
class BaselineSpec(BaseModel):
    id: str
    node_id: str
    metric: str = "coherence"
    threshold: float = 0.5
    description: str = ""
    parameters: Dict[str, Any] = Field(default_factory=dict)
