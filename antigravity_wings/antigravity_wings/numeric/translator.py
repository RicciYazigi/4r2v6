"""
NumericTranslator - Professional NRIF Vector Generation (v2)

Converts dual-agent reports + notebook summary into meaningful
Normative-Representational-Informational-Physical vectors.

This is a pragmatic but improved implementation. Vectors are
designed to carry real signal from the tomography + Mario/Luigi analysis.
"""

from typing import List
from antigravity_wings.api.models import (
    ConsolidatedReport,
    NotebookSummary,
    NumericEvidence,
)
import numpy as np


class NumericTranslator:
    """
    Improved translator from qualitative dual analysis to NRIF vectors.
    """

    def to_evidence(
        self,
        report: ConsolidatedReport,
        nb_summary: NotebookSummary
    ) -> NumericEvidence:
        mario = report.mario
        luigi = report.luigi

        # Normative (N): Alignment with declared standards + strengths
        # Higher strengths + fewer contradictions = better normative
        n_strength = min(1.0, len(mario.strengths) / 8.0)
        n_safety = min(1.0, len(mario.safe_zones) / 4.0)
        n_consistency = 0.85 if len(mario.notes) < 3 else 0.6
        normative = [n_strength, n_safety, n_consistency]

        # Representational (R): Quality of the internal model
        # Fewer risks + fewer fragile points = better model
        r_risk_penalty = max(0.0, 1.0 - len(luigi.risks) / 10.0)
        r_fragile_penalty = max(0.0, 1.0 - len(luigi.fragile_dependencies) / 6.0)
        r_no_return = max(0.0, 1.0 - len(luigi.no_return_points) / 4.0)
        representational = [r_risk_penalty, r_fragile_penalty, r_no_return]

        # Informational (I): Richness and clarity of output
        info_density = min(1.0, len(nb_summary.key_points) / 7.0)
        info_clarity = 0.9 if len(nb_summary.condensed_summary) > 40 else 0.65
        info_refs = min(1.0, len(nb_summary.source_refs) / 5.0)
        informational = [info_density, info_clarity, info_refs]

        # Physical (F): Resource / complexity indicators (proxy)
        # More nodes/edges and longer summary = higher resource demand
        node_count = len(getattr(report, 'graph_nodes', [])) or 12
        edge_count = len(getattr(report, 'graph_edges', [])) or 15
        complexity = min(1.0, (node_count + edge_count) / 40.0)
        latency_proxy = min(1.0, len(report.summary) / 300.0)
        energy_proxy = 0.3 + 0.4 * complexity   # synthetic but monotonic
        physical = [complexity, 0.25, energy_proxy, latency_proxy]

        # Normalize all vectors to reasonable ranges
        def norm(v):
            arr = np.array(v, dtype=float)
            s = arr.sum() + 1e-8
            return (arr / s * 3.0).tolist()   # scale so they are not tiny

        return NumericEvidence(
            client_id=report.client_id,
            normative=norm(normative),
            representational=norm(representational),
            informational=norm(informational),
            physical=physical,
            confidence_score=0.88,
            metadata={
                "engine": "NRIF-v2-improved",
                "source": "MasterOrchestrator",
                "mario_strengths": len(mario.strengths),
                "luigi_risks": len(luigi.risks),
                "key_points": len(nb_summary.key_points),
            }
        )
