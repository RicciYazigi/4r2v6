# ADR-0008: Frontier v7.0 H(x) energy score, and dropping the (1−C_IF) term

**Date:** 2026-07-05
**Status:** Accepted
**Deciders:** Fable 5 (co-architect), Richie (human direction)
**Related:** ADR-0006 (angular metric), ADR-0007 (Layer Breach Breaker),
`core/frontier_v7.py`, `docs/FRONTIER_REPORT.md`,
`evidence/eval_high_ver_fpr.json`, `evidence/eval_E4E5_results.json`

## Context

ADR-0001 and ADR-0002 remain unchanged historical records (their 1−cos formulas
are legacy; ADR-0006 is the current canon). This ADR does NOT rewrite them — it
records a new decision, per the project's ADR-immutability convention.

v7.0 introduced a layer-breach energy score to formalize the heuristic LBB:

```
H(x) = a·C_NR + b·C_RI + g·(1 − C_IF)          (a, b, g ≥ 0, on the simplex)
```

The intent of the `g·(1 − C_IF)` term was to penalize the "high-verifiability
camouflage" attack, in which an attacker sets perfect verifiability (C_IF → 0)
to dilute a real normative breach below the gate threshold.

## Problem found (reviewer, 2026-07-05)

The `(1 − C_IF)` term is **non-discriminative** for that attack. Both the
camouflage attacker and a *legitimately impeccable* case have C_IF = 0, hence
`(1 − C_IF) = 1`. With `g > 0` (e.g. the un-calibrated balanced config
a=b=g=1/3), H therefore treats genuine perfect verification as suspicious.

**Measured** (`evidence/eval_high_ver_fpr.json`, 120 legit high-verifiability
cases through the real kernel, all with F=[1,1,1,1]):

| H variant | FPR on high-ver legit | Attack veto |
|:----------|:---------------------:|:-----------:|
| balanced (a=b=g=1/3), θ=0.42 | **0.15** | 1.00 |
| Fisher-calibrated (a=1, g=0), θ=0.251 | **0.00** | 1.00 |
| breach-only (a=b=1/2, g=0), θ=0.209 | **0.00** | 1.00 |

The balanced term cost **15% false positives on the best traffic** and bought
**zero** additional attack veto. Independently, the E2 Fisher calibration had
already set g = 0 on real data — the data agreed before the flaw was noticed.

## Decision

1. **H(x) weights MUST be calibrated** (Fisher-LDA on benign vs breach). The
   un-calibrated balanced config is **retired** for production use.
2. On the camouflage threat, calibration correctly drives **g → 0**: the
   discriminative signal is in the breach layers (C_NR, C_RI), not in
   verifiability. Verifiability is already handled by the gate's C_total and by
   the negation-aware VER fuse; it must not be double-counted into H.
3. The `frontier_v7.HParams` default keeps `threshold = 1.01` (H escalation
   disabled) so an *uncalibrated* deployment never inherits the flawed behavior.
4. Regression tests lock this: `test_calibration_drives_gamma_to_zero_on_camouflage`
   and `test_balanced_H_penalizes_perfect_verifiability_REGRESSION`.

## Consequences

- H(x) remains the derived generalization of the LBB, now on a calibrated
  boundary over the breach layers, with **FPR = 0 on high-verifiability legit
  traffic** (measured) and attacker single-layer success cut 100% → 34%.
- Honest limitation retained: H is calibrated per deployment; outside
  calibration there is no guarantee. The formula still admits g > 0 if a future
  deployment's data ever supports it — but the default and the evidence say g≈0.

## Guarantee category

Mixed, explicitly separated: the FPR/veto numbers are **empirical (T2)**, sealed
by SHA-256 with seed 1240421; the H bounds/monotonicity are **mathematical
(T1)**, proven in `scripts/test_frontier_v7.py`.
