"""
Agente LUIGI (Backward Scan):
Analiza la Tomografía desde el final hacia atrás.
Puntos sin retorno, cascadas de fallo, fragilidades, gaps operativos, riesgos.
"""

from antigravity_wings.api.models import TomographyGraph, LuigiReport


class LuigiAgent:
    def analyze(self, graph: TomographyGraph) -> LuigiReport:
        """
        Backward scan: identify risks, fragile dependencies, no-return points.
        Real (non-redacted) logic.
        """
        risks = []
        fragile = []
        no_return = []

        # Heuristic: look for nodes that appear as targets a lot (bottlenecks)
        target_counts = {}
        for e in graph.edges:
            target_counts[e.to_id] = target_counts.get(e.to_id, 0) + 1

        high_degree_targets = [k for k, v in target_counts.items() if v >= 2]

        if high_degree_targets:
            risks.append(f"High in-degree nodes: {high_degree_targets[:3]} (potential single points of failure)")
            fragile.extend(high_degree_targets[:2])
            no_return.extend(high_degree_targets[:1])

        if not high_degree_targets:
            risks.append("No obvious high-degree bottlenecks detected in backward scan.")

        notes = ["LUIGI backward scan complete. Review high in-degree nodes."]

        return LuigiReport(
            client_id=graph.client_id,
            risks=risks or ["No critical risks flagged by basic backward scan."],
            fragile_dependencies=fragile,
            no_return_points=no_return,
            notes=notes
        )
