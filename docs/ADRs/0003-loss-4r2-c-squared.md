# ADR-0003: Loss_4R2 uses C_total ** 2 (higher C = higher penalty)

**Date:** 2026-06-23  
**Status:** Accepted  

## Context
Earlier implementations inverted the objective by using (1 - C_total)**2. Since lower C_total = better coherence, the penalty term must increase with C_total.

## Decision
L_4R2 = L_base + α * (C_total ** 2) + γ * L_landauer

## Consequences
- Monotonic: higher incoherence → higher loss (correct for optimization/gating).
- Critical semantic bug fixed; affects any downstream use of Loss for training or scoring.
- alpha/gamma remain tunable parameters (default 1.0).

**Impact on metrics:**
- Loss values now correctly higher for bad states (e.g. bad_loss 0.944 > perfect 0.5242 in selftest).
- C_total itself unchanged.
- Landauer term unaffected.

**Evidence:** kernel_1240421.py docstring and compute_loss_4R2, selftest "loss_correct_direction": true, all historical evidence regenerated or noted.

## Verification
- Kernel tests include direction test.
- All Docker runs confirm (including brutal runner and harness).
- Documented in CANON_SPEC.md and historial.
