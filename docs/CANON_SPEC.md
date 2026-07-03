# 4R2 Canonical Specification (v5.3 - Clean Workspace)

**Single Source of Truth**: `core/kernel_1240421.py` (algorithm 1240421).  
**Date**: 2026-07-03 (post v5.3 weights alignment).  
**Status**: Authoritative for this workspace. All evidence, tests, and orchestration reference these definitions.

This document is the mathematical and implementation contract. It takes precedence over any older or flat documents.

## 1. Layer State (NRIF Tetrad)

```python
@dataclass
class LayerState:
    normative: np.ndarray      # N: goals, constraints, declared policy
    representational: np.ndarray  # R: internal model / embeddings
    informational: np.ndarray     # I: outputs, tokens, actions (variable dim)
    physical: np.ndarray          # F: [FLOPS, mem_GB, energy_J, latency_ms] (always 4)
```

Validation: physical must have len==4. All are np.ndarray.

## 2. Core Coherence Metrics (exact)

All use the same primitive:

```python
def _safe_norm(self, vec: np.ndarray, epsilon: float = 1e-8) -> np.ndarray:
    norm = np.linalg.norm(vec)
    return vec / (norm + epsilon)
```

### C_NR (Normative-Representational)
```python
C_NR = 1.0 - dot( _safe_norm(N), _safe_norm(R) )
```
Range [0, 2]. 0 = identical direction after norm.

### C_RI (Representational-Informational)
```python
C_RI = 1.0 - dot( _safe_norm(R), _safe_norm(I) )
```

### C_IF (Informational-Physical) — cosine formulation (locked)
```python
i = _safe_norm(informational)
p = _safe_norm(physical)
size = max(len(i), len(p))
ia = zeros(size); ia[:len(i)] = i
pa = zeros(size); pa[:len(p)] = p
ia = _safe_norm(ia); pa = _safe_norm(pa)
C_IF = 1.0 - dot(ia, pa)
```
- Zero-pad shorter + re-norm ensures fair comparison when I (often ~3-4 from translator) vs F (fixed 4).
- Consistent math with C_NR / C_RI.
- **Rationale (historical)**: Prior KL (capped) gave C_IF=1.0 on perfect-scale cases and was asymmetric. Cosine + pad gives uniform semantics across NRIF. Lower = better I↔F alignment (resource efficiency proxy).
- Limitation: proxy metric (different layer semantics); documented.

**Docker-validated example** (perfect aligned ones(4) vs physical [1000,8,50,10]):
```
C_NR=0.0, C_RI=0.0, C_IF≈0.4667, C_total≈0.3556
```

### C_total (operational)
```python
C_total = (1/21) * C_NR + (4/21) * C_RI + (16/21) * C_IF
```
(Default weights matching the 1:4:16 layers proportions from v5.3 blueprint: w_NR=1/21, w_RI=4/21, w_IF=16/21.)

**Invariant**: lower C_total is always better (lower distance = higher coherence).

## 3. Thermodynamic Components

### Landauer Cost
```python
# physical
LANDAUER_MIN = k_B * T * ln(2)   # ~2.87e-21 J/bit at 300K
raw = decision_changes * LANDAUER_MIN

# normalized (default in kernel)
cost = lambda_landauer * decision_changes   # lambda=0.05 typical
```

> [!NOTE]
> **Audit and Scientific Validity Note (v5.3 Release)**: 
> - The Landauer cost implemented in this system is an **operational ANALOGY** designed to model and incentivize stability in logical decision making for multi-agent systems.
> - It **DOES NOT** represent a direct reading of thermal dissipation from physical processor transistors (silicon).
> - The logical changes variable (`decision_changes` / `bits_erased`) is an external input provided by the agent's environment, not a hardware metric captured via real-time physical instrumentation.


### Loss_4R2 (corrected formulation)
```python
coherence_penalty = alpha * (C_total ** 2)           # higher C → higher penalty
irreversibility_penalty = gamma * landauer_cost
L_4R2 = base_loss + coherence_penalty + irreversibility_penalty
```
**Key correction (2026-06-23)**: Previously used (1 - C_total)**2 which inverted the objective. Now monotonic with C_total.

