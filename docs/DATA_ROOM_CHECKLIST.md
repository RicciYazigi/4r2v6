# DATA ROOM CHECKLIST (acquisition / diligence readiness)
Status legend: DONE (in repo, verifiable) · PARTIAL · ND (not available —
requires business action, cannot be produced by code).
| Item | Status | Pointer |
|:-----|:------:|:--------|
| Canonical math spec + ADRs | DONE | docs/CANON_SPEC.md, docs/ADRs/ (0001…0008) |
| Version story (single, machine-enforced) | DONE | scripts/check_release_coherence.py, docs/VERSIONING_POLICY.md |
| Test suite (core + SDK + sidecar + frontier) all green | DONE | `python -m pytest -q` |
| Determinism proof harness | DONE | scripts/determinism_harness.py |
| Evidence chain (SHA-256 index) | DONE | evidence_index.json |
| Evaluations with scope-tagged claims | DONE | docs/LIMITATIONS.md §2 |
| Threat model (closed/mitigated/residual) | DONE | docs/THREAT_MODEL.md |
| Layer-decoupling defenses + reviewer-caught symmetric vulns | DONE | docs/FRONTIER_REPORT.md, ADR-0008 |
| Reproducible benchmark harness (external-corpus ready) | DONE | benchmarks/ |
| Integration guide + sidecar + Docker | DONE | docs/INTEGRATION.md |
| Dependency inventory | DONE | pyproject.toml (extras declared) |
| License & chain of title | PARTIAL | Proprietary notice present; formal IP assignment docs = ND (legal action) |
| External/independent benchmark run | ND | harness ready (`--corpus`); needs external corpus selection |
| Customers / pilots / LOIs / ARR | ND | business milestone, not a code artifact |
| Production traffic metrics (FP cost, incidents avoided) | ND | requires deployment; sidecar /metrics is the collection instrument |
| Compliance legal opinion (EU AI Act) | ND | mapping is plausibility-level (MEGA v6.1 §4); needs counsel |
Honesty note: the ND rows are the difference between "technically 10/10" and
"transactionally 10/10". No code deliverable can close them; only deployment
and commercial execution can.
