"""
Construye la Tomografía (grafo) a partir de un SystemSnapshot.

Descriptivo, no evaluativo.
"""

from typing import List
from antigravity_wings.api.models import (
    SystemSnapshot,
    TomographyGraph,
    TomographyNode,
    TomographyEdge,
    NodeType,
    EdgeType,
)


class TomographyBuilder:
    def build(self, snapshot: SystemSnapshot) -> TomographyGraph:
        nodes: List[TomographyNode] = []
        edges: List[TomographyEdge] = []

        nodes.append(TomographyNode(
            id="entry",
            label="Entry",
            node_type=NodeType.ENTRY,
            metadata={}
        ))
        nodes.append(TomographyNode(
            id="exit",
            label="Exit",
            node_type=NodeType.EXIT,
            metadata={}
        ))
        nodes.append(TomographyNode(
            id="decision_1",
            label="Decision Point 1",
            node_type=NodeType.DECISION,
            metadata={"observed_flows_count": len(snapshot.observed_flows)}
        ))

        edges.append(TomographyEdge(
            id="edge_1",
            from_id="entry",
            to_id="decision_1",
            edge_type=EdgeType.SYNC_CALL,
            metadata={}
        ))
        edges.append(TomographyEdge(
            id="edge_2",
            from_id="decision_1",
            to_id="exit",
            edge_type=EdgeType.SYNC_CALL,
            metadata={}
        ))

        return TomographyGraph(
            client_id=snapshot.client_id,
            nodes=nodes,
            edges=edges
        )
