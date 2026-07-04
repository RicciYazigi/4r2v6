# ADR-0002: C_total as weighted SUM (1/3 each) instead of product

**Date:** 2026-06-23  
**Status:** Accepted  

## Context
Early versions and some legacy docs referenced product form for overall coherence (C_NR × C_RI × C_IF) or other aggregations. Operational evidence, tests, and orchestrator always used or converged on weighted sum with equal 1/3 weights.

## Decision
Lock C_total = w_NR * C_NR + w_RI * C_RI + w_IF * C_IF (default w=1/3, sum(w)=1 verified).

## Consequences
- Convex combination, bounds [0,2] clean.
- Lower C_total always better (consistent direction for all layers).
- Easier interpretation and tuning of per-layer weights if needed in future.
- Matches all current evidence packs and determinism proofs.

**Impact on metrics:**
- No change to individual C_ values.
- C_total and downstream Loss_4R2 reflect additive penalties rather than multiplicative.
- Historical product mentions annotated as legacy.

**Evidence:** CANON_SPEC.md, kernel selftest, all Docker runs (global scores in E2E/fresh evidence use sum).

## Verification
- weight_sum == 1.0 assertion in kernel.
- Tests and harness confirm.
