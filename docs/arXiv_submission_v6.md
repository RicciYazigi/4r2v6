# Geometric Coherence Gating for LLM Runtime Governance: the 4R2 Guardrail

**Draft for arXiv submission (cs.AI / cs.SE) — v6.1.0, 2026-07-04**
**Authors:** Ricardo "Ricci" Yazigi (architecture & direction); agentic
collaboration acknowledged (Claude Fable 5 — verification, adversarial
evaluation, ADR-0006/0007).

## Abstract

We present 4R2, a deterministic runtime guardrail that scores the coherence of
an LLM-driven decision across a four-layer tetrad — Normative (policy),
Representational (request), Informational (output), and Verifiability — and
gates execution through a fail-closed verdict (ALLOW/FLAG/BLOCK). Coherence
between embedding layers uses the normalized angular distance
d(a,b)=arccos(â·b̂)/π, a true metric on the unit sphere; verifiability is an
explicit [0,1]⁴ vector (groundedness, numeric, citation, executability).
We identify and close a structural vulnerability of convex score aggregation —
the *single-layer camouflage attack*, in which any one violated layer is
diluted below the gate threshold by healthy siblings — via a Layer Breach
Breaker (LBB). On a controlled synthetic benchmark (300 labeled cases, exact
geometric ground truth), the gated kernel achieves 0.0 false-positive rate on
on-topic traffic, 0.0 false-negative rate on grave off-topic content, and
raises adversarial veto accuracy from 50% (convex gate alone) to 100% (with
LBB). The scoring path is bit-deterministic (20 runs, 1e-12 tolerance,
SHA-256-sealed evidence).

## 1. Method

**Layer state.** S = (N, R, I ∈ ℝᵈ; F ∈ [0,1]⁴). Legacy raw telemetry F is
accepted through a documented dual path (angular distance on zero-padded unit
vectors) — never silently clipped.

**Coherence.** C_NR = d(N,R); C_RI = d(R,I); C_IF = 1 − mean(F).
C_total = Σ wⱼCⱼ, w on the simplex, production default w = (1/3,1/3,1/3).

**Irreversibility.** R_irr = JS(π_t ‖ π_{t−1}) over verdict distributions
(bounded, symmetric); Landauer is a conceptual analogy only, not a hardware
reading.

**Loss.** L = base + α·max(0,C_total)² + γ·R_irr + δ·K_contra, monotone in
C_total.

**Gate.** ALLOW iff C_total ≤ θ (default 0.35); FLAG ≤ θ+0.15; else BLOCK.
Criticality tightens θ (never relaxes). Any scoring exception ⇒ BLOCK.

**Layer Breach Breaker (contribution).** Convexity bounds any single layer's
contribution by max wⱼ < θ, so single-layer violations pass the gate. LBB adds
per-layer caps: max(C_NR, C_RI) ≥ 0.75 ⇒ BLOCK; ≥ 0.60 ⇒ ALLOW→FLAG.

## 2. Threat model & evaluation

Four adversarial families (20 cases each, seed 1240421): normative camouflage
(antipodal N↔R, perfect F), legacy raw-F exploitation, zero-vector poisoning,
verifiability inflation. Baseline set: 100 on-topic, 60 mild-drift, 60 grave,
across technical/financial/conversational/critical domains. Vectors are
constructed at controlled angular distances, so labels are exact by
construction (no annotation noise).

| Metric | Convex gate | + LBB |
|:-------|:---:|:---:|
| FPR (on-topic, n=100) | 0.0 | 0.0 |
| FNR (grave, n=60) | 0.0 | 0.0 |
| Adversarial veto (n=80) | 0.50 | **1.00** |

## 3. Limitations

(i) Synthetic-controlled benchmark: results certify the *gating mathematics*,
not embedding quality; real-embedding evaluation (E2/E3) is future work.
(ii) LBB thresholds are globally calibrated; per-domain calibration pending.
(iii) Verifiability vector is supplied by the environment; garbage-in applies
(mitigated by fail-closed validation).

## 4. Reproducibility

Deterministic seed 1240421; no RNG in the scoring path; evidence sealed:
dataset `da23cad533ffbf82…`, results `de6056dbd699ccb4…`, determinism harness
PASS (20 runs, 1e-12). Code: `core/kernel_v6.py` + `core/kernel_1240421.py`;
spec `docs/CANON_SPEC.md`; decisions ADR-0001…0007.
