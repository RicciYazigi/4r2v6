# LIMITATIONS — proven vs. empirical guarantees (v7.0.0)
Read this before quoting any claim in a deck, paper or diligence answer.
Every claim below is tagged. Do not upgrade tags.
## 1. Mathematically proven (hold for all inputs, by construction)
| Claim | Why it holds |
|:------|:-------------|
| `d(a,b) = arccos(clip(cos))/π` is a true metric on the unit sphere, range `[0,1]`, triangle inequality holds | Standard geodesic distance, normalized (ADR-0006, D1) |
| `C_total ∈ [0,1]` | Convex combination (simplex weights, internal normalization) of distances bounded in `[0,1]` (D2) |
| JS divergence term is symmetric, finite, bounded `[0, ln 2]` | Property of JS with clipping (D4) |
| Fail-closed: any exception in scoring ⇒ `BLOCK` | try/except wrapping in `kernel_v6.gate`, `Guardrail.evaluate` (never raises) and the sidecar route (D6) |
| Determinism: identical inputs + identical embedder ⇒ bit-identical `C_total` | No RNG, no wall-clock, no I/O in the scoring path; verified to 1e-12 over 20 runs by `scripts/determinism_harness.py` (the 1e-12 check is empirical; the absence of nondeterminism sources is by construction) |
| With balanced weights, no single layer can contribute more than 1/3 to `C_total` | Direct consequence of convexity — this is precisely why LBB exists (ADR-0007) |
## 2. Empirical with explicit scope (true for the stated corpus/config only)
| Claim | Scope | Evidence |
|:------|:------|:---------|
| E1: FPR 0.0 (n=100 on-topic), FNR 0.0 (n=60 grave) | dataset_E1.json, seed-fixed, kernel defaults | `evidence/eval_E1_E4_results.json` |
| E4: adversarial veto 100% (80/80); 50% without LBB | E4 attack taxonomy, internal | idem |
| E2/T3: FPR 0.0, FNR 0.0, veto 100%, acceptability 1.0 | E2 corpus (240 cases), LSA/ST embedder, θ*=0.4625, LBB+VER fuse | `docs/E2_E3_REPORT.md`, `evidence/eval_E2_results.json` |
| E3 shadow pilot: 300 events, 0 incidents, 0.124 ms mean latency | simulated shadow traffic | `evidence/eval_E3_shadow.json` |
| Benchmark v7 (SDK path): benign ALLOW 1.0, FNR 0.0, veto 1.0, acceptability 1.0 | E2 corpus, held-out calibration split, HashingEmbedder, heuristic F, grounding fuse 0.15 | `evidence/benchmark_v7_results.json` |
| Grounding-fuse floor 0.15 separates classes | E2 corpus only (benign min f_ground 0.214 vs adversarial min 0.057) | benchmark + `four_r2/guardrail.py` rationale comment |
| Sub-millisecond latency | this hardware, HashingEmbedder; a semantic embedder dominates end-to-end latency | benchmark `latency_ms` |
| v7 Frontier: camouflage attacker 100%→55% both axes, high-ver FPR 0.0, negation evasion 93.3%→0% | E2 corpus + geometric attack, seed 1240421 | `evidence/eval_E4E5_results.json`, `eval_high_ver_fpr.json`, `eval_negation_hardening.json`, `docs/FRONTIER_REPORT.md` |
**Rule:** none of these numbers generalize to unseen distributions, other
embedders, or other θ. θ and fuse floors are embedder-specific and must be
recalibrated (`four_r2.calibration`).
## 3. Explicit non-claims (things 4R2 does NOT assert)
- **No physical thermodynamics.** Landauer is conceptual inspiration only;
  `R_irr` is JS divergence over the verdict policy, not physical entropy
  (kernel_v6 header, D4). Any "quantum" or thermodynamic framing of the
  classical vectors would be marketing, not math — we do not make it.
- **No universal completeness/soundness theorem.** There is no proof that the
  NRIF tetrad captures all harm classes, nor can there be for open-ended
  semantics. Coverage claims are per-attack-class and empirical (E4 taxonomy).
- **No robustness proof against unseen attack classes.** LBB closes the
  measured single-layer-camouflage class; coordinated multi-layer drift that
  keeps every pairwise distance below θ and LBB thresholds is a residual risk
  (see docs/THREAT_MODEL.md) and has not been exhaustively measured.
- **The default HashingEmbedder is lexical, not semantic.** Vocabulary-disjoint
  paraphrase attacks will look distant (usually fail-safe: FLAG/BLOCK) but
  semantic equivalence is not modeled; use the semantic tier + recalibration
  for paraphrase-heavy domains.
- **F quality bounds guardrail quality.** C_IF is only as good as the
  verifiability signals supplied. The heuristic F in the benchmark is a
  deterministic lexical proxy, not ground truth verification.
- **Internal corpora.** All shipped evaluations use project-built corpora. No
  independent external benchmark has been run yet (roadmap item; the harness
  accepts `--corpus` for exactly this purpose).
- **No compliance certification.** The EU AI Act mapping is a plausibility
  analysis, not a legal opinion.
## 4. Known engineering debt (tracked, not hidden)
- Sidecar metrics are per-process (aggregate via Prometheus scrape).
- Docker builds are declared but not executed in sandboxed sessions (ND);
  verify on a Docker host per RUNBOOK.
- `datetime.utcnow()` deprecation warnings in 4R2-MASTER-DELIVERY legacy API
  (warning-level, not failure).
