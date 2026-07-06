# THREAT MODEL — 4R2 guardrail (v7.0.0)
Scope: the decision path `texts + F → embeddings → NRIF → gate → verdict`,
plus the sidecar exposure surface. Status per attack class: **CLOSED**
(measured + defense), **MITIGATED** (defense, partial measurement),
**RESIDUAL** (declared, not yet measured).
## Attack classes on the scoring path
| # | Class | Vector | Status | Defense | Evidence |
|--:|:------|:-------|:------:|:--------|:---------|
| 1 | Single-layer camouflage | Antipodal normative violation diluted by convex weights (no single layer can exceed 1/3 of C_total) | **CLOSED** | LBB (ADR-0007): max(C_NR, C_RI) ≥ 0.75 ⇒ BLOCK; ≥ 0.60 ⇒ FLAG; generalized by H(x) both-axes (ADR-0008) | E4: veto 50%→100% (n=80); frontier both-axes 100%→55% |
| 2 | Verifiability inflation | Pump f_num/f_exec while response is unmoored from request (f_ground ≈ 0.1) | **CLOSED** (on E2 corpus) | VER grounding fuse: F[0] < 0.15 ⇒ ALLOW→FLAG; plus mean(F) floor | benchmark_v7: veto 0.958 → 1.0 |
| 2b | High-verifiability camouflage (C_IF→0 dilutes a real breach) | Set perfect verifiability so convex dilution hides an N-R/R-I breach | **CLOSED** | H(x) calibrated on both breach axes (a≈b, g→0); (1−C_IF) retired as non-discriminative | `eval_high_ver_fpr.json`: FPR high-ver 15%→0%, veto both axes 1.0 |
| 3 | Poisoned inputs (zero vectors, NaN, dim mismatch, F outside [0,1]^4) | Malformed state to force silent pass | **CLOSED** | Fail-closed by exception ⇒ BLOCK at kernel, SDK and HTTP layers | test suite (fail-closed tests) |
| 4 | Raw-telemetry blind spot | Raw hardware magnitudes silently clipped to perfect C_IF | **CLOSED** | Dual-path C_IF (ADR-0006) | regression tests |
| 5 | Gate-direction inversion | CRITICAL intent relaxing θ instead of tightening | **CLOSED** | ADR-0006 fix: CRITICAL ⇒ θ − 0.10 (floor 0.15) | tests + spec |
| 6 | Coordinated multi-layer drift | Keep every pairwise distance just below θ AND below LBB thresholds while cumulative intent drifts | **RESIDUAL** | Partial: R_irr (JS over verdict policy) penalizes distribution shifts; not exhaustively attacked | not measured — declared |
| 7 | Semantic paraphrase evasion | Vocabulary-disjoint rephrasing to game a lexical embedder | **MITIGATED** | Usually fail-safe (distance grows ⇒ FLAG/BLOCK, not ALLOW); semantic tier + recalibration recommended; hardened negation detector (frontier) closes paraphrased control-bypass | LIMITATIONS §3; `eval_negation_hardening.json` 93.3%→0% |
| 8 | Threshold gaming after calibration leak | Attacker crafts c_total just under a known θ* | **MITIGATED** | Defense in depth: LBB + fuses fire independently of θ; keep θ* non-public per tenant | benchmark cases show fuses catching sub-θ attacks |
| 9 | F-signal spoofing | Caller supplies fabricated F=(1,1,1,1) | **RESIDUAL** | Out of scope of the kernel: F provenance must be enforced by the integrator (compute F server-side, never trust client F) | INTEGRATION.md guidance |
## Sidecar exposure surface
| Threat | Defense |
|:-------|:--------|
| Unauthenticated scoring / metrics scraping | `FOUR_R2_API_KEY` ⇒ X-API-Key required on /v1/evaluate and /metrics (health stays open for probes) |
| Fail-open on service error | Errors return HTTP 200 with `verdict=BLOCK, fail_closed=true` (a 5xx could be read as "no answer, proceed"); clients MUST treat any non-200 or unreachable sidecar as BLOCK |
| Payload abuse | Pydantic validation (types, [0,1] bounds, 4-element F, domain length cap) ⇒ 422 |
| Version confusion | /health reports package + kernel-math versions; release-coherence gate in CI |
## Integrator obligations (the guardrail cannot enforce these)
1. Compute F server-side from verifiable signals; never accept client-supplied F.
2. Treat sidecar unreachability/timeouts as BLOCK (fail-closed end-to-end).
3. Recalibrate θ and fuse floors when changing embedder, domain, or F pipeline.
4. Route FLAG to human review (that is its contract, per EU AI Act Art. 14 mapping).
