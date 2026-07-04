# ADR-0005: Weight Profile Policy — Balanced Default, Physics Profile Explicit

**Date:** 2026-07-03
**Status:** Accepted
**Supersedes:** ADR-0002 (extends, does not contradict)

## Context

During the v5.3.1 consolidation cycle, the `CoherenceKernel` constructor default was changed from the
ADR-0002-mandated equal weights (`w_NR=1/3, w_RI=1/3, w_IF=1/3`) to a physics-priority progression
derived from empirical fuzzing evidence over 2540 cases (`w_NR=1/21, w_RI=4/21, w_IF=16/21`).

While the empirical motivation is valid (the 1:4:16 ratio showed lower loss variance in Monte Carlo
simulation with p25=0.8016 and mean=0.9939 for random noise), the promotion of this ratio to the
**production default of the Hard-Gate** introduced a critical security vulnerability (P0):

**Ethical Blind-Spot Scenario:**
A transaction with total normative violation (`C_NR=1.0`) but optimal hardware execution
(`C_RI=0.1, C_IF=0.1`) scores:

```
C_total = (1/21)(1.0) + (4/21)(0.1) + (16/21)(0.1)
        = 0.0476 + 0.0190 + 0.0762
        = 0.1428  →  Zone GREEN (< 0.35)
```

This allows a critical normative breach to pass the Hard-Gate undetected — a production security fault.

## Decision

1. **Restore `CoherenceKernel.__init__` default to balanced weights** (`w_NR=1/3, w_RI=1/3, w_IF=1/3`)
   in full compliance with ADR-0002. This is the **mandatory default for all production Hard-Gate
   evaluations**.

2. **Register `1/21:4/21:16/21` as a named experimental profile** (`physics_priority_profile`) to be
   activated **only by explicit opt-in**. This profile is appropriate for hardware-throughput
   benchmarks and Monte Carlo simulation studies, never for security-critical gating.

3. **The `Regime` and `DomainKernel` subsystems are unaffected** — their context-dynamic weights
   (`0.25/0.25/0.50` for Regime default; domain-specific for DomainKernel) represent runtime
   contextual adjustments via CCA telemetry and remain valid. They are not defaults of the
   base kernel constructor.

## Named Weight Profiles (Registry)

| Profile Name              | w_NR  | w_RI  | w_IF  | Use Case                                      |
|:--------------------------|:------|:------|:------|:----------------------------------------------|
| `balanced` (**default**)  | 1/3   | 1/3   | 1/3   | Production Hard-Gate, security evaluation     |
| `physics_priority`        | 1/21  | 4/21  | 16/21 | Hardware throughput benchmarks, MC simulation |
| `normative_priority`      | 0.50  | 0.30  | 0.20  | High-ethics / compliance-critical domains     |
| `regime_default`          | 0.25  | 0.25  | 0.50  | CCA dynamic regime (runtime-adjusted)         |

## Consequences

- The balanced default guarantees that a `C_NR=1.0` violation always contributes >= 0.333 to
  `C_total`, making it impossible to reach Zone GREEN with a normative breach.
- The physics_priority profile is preserved for research use without loss of the empirical evidence.
- All 60 existing tests remain green (tests only assert `sum(weights)==1.0`, not specific values).
- CANON_SPEC.md, arXiv draft, and Funcionamiento completo.md must be updated to reflect this policy.

## Verification

```bash
# 1. Confirm default weights in constructor
python -c "from core.kernel_1240421 import CoherenceKernel; k = CoherenceKernel(); print(k.weights)"
# Expected: {'w_NR': 0.3333..., 'w_RI': 0.3333..., 'w_IF': 0.3333...}

# 2. Confirm Hard-Gate blocks normative breach
python -c "
import numpy as np
from core.kernel_1240421 import CoherenceKernel, LayerState
k = CoherenceKernel()
s = LayerState(np.array([1.,0.,0.,0.]), np.array([0.,1.,0.,0.]),
               np.array([0.9,0.9,0.,0.]), np.array([900.,8.,50.,10.]))
c, b = k.compute_coherence_total(s)
print(f'C_NR={b[\"C_NR\"]:.4f}, C_total={c:.4f}, blocked={c > 0.35}')
"
# Expected: C_NR~1.0, C_total~0.67, blocked=True

# 3. Full test suite
python -m pytest
```

## References

- ADR-0001: C_IF as cosine distance (unchanged)
- ADR-0002: C_total as weighted SUM (extended by this ADR)
- ADR-0003: Loss_4R2 quadratic penalty (unchanged)
- ADR-0004: Real motor as default (unchanged)
- KERNEL_VERSIONS_LEDGER.md: 5-variant comparison and vulnerability analysis
- fuzzing/summary.json: Empirical basis for physics_priority profile (2540 cases)

---

## Amendment (2026-07-04, ADR-0006)

The verification snippet above predates the angular-metric canon. On the
angular scale, orthogonal vectors give C_NR = 0.5 (not 1.0); the measured
values for the scenario are C_NR=0.5000, C_IF=0.2477 (dual-path, no silent
clip), C_total=0.3326 => Zone GRAY (0.28-0.39). The security guarantee is
preserved and strengthened: an antipodal normative breach contributes >= 1/3
to C_total (measured canonical case 0.6667 => RED/BLOCK). See ADR-0006 and
historiafable5.md.
