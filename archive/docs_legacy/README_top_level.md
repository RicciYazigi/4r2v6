# 4R2 Coherence Guardrail
**Release:** 7.0.0 (product layer: SDK + sidecar + release coherence)
**Kernel math:** v6.1.0 — frozen, evidence-sealed, parity-protected (ADR-0001…0008)
**Status:** production-ready core | **License:** Proprietary / Internal

Deterministic runtime guardrail for LLM agents: scores every decision across
the NRIF tetrad (Normative / Representational / Informational / veriFiability),
returns **ALLOW / FLAG / BLOCK** in sub-millisecond time (0.124 ms mean,
measured, E3), fail-closed, with SHA-256 reproducible evidence. Defense in
depth: convex gate (θ) + Layer Breach Breaker (ADR-0007) + VER fuse — each
layer closes a *measured* failure class (`docs/E2_E3_REPORT.md`).

> Versioning contract: the **package** version (7.0.0) tracks the product
> layer. The **kernel math** stays at 6.1.0 because it is sealed by evidence
> (E1/E2/E3/E4) and 4-replica hash parity; changing it requires a new ADR and
> regenerated evidence. `scripts/check_release_coherence.py` enforces a single
> version story on every push. See `docs/VERSIONING_POLICY.md`.

> v7.0 Frontier defenses (opt-in, `core/frontier_v7.py`): a calibrated
> breach-energy score **H(x)** that generalizes the LBB across both breach
> axes, JS camouflage + Shannon OOD telemetry, and a paraphrase-robust
> negation detector. Two *symmetric vulnerabilities of the defense itself*
> were caught in review and closed with data — the `(1−C_IF)` term (ADR-0008)
> and the C_RI-axis calibration gap. Full account: `docs/FRONTIER_REPORT.md`;
> upgrade guide: `docs/MIGRATION_v6_to_v7.md`.

## Install (30 seconds)
```bash
git clone https://github.com/RicciYazigi/4r2v6.git && cd 4r2v6
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[service,dev]"
# Optional semantic embedder tier: pip install -e ".[semantic]"
```
Requirements: Python ≥ 3.10. Core needs only numpy; extras are declared in
`pyproject.toml` (no more undeclared deps).

## Verify the whole system (2 minutes)
```bash
python -m pytest -q                                  # full suite (core + SDK + sidecar + frontier)
python scripts/check_release_coherence.py            # one version story
PYTHONPATH=core python -c "from kernel_1240421 import CoherenceKernel as K; print(K.selftest())"
python scripts/determinism_harness.py                # bit-identical, SHA-sealed
python scripts/eval_e1_e4.py                         # baseline + adversarial (LBB)
python scripts/eval_e2_e3.py                         # real-embedding eval + shadow pilot
python benchmarks/public_benchmark.py                # reproducible benchmark + hash
```
Expected: all tests pass · `perfect_c: 0.0` · determinism PASS ·
E4 veto 100% · E2 T3 acceptable 1.0 · E3 incidents 0 · coherence PASS.

## Use it — 3 lines (SDK)
```python
from four_r2 import Guardrail
g = Guardrail()  # theta=0.35, balanced weights (ADR-0005), fail-closed
d = g.evaluate(
    policy="Only discuss corporate travel policy.",
    request="What is the hotel limit in Europe?",
    response="The policy sets the hotel limit at 180 EUR per night.",
    verifiability=(0.9, 1.0, 0.8, 0.7),   # (f_ground, f_num, f_cite, f_exec)
)
print(d.verdict, d.c_total, d.lbb_trigger)   # ALLOW / FLAG / BLOCK
```
`evaluate()` **never raises** — any internal failure returns `BLOCK` with
`fail_closed=True`. Omitting `verifiability` applies a neutral 0.5 prior
(strictly worse than verified content; supply real F in production).

## Use it — sidecar (any language)
```bash
uvicorn four_r2.service:app --port 8472           # or: docker compose -f docker-compose.sidecar.yml up -d
curl -s localhost:8472/health
curl -s -X POST localhost:8472/v1/evaluate -H 'Content-Type: application/json' \
  -d '{"policy":"...","request":"...","response":"...","verifiability":[0.9,1,0.8,0.7],"domain":"travel"}'
curl -s localhost:8472/metrics                     # Prometheus: verdicts, LBB, latency p50/p95/p99
```
Set `FOUR_R2_API_KEY` to require `X-API-Key`; `FOUR_R2_THETA` to override the
gate. Fail-closed answers are HTTP 200 with `verdict=BLOCK` (a 5xx could be
misread as "no answer, proceed").
Calibrate θ per embedder/domain with `four_r2.calibration.calibrate_theta`
(θ\* = midpoint p95(benign)/p5(grave); reports OVERLAP honestly if no clean
threshold exists). Integration recipes: `docs/INTEGRATION.md`.

## Make targets
```bash
make test-local     # pytest without docker
make evals          # E1/E4 + E2/E3 + determinism
make parity         # 4 kernel replicas -> must print 1 (single hash)
make coherence      # release-coherence gate
make benchmark      # reproducible public benchmark
```

## Repository map
| Path | What it is |
|:-----|:-----------|
| `core/kernel_v6.py` | Mathematical single source of truth |
| `core/kernel_1240421.py` | Canonical wrapper v6.1.0 (LBB, dual-path C_IF) |
| `core/frontier_v7.py` | v7.0 opt-in defenses: H(x), JS camouflage, Shannon OOD, hardened negation |
| `four_r2/` | **Product SDK**: Guardrail facade, embedders, calibration, metrics, sidecar |
| `tests/` | SDK + sidecar + release-coherence tests |
| `benchmarks/` | Reproducible benchmark harness + methodology |
| `docs/CANON_SPEC.md` | Authoritative math spec |
| `docs/LIMITATIONS.md` | **Proven vs. empirical guarantees** — read before quoting claims |
| `docs/THREAT_MODEL.md` | Attack classes: closed, mitigated, residual |
| `docs/FRONTIER_REPORT.md` | v7.0 Frontier: T1/T2 guarantees, both-axes attacks, SoTA comparison |
| `docs/ADRs/` | 8 architecture decision records (ADR-0008 = H(x) design) |
| `docs/E2_E3_REPORT.md` | Real-embedding eval + shadow pilot results |
| `evidence/` + `evidence_index.json` | SHA-256 chained artifacts (E1/E2/E3/E4/E5 + frontier + benchmark) |
| `antigravity_wings/` | Governance shell (fuses, dual agents, orchestration) |
| `4R2-MASTER-DELIVERY/` | Deployable systems (basic/enhanced) + hardening tests |

## CI
`.github/workflows/ci.yml` runs on every push: pytest (core + SDK + frontier),
release coherence, determinism harness, E1/E4, E2/E3, public benchmark, replica
hash-parity, and the v7 frontier gates. A red parity check means a kernel copy
drifted — fix before merging.

## Evidence rule
If an artifact is not in `evidence_index.json`, it does not exist for audit
purposes. Regenerate after adding evidence:
`python scripts/generate_evidence_index.py --evidence-dir evidence --output evidence_index.json`
