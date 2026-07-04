from enum import Enum
from typing import List, Optional
from pydantic import BaseModel

class DecisionEnum(str, Enum):
    APPROVE = "approve"
    DEGRADE = "degrade"
    ESCALATE = "escalate"
    STOP = "stop"

class AgentVotes(BaseModel):
    luz_reason: str
    sombra_reason: str
    luz_score: float
    sombra_score: float

class DecisionContract(BaseModel):
    trace_id: str
    decision: DecisionEnum
    confidence: float
    primary_reason: str
    secondary_factors: List[str]
    fusibles_triggered: List[str]
    agent_votes: Optional[AgentVotes] = None
    pilot_id: str
    policy_version: str
