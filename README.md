# 4R2 Coherence Guardrail — Quickstart

**Version:** kernel v6.1.0 (ADR-0001…0007) | **Status:** production-ready core,
evidence-sealed | **License:** Proprietary / Internal

Deterministic runtime guardrail for LLM agents: scores every decision across
the NRIF tetrad (Normative / Representational / Informational / veriFiability),
returns **ALLOW / FLAG / BLOCK** in ~0.12 ms, fail-closed, with SHA-256
reproducible evidence. Defense in depth: convex gate (θ) + Layer Breach
Breaker (ADR-0007) + VER fuses — each layer closes a measured failure class
(see `docs/E2_E3_REPORT.md`).

## Setup (60 seconds)

```bash
git clone https://github.com/RicciYazigi/4r2v6.git && cd 4r2v6
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install numpy pytest fastapi httpx uvicorn pydantic
# Optional (semantic tier for E2): pip install sentence-transformers
```

Requirements: Python ≥ 3.10, numpy. Everything else is optional per component.

## Quickstart — verify the whole system (2 minutes)

```bash
python -m pytest -q                                  # 65 tests
PYTHONPATH=core python -c "from kernel_1240421 import CoherenceKernel as K; print(K.selftest())"
python scripts/determinism_harness.py                # bit-identical, SHA-sealed
python scripts/eval_e1_e4.py                         # baseline + adversarial (LBB)
python scripts/eval_e2_e3.py                         # real-embedding eval + shadow pilot
```

Expected: 65/65 pass · `perfect_c: 0.0` · determinism PASS ·
E4 veto 100% · E2 T3 acceptable 1.0 · E3 incidents 0.

## Minimal usage

```python
import numpy as np, sys; sys.path.insert(0, "core")
from kernel_1240421 import CoherenceKernel, LayerState, Regime

k = CoherenceKernel()                       # balanced weights (ADR-0005)
state = LayerState(
    normative=emb("policy text"),           # your embedder, any dim d
    representational=emb("user request"),
    informational=emb("model output"),
    physical=np.array([0.9, 1.0, 0.8, 0.7]) # verifiability [0,1]^4
)
c_total, res = k.compute_with_regime(state, Regime())   # theta=0.35 default
print(res["verdict"], res["lbb_trigger"], res["breakdown"])
```

Calibrate θ per embedder with the percentile procedure in
`scripts/eval_e2_e3.py` (θ* = midpoint of p95(benign) / p5(grave)).

## Make targets

```bash
make test-local     # pytest without docker
make evals          # E1/E4 + E2/E3 + determinism
make parity         # 4 kernel replicas -> must print 1 (single hash)
make test           # dockerized test run (requires Docker)
make real-run       # dockerized 100%-real e2e (requires Docker)
```

## Repository map

| Path | What it is |
|:-----|:-----------|
| `core/kernel_v6.py` | Mathematical single source of truth |
| `core/kernel_1240421.py` | Canonical wrapper v6.1.0 (LBB, dual-path C_IF) |
| `docs/CANON_SPEC.md` | Authoritative math spec |
| `docs/ADRs/` | 7 architecture decision records |
| `docs/E2_E3_REPORT.md` | Real-embedding eval + shadow pilot results |
| `docs/ROADMAP_DEFINITIVO.md` | Milestones v6.2 → v7 |
| `scripts/` | Eval harnesses, determinism, evidence tooling |
| `evidence/` + `evidence_index.json` | SHA-256 chained artifacts (E1/E2/E3/E4) |
| `antigravity_wings/` | Governance shell (fuses, dual agents, orchestration) |
| `4R2-MASTER-DELIVERY/` | Deployable systems (basic/enhanced) + hardening tests |
| `historiafable5.md` | Full engineering log (4 audit cycles, sealed hashes) |

## CI

`.github/workflows/ci.yml` runs on every push: pytest, determinism harness,
E1/E4, E2/E3, and replica hash-parity. A red parity check means a kernel copy
drifted — fix before merging.

## Evidence rule

If an artifact is not in `evidence_index.json`, it does not exist for audit
purposes. Regenerate after adding evidence:
`python scripts/generate_evidence_index.py --evidence-dir evidence --output evidence_index.json`