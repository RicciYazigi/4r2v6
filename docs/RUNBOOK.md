# 4R2 + Antigravity Wings — RUNBOOK (v5.3 - Meticulous Audit-Ready Edition)

**Workspace**: `C:\Users\USER\Documents\4R2 repo maestro jul2026`  
**Golden Rule**: Original in `Downloads/files (34)/4R2-MASTER-DELIVERY` is never touched.

All commands assume you are at the repository root.

**Meticulous Updates (v5.3 Release)**:
- Integrated insights from Kernel v5.x canons (PSC/MOSEF/CCA for dynamic LLM/agent coexistence), weights $w_{NR}=1/21$, $w_{RI}=4/21$, $w_{IF}=16/21$, real hashes, and dynamic layers.
- All changes preserve core math (cosine C_IF, SUM C_total, sq Loss).
- Focus on audit-readiness: real hashes, calibration, hermetic extensions, dynamic layers.
- See CANON_SPEC.md for full mapping.

## 1. Environment

- Python 3.11+ with numpy, pydantic, httpx, fastapi, google-generativeai (use Docker for reproducibility)
- Docker (required for every evidence / validation run)

## 2. Quick Docker Environment (recommended for all numeric work)

```bash
docker run --rm -v "$(pwd):/workspace" -w /workspace python:3.11-slim \
  bash -c 'pip install -q numpy pydantic httpx requests fastapi && \
           PYTHONPATH=core:antigravity_wings python -c "from kernel_1240421 import CoherenceKernel; print(CoherenceKernel.selftest())"'
```

## 3. Kernel Self-test & Manual Check

```bash
PYTHONPATH=core python -c '
from kernel_1240421 import CoherenceKernel, LayerState
import numpy as np
k = CoherenceKernel()
print(k.selftest())
perfect = LayerState(np.ones(4), np.ones(4), np.ones(4), np.array([1000.,8.,50.,10.]))
c, br = k.compute_coherence_total(perfect)
print("C_total=", round(c,6), "breakdown=", {k:round(v,6) for k,v in br.items() if isinstance(v,(int,float))})
'
```

Expected (approx): perfect_c 0.3556, loss direction true.

## 4. Full Test Suites (Docker)

Kernel (24 tests):
```bash
docker run --rm -v "$(pwd):/workspace" -w /workspace python:3.11-slim bash -c '
pip install -q numpy pytest
PYTHONPATH=core:4R2-MASTER-DELIVERY/tests python -m pytest 4R2-MASTER-DELIVERY/tests/test_kernel_1240421.py -q --tb=line
'
```

AGW orchestration tests (prior baseline 17/17; run specific):
```bash
docker run ... PYTHONPATH=antigravity_wings python -m pytest antigravity_wings/tests -q --tb=no || echo "(use exact test paths if collection issues on logs)"
```

## 5. Brutal End-to-End Real Pipeline (no mocks)

```bash
docker run --rm -v "$(pwd):/workspace" -w /workspace python:3.11-slim bash -c '
pip install -q numpy pydantic httpx requests fastapi
PYTHONPATH=core:antigravity_wings python scripts/brutal_end_to_end_runner.py
'
```

Verifies:
- Motor = LocalCanonicalMotor / canonical-4.0-local-real
- Real Mario/Luigi/Arbiter/Translator output
- Real C_total + breakdown
- "No MockMotor in this execution path"

## 6. Fresh Evidence Pack (brutal_fresh_evidence)

```bash
docker run --rm -v "$(pwd):/workspace" -w /workspace python:3.11-slim bash -c '
pip install -q numpy pydantic httpx requests fastapi
PYTHONPATH=core:antigravity_wings python generate_fresh_evidence.py
'
```

Produces `evidence/fresh/*.json` (fuzz, soak, ablation, parity) + prints SHAs.
Update `evidence_index_fresh.json` after (or re-run the index builder).

## 7. Determinism Harness

```bash
PYTHONPATH=core:antigravity_wings python scripts/determinism_harness.py
```

- Runs kernel + full pipeline multiple times
- SHA256 on numeric-only results (timestamps excluded)
- Cross-invocation and intra-loop proof

## 8. Production Hardening Verification

```bash
docker run ... PYTHONPATH=antigravity_wings python scripts/verify_production_hardening.py
```

Checks rate-limit 429, CB open on repeated failures, auth 401, structured logs.

## 9. Evidence Sealing & Hashes

After any generation run:
- Compute `sha256sum evidence/fresh/*.json`
- Record in historial + evidence_index
- Commit the JSONs + updated index (never alter prior sealed packs)

## 10. Common PYTHONPATHs

- Core only: `PYTHONPATH=core`
- Full AGW + core: `PYTHONPATH=core:antigravity_wings`
- With legacy tests: `PYTHONPATH=core:antigravity_wings:4R2-MASTER-DELIVERY/tests`

## 11. Important Notes

- Always run evidence / harness / brutal via Docker for audit-grade reproducibility.
- Default motor is real (LocalCanonical). Mocks are test-only.
- C_IF is cosine (see CANON_SPEC.md). Old KL refs are annotated HISTÓRICO.
- Loss_4R2 uses C_total**2 (higher C = higher penalty).
- All changes to math or core must update CANON_SPEC first, then tests + evidence.

## 12. Troubleshooting

- Import errors: check PYTHONPATH and that you are at rempacado root.
- "No module": install the listed packages inside the same docker -c.
- Collection noise on AGW tests: often .txt log artifacts; run specific test files.
- HTTP motor: start the 4R2 service separately (docker-compose in 4R2-MASTER-DELIVERY/systems/basic) and use force_http_real=True.

**This RUNBOOK is executable truth.** Update it when new verification scripts or Docker patterns are added.
