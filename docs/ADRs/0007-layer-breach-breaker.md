# ADR-0007: Layer Breach Breaker (LBB) & Fail-Closed Wrapper

**Date:** 2026-07-04 | **Status:** Accepted | **Extends:** ADR-0005, ADR-0006

## Context — the convex dilution attack

With balanced weights (1/3 each), C_total is a convex combination: **no single
layer can contribute more than 1/3 ≈ 0.333 < θ = 0.35**. Therefore any
single-layer breach camouflaged by two healthy layers passes the Hard-Gate.
Evaluation E4 (80 adversarial cases, seed 1240421) confirmed it empirically:

| Attack subtype | Raw v6 gate vetoed | Description |
|:---------------|:---:|:------------|
| A1 normative camouflage | **0/20** | antipodal N↔R + perfect verifiability |
| A2 legacy raw-F exploit | 20/20 | closed by ADR-0006 dual-path |
| A3 zero-vector poisoning | 20/20 | v6 fail-closed (D6) |
| A4 verifiability inflation | **0/20** | grave R↔I drift + F=[1,1,1,1] |

Raw-gate veto accuracy: **50%**. Additionally, the wrapper crashed
(`KeyError: C_total`) on v6 fail-closed results — a guardrail that raises on
poisoned input is not fail-closed.

## Decision

1. **LBB in `compute_with_regime`** (post-gate, pre-verdict):
   - `max(C_NR, C_RI) >= 0.75` ⇒ verdict **BLOCK** (`lbb_trigger=LBB_BLOCK`)
   - `max(C_NR, C_RI) >= 0.60` and verdict ALLOW ⇒ downgrade to **FLAG**
   - C_IF excluded: low verifiability already raises C_IF directly; F=[1,1,1,1]
     is a legitimate state, the attack surface is the inter-layer angles.
2. **Fail-closed wrapper**: v6 fail-closed results (no C_total) map to
   `C_total=1.0, breakdown={}, verdict=BLOCK` — never an exception upstream.
3. Result dict now exposes `verdict` (ALLOW/FLAG/BLOCK) and `lbb_trigger`.

## Rationale for thresholds

Angular scale: 0.5 = orthogonal (unrelated), 0.75 = strongly opposed,
1.0 = antipodal (contradiction). LBB_BLOCK at 0.75 targets active
contradiction of policy/representation; LBB_FLAG at 0.60 escalates
"beyond-orthogonal" drift to human review. Legitimate traffic measured in E1:
on-topic max layer < 0.15; off-topic-leve < 0.45 — an order gap below the
0.60 trigger (no false positives observed, n=160).

## Evidence (E1 + E4, kernel v6.1.0, deterministic seed 1240421)

```
E1 baseline (n=220):  FPR on-topic = 0.0   FNR grave = 0.0
  on-topic      C_total mean 0.0753  → 100 ALLOW
  off-leve      C_total mean 0.2978  → 57 ALLOW / 3 FLAG
  off-grave     C_total mean 0.7337  → 60 BLOCK
E4 adversarial (n=80): veto accuracy 50% (raw) → 100% (LBB)
dataset_E1.json       SHA256 da23cad533ffbf82...
eval_E1_E4_results    SHA256 de6056dbd699ccb4...
pytest 65/65 · determinism PASS · pilots PASS
```

## Consequences

- Kernel bumped to **v6.1.0**; 4 replicas re-synced to one hash.
- The 1/3-dilution property is now documented as an explicit attack class
  ("single-layer camouflage") in the arXiv draft §Threat Model.
- LBB thresholds are constants pending domain calibration (roadmap v6.2:
  per-domain LBB via DomainKernel).
