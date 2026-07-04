# ADR-0006: Angular Metric Canon, Dual-Path C_IF, and Gate Recalibration

**Date:** 2026-07-04
**Status:** Accepted
**Supersedes:** numeric examples in ADR-0001/ADR-0005 verification sections; CANON_SPEC v5.3 formulas
**Author:** Co-arquitectura Richie + Claude Fable 5

## Context

The v6.0 kernel (`kernel_v6.py`) replaced the `1 - cos` similarity with a true
angular metric and redefined the F-layer as a verifiability vector. The wrapper
(`kernel_1240421.py`) adopted v6 math, but three latent defects and a
documentation drift survived:

1. **P0 — Silent-clip blind spot.** `compute_C_IF` did `clip(physical, 0, 1)`.
   Raw hardware telemetry (e.g. `[1000, 8, 50, 10]`) clipped to `[1,1,1,1]`,
   yielding `C_IF = 0.0` — a *false certificate of perfect physical coherence*
   for any caller using the legacy F convention (all root tests and several
   production scripts do).
2. **P0 — Gate threshold on the wrong scale.** `Regime.theta` defaulted to
   `0.75` (a value calibrated for the old `1 - cos` scale, range [0,2]) while
   the v6 gate operates on the angular scale (range [0,1], where orthogonal
   = 0.5). Effectively almost everything passed the Hard-Gate.
3. **P0 — Directional inversion in CRITICAL mode.** `intent_level="CRITICAL"`
   executed `theta = theta + 0.1`, *relaxing* the gate exactly when it should
   tighten. Same inversion in `CCA.to_regime` (crit>0.7 → theta 0.95).
4. **Doc drift.** CANON_SPEC/ADR-0005 still documented `1 - cos` formulas,
   ranges [0,2], zone bounds 0.35/0.65, and the promised
   `CoherenceKernel.PHYSICS_PRIORITY_PROFILE` registry did not exist in code.

## Decision

### D1. Angular metric is canon for all inter-layer coherence
```
d(a, b) = arccos( clip( a·b / (|a||b|), -1, 1 ) ) / π   ∈ [0, 1]
```
True metric (triangle inequality holds), unbiased (identical vectors → 0),
orthogonal → 0.5, antipodal → 1.0. Applies to C_NR, C_RI and legacy C_IF.

### D2. Dual-path C_IF (backward-compatible, fail-visible)
- **Path A (canonical):** if `F ∈ [0,1]^4`, F is verifiability
  `(f_ground, f_num, f_cite, f_exec)` → `C_IF = 1 - mean(F)`.
- **Path B (legacy raw telemetry):** if any component of F is outside [0,1],
  F is raw hardware magnitude → `C_IF = d(pad(Î), pad(F̂))` (zero-pad to common
  size, re-normalize, angular distance). Never again `C_IF = 0` by clipping.
- `compute_with_regime` injects Path B through a verifiability proxy
  `F* = full(4, 1 - C_IF)` so the v6 pipeline reproduces the identical value.

### D3. Gate recalibration to the angular scale
Old thresholds map by `d_new = arccos(1 - d_old) / π`:

| Concept              | old (1-cos) | new (angular) |
|:---------------------|:-----------:|:-------------:|
| GREEN upper bound    | 0.35        | **0.28**      |
| RED lower bound      | 0.65        | **0.39**      |
| Hard-Gate θ default  | 0.65–0.75   | **0.35**      |

`Regime.theta` default = 0.35 (matches kernel_v6). Verdicts: ALLOW iff
`C_total ≤ θ`; FLAG iff `≤ θ + 0.15`; BLOCK otherwise. Fail-closed on any
scoring exception (v6 D6, unchanged).

### D4. CRITICAL tightens — never relaxes
- `Regime(intent_level="CRITICAL")`: `θ ← max(0.15, θ - 0.10)`.
- `CCA.to_regime`: `θ = 0.25` if criticality > 0.7 else `0.35`.
- kernel_v6 additionally applies `θ ← max(0.15, θ - 0.10)` when
  `criticality > 0.7`. The compounding (0.25 → 0.15 effective) is intentional:
  double-flagged criticality deserves the strictest gate.

### D5. Weight-profile registry (fulfils ADR-0005's promise)
`CoherenceKernel.WEIGHT_PROFILES = {balanced, physics_priority,
normative_priority, regime_default}` with `PHYSICS_PRIORITY_PROFILE`
(1/21, 4/21, 16/21) as explicit opt-in only. Balanced (1/3 each) remains the
mandatory production default.

## Security guarantee (recomputed for the angular scale)

With balanced weights, an antipodal normative breach (C_NR = 1.0) contributes
≥ 1/3 ≈ 0.333 to C_total → always lands ≥ GRAY (0.28) and typically RED
(measured canonical case: C_total = 0.6667 → BLOCK). An *orthogonal* breach
contributes 0.5/3 ≈ 0.167; combined with its induced C_RI/C_IF the measured
ADR-0005 scenario scores C_total = 0.3326 → GRAY (fuse `GRAY_WARNING` fires).

## Canonical measured values (evidence, 2026-07-04)

```
selftest: perfect_c=0.0  bad_c=0.5833  loss_correct_direction=True
legacy docker example ones(4) vs [1000,8,50,10]: C_IF=0.3210, C_total=0.1070
ADR-0005 scenario (raw F): C_NR=0.5000 C_RI=0.2500 C_IF=0.2477 C_total=0.3326
antipodal normative breach: C_total=0.6667 → RED / BLOCK
CRITICAL regime theta: 0.25 (CCA) → 0.15 effective (v6 compounding)
pytest: 65/65 PASSED
determinism harness: PASS (20 runs, tol 1e-12)
```

## Consequences

- All 65 tests remain green; zone boundaries in
  `fuse_config/generator.py`, `end_to_end_validation.py`, `cca.py`,
  `orchestration/master.py` recalibrated to the angular scale.
- Historical evidence sealed before 2026-07-04 remains valid *for the old
  scale* and is superseded by the hashes in `historiafable5.md`.
- CANON_SPEC.md updated to v6.0.1; any doc claiming `1 - cos` formulas,
  [0,2] ranges, or 0.35/0.65 zones is stale.

## References

- ADR-0001 (geometry rationale, formulas superseded), ADR-0002 (weighted sum,
  unchanged), ADR-0003 (quadratic loss, unchanged), ADR-0004 (real motor,
  unchanged), ADR-0005 (balanced weights, verification numbers superseded).
- `historiafable5.md` — full action log and sealed hashes of this cycle.
