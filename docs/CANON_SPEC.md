# 4R2 Canonical Specification (v6.0.1)

**Single Source of Truth**: `core/kernel_v6.py` (math) + `core/kernel_1240421.py` (canonical wrapper, algorithm 1240421).
**Date**: 2026-07-04 (ADR-0006 — angular metric canon).
**Status**: Authoritative. Supersedes v5.3 spec entirely. All evidence, tests and orchestration reference these definitions.

## 1. Layer State (NRIF Tetrad)

```python
@dataclass
class LayerState:
    normative: np.ndarray         # N: goals, constraints, declared policy
    representational: np.ndarray  # R: internal model / embeddings
    informational: np.ndarray     # I: outputs, tokens, actions (variable dim)
    physical: np.ndarray          # F: EITHER verifiability [0,1]^4
                                  #    (f_ground, f_num, f_cite, f_exec)
                                  #    OR legacy raw telemetry (len 4)
```

Validation: `len(physical) == 4`. All np.ndarray. N, R, I must share
embedding dimension for angular comparison (v6 enforces; wrapper pads I↔F).

## 2. Core Coherence Metrics (exact, locked)

### Angular distance (canonical primitive — ADR-0006)
```python
d(a, b) = arccos( clip( dot(â, b̂), -1, 1 ) ) / π    # ∈ [0, 1]
```
True metric; identical → 0, orthogonal → 0.5, antipodal → 1.0.
Zero-norm input ⇒ ValueError ⇒ gate fail-closed (BLOCK).

### C_NR, C_RI
```python
C_NR = d(N, R)
C_RI = d(R, I)
```

### C_IF — dual path (ADR-0006)
```python
if all(0 <= F_k <= 1):            # Path A: verifiability semantics (v6 D3)
    C_IF = 1 - mean(F)
else:                             # Path B: legacy raw telemetry
    C_IF = d( pad_renorm(Î), pad_renorm(F̂) )   # zero-pad to common size
```
Both paths ∈ [0, 1]. The silent-clip blind spot (raw F ⇒ C_IF=0) is removed.

### C_total (operational)
```python
C_total = w_NR·C_NR + w_RI·C_RI + w_IF·C_IF          # ∈ [0,1] by convexity
# Production default (ADR-0002 + ADR-0005): w = (1/3, 1/3, 1/3)
```
Named profiles in `CoherenceKernel.WEIGHT_PROFILES`:
`balanced` (default) | `physics_priority` (1/21, 4/21, 16/21 — explicit opt-in
only) | `normative_priority` (0.5, 0.3, 0.2) | `regime_default` (0.25, 0.25, 0.5).

**Invariant**: lower C_total = higher coherence. Antipodal normative breach
contributes ≥ 1/3 under balanced weights ⇒ can never land GREEN.

## 3. Irreversibility & Loss

### R_irr (v6 D4 — replaces physical Landauer)
```python
R_irr = JS(π_t ‖ π_{t−1})     # Jensen-Shannon over {ALLOW, FLAG, BLOCK}, ∈ [0, ln 2]
```
Legacy normalized form retained in wrapper: `cost = λ·decision_changes` (λ=0.05).
Landauer (`k_B·T·ln2·N`) is a conceptual analogy only — never a hardware reading.

### Loss_4R2
```python
L_4R2 = base + α·max(0, C_total)² + γ·R_irr + δ·K_contra
```
Monotone in C_total (correction of 2026-06-23 stands). Invariant:
`L(bad) > L(perfect)` — enforced by selftest.

## 4. Gate & Operational Zones (angular scale — ADR-0006)

```python
verdict = ALLOW  if C_total <= θ
        = FLAG   if C_total <= θ + 0.15
        = BLOCK  otherwise            # and BLOCK on any exception (fail-closed)
```

| Parameter | Value | Note |
|:----------|:-----:|:-----|
| θ default | **0.35** | `Regime.theta`; matches kernel_v6 |
| θ critical (CCA crit > 0.7) | 0.25 → 0.15 effective | CRITICAL always TIGHTENS |
| GREEN | C_total < 0.28 | old 0.35 mapped via arccos(1−x)/π |
| GRAY (GRAY_WARNING fuse) | 0.28 – 0.39 | old 0.35–0.65 |
| RED (RED_CRITICAL fuse) | > 0.39 | severity critical > 0.55 |

## 5. Canonical Evidence (selftest, 2026-07-04)

```
PYTHONPATH=core python -c "from kernel_1240421 import CoherenceKernel; print(CoherenceKernel.selftest())"
{'perfect_c': 0.0, 'perfect_loss': 0.5, 'bad_c': 0.5833, 'bad_loss': 0.9403,
 'loss_correct_direction': True}
```
Legacy example (ones(4) vs raw F [1000,8,50,10]): `C_IF=0.3210, C_total=0.1070`.

## 6. Determinism & Reproducibility

- No RNG in the scoring path. Fixed inputs ⇒ bit-identical outputs
  (harness: 20 runs, tolerance 1e-12, SHA-256 sealed).
- `history` is an append-only audit trail.
- Kernel replicas (core + basic + enhanced + tests) must share ONE SHA-256;
  CI/verification: `sha256sum` over the four copies.

## 7. Extensions (unchanged semantics)

- `measure_coherence_with_keys` — frozen API contract: `total_coherence`
  (raw, may be < 0) vs `coherence_score` (clamped [0,1]).
- **BeliefTracker** — log-odds pooling (κ=0.7 trusted / 0.4 untrusted) +
  Ebbinghaus decay on episodic facts (τ = 20 min default).
- **CalibratedEvaluator** — centered Platt σ((raw−b)/T).
- **DomainKernel / CCA / Regime** — contextual weight adjustment per ADR-0005 §3.
- **4R2_FUSES** — VER / ASYM / PRIO / GRAY_WARNING / RED_CRITICAL; fail-closed
  dispatch in `operators/dual_runtime.py`; zones per §4.

## 8. Version & Precedence

v6.0.1 = angular metric (D1) + dual-path C_IF (ADR-0006 D2) + simplex weights
(D2) + JS irreversibility (D4) + fail-closed gate (D6) + balanced default
weights (ADR-0005) + gate/zone recalibration (ADR-0006 D3/D4).

**Any code, test or doc claiming `1 - cos` formulas, ranges [0,2], zone bounds
0.35/0.65, or θ default 0.65–0.75 is stale.** See `historiafable5.md` for the
migration log and sealed hashes.
