# ADR-0001: Cosine-based C_IF with zero-pad re-norm

**Date:** 2026-06-23  
**Status:** Accepted  
**Deciders:** Grok (agentic), Ricardo Yazigi  
**Related:** CANON_SPEC.md, core/kernel_1240421.py, gap_c_if_improvement

## Context
Previous implementation used capped KL-divergence for C_IF (Informational-Physical). This produced inconsistent values (e.g. C_IF=1.0 even for perfectly scaled cases) and was not uniform with C_NR and C_RI (which used 1 - cosine after _safe_norm).

Dimensional mismatch between informational vectors (often ~3-4D from translator) and physical (fixed 4D) required alignment.

## Decision
Adopt the same cosine distance for C_IF:
- _safe_norm both vectors
- Zero-pad the shorter to max length
- Re-normalize after padding
- C_IF = 1.0 - dot(padded_normed)

This makes all three coherence layers use identical mathematical primitive (1 - cosine after safe_norm + alignment where needed).

## Consequences
**Positive:**
- Uniform semantics across NRIF tetrad.
- Correct behavior on "perfect" cases (C_IF < 1.0 when directions align after norm).
- Better interpretability: lower C_IF = better I-F resource alignment proxy.
- Preserves determinism and bounds [0,2].

**Negative / Trade-offs:**
- C_IF remains a proxy metric (different semantic layers); documented limitation.
- Slight change in numeric values vs historical KL evidence (but historical evidence preserved; new evidence uses cosine).

**Impact on metrics:**
- C_total lowered for well-aligned cases (e.g. perfect state C_total ~0.1556 vs previous ~0.333).
- Loss_4R2 affected indirectly via C_total (but Loss formula itself uses C**2 as per separate ADR).
- Landauer Cost unchanged (independent).

**Evidence:**
- Docker selftest and brute runs post-change.
- determinism_harness SHAs sealed (e.g. e14207fb... for kernel).
- Updated CANON_SPEC.md with exact code + rationale.

## Verification
- Kernel tests updated for new bounds/behavior.
- All Docker re-vals (24/24, E2E, hardening) pass with cosine.
- No change to Loss_4R2 formula or Landauer.