## 4. Canonical Evidence (Docker selftest)

Command: `PYTHONPATH=core python -c 'from kernel_1240421 import CoherenceKernel; print(CoherenceKernel.selftest())'`

```
{
  "perfect_c": 0.3556,
  "perfect_loss": 0.5342,
  "bad_c": 0.5865,
  "bad_loss": 0.944,
  "loss_correct_direction": true
}
```

Loss direction test always passes: bad state produces strictly higher Loss_4R2.

Loss direction test always passes: bad state produces strictly higher Loss_4R2.

## 5. Bounds & Thresholds (from kernel tests + production)

- C_* ∈ [0, 2] (cosine distance after unit norm)
- C_total ∈ [0, 2] (convex)
- Excellent (pilot): C_total < 0.15
- Acceptable: < 0.35
- Concerning: > 0.5
- Gate / fuse trigger: > 0.65 (common)

All kernel tests (24) enforce:
- perfect alignment → C_NR/C_RI ≈ 0
- weight sum == 1.0
- Loss increases with C_total
- C_IF after pad is in [0,2]
- determinism on fixed input

## 6. Determinism & Reproducibility

- No np.random anywhere in core path.
- Fixed input vectors → bit-identical C_total / breakdown (within float64; harness uses 1e-12 tolerance on numeric fields).
- History list is append-only audit trail (reset optional).
- All fresh evidence runs (generate_fresh_evidence.py) and determinism_harness produce sealed SHA256 on numeric results.

## 7. Version & Precedence

v5.3 (cosine C_IF, SUM C_total, w_NR=1/21 w_RI=4/21 w_IF=16/21 default weights, Loss**2, LocalCanonicalMotor default).

This spec + core/kernel_1240421.py are the contract. Older KL descriptions exist only in annotated historical notes.

---

**End of authoritative spec.** Any code, test or doc claiming different formulas for C_IF / Loss direction / aggregation is stale.

## 8. Hardening and Core Extensions
**Kernel Separation (from LLMsuperEngine/kernel variants):**
- Added `measure_coherence_with_keys` for `total_coherence` (raw, can be <0) vs `coherence_score` (clamped to [0,1]).
- Separates raw mathematical analysis from operational enforcement. Tested and verified in all test harnesses.
- Impact: Prevents negative scores in production, enhancing audit traceability.

**4R2_FUSES (from dynamic pilot governance):**
- Concrete safety guards: VerificationGuard (blocks <0.9 on high), AsymmetryBreaker (vetoes EXISTENTIAL+PASSIVE risk actions), and PriorityBreaker (vetoes high execution ranks).
- Integrated across:
  - `fuses/fuses_4r2.py` (definition registry)
  - `operators/dual_runtime.py` (runtime dispatch and evaluation)
  - `fuse_config/generator.py` (dynamic generation from engine scores)
- Impact: Strict fail-closed execution, halting logical drift and protecting physical resources when coherence drops below critical thresholds.

**AGW / Dual / LLM Harness Integration:**
- Orchestration runtime defaults to real execution (`LocalCanonicalMotor`), showing correct coherence progression (C_total rises as misalignment increases).

---

## 9. Architectural Integration Insights (backup42final extraction)
**Kernel Coexistence Modes:**
- **Mode A (Static/Auditor)**: Fixed configurations, rigid safety fuses, representing strict external auditor constraints.
- **Mode B (Dynamic/Conviviente)**: Adaptive thresholds, dynamic context prioritization (`CCA`), enabling coexistence in shared agent environments.

**Belief and Coherence Coexistence:**
- Dynamic regimes adapt NRIF weights based on criticality. For example, high-criticality contexts dynamically shift weights to prioritize physical constraints ($w_{IF}$).
- The "Incoherency Tax" provides an economic narrative linking software failures and logical hallucinations directly to operational downtime, making C_total a proxy for physical execution cost.

---

**End of authoritative spec. All core definitions strictly locked.**
