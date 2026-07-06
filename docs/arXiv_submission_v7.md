# Geometric Coherence Gating for LLM Runtime Governance: the 4R2 Guardrail (v7.0 "Frontier")

**Draft for arXiv submission (cs.AI / cs.SE) — v6.1.0, 2026-07-04**
**Authors:** Ricardo "Ricci" Yazigi (architecture & direction); agentic
collaboration acknowledged (Claude Fable 5 — verification, adversarial
evaluation, ADR-0006/0007/0008; H(x) design; both-axes camouflage closure).

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
SHA-256-sealed evidence). In v7.0 we generalize the LBB into a *calibrated
breach-energy score* H(x)=a·C_NR+b·C_RI+g·(1−C_IF) and add JS-divergence
camouflage and Shannon-entropy OOD telemetry. On a real-kernel extended attack
(E4-extended, both breach axes), the plain convex gate is evaded 100%; H(x)
cut single-layer attacker success to 55% symmetrically on both axes while
keeping 0.0 false-positive rate on high-verifiability legitimate traffic. We
report two *symmetric vulnerabilities of the defense itself*, found in internal
review and closed with data: (i) the (1−C_IF) term treats genuine perfect
verifiability as suspicious (15%→0% FPR once g calibrates to 0); (ii) a
single-axis calibration corpus degenerated the C_RI weight to 0, reopening the
camouflage gap on the other axis (closed by both-axes calibration; both breach
weights verified non-zero). We argue that reporting such symmetric failures —
rather than only headline veto rates — is what distinguishes an auditable
guardrail from a benchmarked classifier.

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

## 7. v7.0 "Frontier": calibrated H(x), both-axes closure, and honest negatives

**H(x) as a derived LBB.** The v6.1.0 LBB used hard thresholds
max(C_NR,C_RI) ≥ 0.75/0.60. v7.0 replaces the heuristic with a linear
breach-energy score H(x)=a·C_NR+b·C_RI+g·(1−C_IF) whose weights are calibrated
by Fisher linear discriminant on real labelled data. H is bounded [0,1] on the
simplex and monotone in each breach coordinate (proven, T1).

**Two symmetric vulnerabilities of the defense (found in review, closed with data).**

1. *The (1−C_IF) term.* Because a camouflage attacker forces C_IF→0, the term
   (1−C_IF)→1 was intended to penalize camouflage. But an impeccable legitimate
   case also has C_IF=0, so a balanced H (g=1/3) flagged 15% of
   high-verifiability legitimate traffic for zero additional veto. Fisher
   calibration drives g→0; the measured FPR on high-verifiability legitimate
   traffic drops 15%→0% with no loss of veto (ADR-0008).

2. *The C_RI-axis gap.* A calibration corpus whose attacks varied only C_NR made
   Fisher learn b=0, so a camouflage attack concentrated in C_RI (under the LBB
   floor) evaded H entirely — the single-layer camouflage vulnerability reopened
   on the orthogonal axis. Calibrating on a corpus containing attacks on **both**
   axes restores a≈b≈0.5, vetoes both axes, and we assert neither breach weight
   degenerates to 0 (regression test `test_calibration_covers_both_breach_axes`).

**Honest negative result.** Shannon entropy over the breach vector does **not**
detect the high-verifiability single-layer attack (attacker entropy sits inside
the benign band); it is retained as generic OOD telemetry, not claimed as this
attack's defense. Reporting this — instead of quietly dropping it — is central to
the auditability claim.

**Fisher vs angular.** A diagonal-Fisher reweighting of the layer features gives
ΔAUROC −0.06 vs the angular projection on the real corpus; we keep the angular
metric (a proven true metric) because generic embeddings are not parameters of a
distribution family for which a true Fisher-Information metric exists.

**Reproducibility.** All v7 figures are produced by seeded scripts
(`scripts/frontier_calibrate.py`, `scripts/eval_e4_extended.py`,
`scripts/eval_high_verifiability_fpr.py`, `scripts/eval_negation_hardening.py`)
and SHA-256-sealed in `evidence_index.json`. Test suite: 77/77.

**Limitations (named).** The hardened negation detector is lexical (n=15 probe),
not semantic. H(x) is calibrated per deployment; outside calibration there is no
guarantee. The sealed embedding backend is deterministic LSA; the
sentence-transformers tier runs in CI/host. The EU AI Act mapping remains
*plausible — pending legal review*, not certified.
