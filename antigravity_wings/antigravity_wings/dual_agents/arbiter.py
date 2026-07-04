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
