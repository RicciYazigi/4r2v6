"""
Agente MARIO (Forward Scan):
Analiza la Tomografía desde el inicio del flujo hacia adelante.
Inventario de capacidades, márgenes seguros, redundancias, zonas estables.
"""

from typing import List
from antigravity_wings.api.models import TomographyGraph, MarioReport


class MarioAgent:
    def analyze(self, graph: TomographyGraph) -> MarioReport:
        """
        Forward scan: identify capabilities, redundancies, safe zones.
        Real (non-redacted) logic based on graph structure.
        """
        node_types = [n.node_type for n in graph.nodes]
        has_entry = "entry" in node_types or any("entry" in str(n).lower() for n in graph.nodes)
        has_exit = "exit" in node_types

        strengths = [
            f"{len(graph.nodes)} nodes analyzed (forward).",
        ]
        if has_entry:
            strengths.append("Clear entry points detected.")
        if has_exit:
            strengths.append("Clear exit points detected.")
        if len(graph.edges) > len(graph.nodes):
            strengths.append("Multiple connection paths (redundancy signal).")

        redundancies = []
        # Simple heuristic: if more edges than nodes * 1.5, note redundancy
        if len(graph.edges) > len(graph.nodes) * 1.5:
            redundancies.append("High connectivity suggests path redundancy.")

        safe_zones = []
        if has_entry:
            safe_zones.append("entry")
        if has_exit:
            safe_zones.append("exit")

        notes = ["MARIO forward scan complete."]

        return MarioReport(
            client_id=graph.client_id,
            strengths=strengths,
            redundancies=redundancies,
            safe_zones=safe_zones,
            notes=notes
        )
