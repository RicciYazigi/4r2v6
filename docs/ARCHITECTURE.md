# Architecture Overview — 4R2 + Antigravity Wings (v5.3)

**Golden Rule**: Governance (Antigravity Wings) evolves independently of the scientific motor. The core kernel is the pure, auditable, deterministic math layer.

## 1. Layered Structure (Mermaid)

```mermaid
graph TD
    Client[Client / Intake] --> Obs[Observation + Tomography]
    Obs --> Tomo[TomographyBuilder → Graph]
    Tomo --> Mario[MarioAgent<br/>forward strengths/redundancy]
    Tomo --> Luigi[LuigiAgent<br/>backward risks/no-return]
    Mario & Luigi --> Arbiter[DualArbiter<br/>consolidation + disagreement trace]
    Arbiter --> Notebook[NotebookClient]
    Arbiter & Notebook --> Translator[NumericTranslator v2<br/>→ NRIF vectors]
    Translator --> Evidence[NumericEvidence<br/>{N,R,I,F}]
    Evidence --> MotorBridge{Motor Bridge}
    MotorBridge -->|default| Local[LocalCanonicalMotor<br/>direct import core/kernel_1240421]
    MotorBridge -->|opt| Real[RealMotor<br/>HTTP to /api/coherence/measure]
    Local & Real --> Kernel[CoherenceKernel 1240421<br/>C_NR / C_RI / C_IF(cosine) / C_total / Loss]
    Kernel --> Scores[MotorOutput<br/>scores: {global=C_total, C_*, breakdown}]
    Scores --> Fuses[FuseSpec generation + DualRuntime]
    Fuses --> Decision[RuntimeDecision + ReasonDetail]
```

## 2. Core Components

**Governance (antigravity_wings/)**:
- observation/, tomography/
- dual_agents/{mario,luigi,arbiter}.py (real heuristics, no REDACTED)
- numeric/translator.py (v2, signal-carrying NRIF)
- orchestration/master.py (MasterOrchestrator)
  - defaults `use_real_motor=True`
  - prefers LocalCanonicalMotor (sys.path to core/)
  - RealMotor (circuit-breaker "real_motor_http")
  - resilience/circuit_breaker.py, rate limiting in API
- api/models.py (NumericEvidence, MotorOutput, ConsolidatedReport, etc.)

**Core (Single Source of Truth)**:
- `core/kernel_1240421.py`
  - LayerState + validation
  - CoherenceKernel (all C_ via 1-cos after _safe_norm + pad for C_IF)
  - compute_loss_4R2 with C_total**2
  - selftest(), history for audit
  - create_kernel()

## 3. Motor Paths (critical)

1. **LocalCanonicalMotor** (preferred, 100% real):
   - Direct Python import of kernel
   - No network, no mock in production path
   - Version string "canonical-5.2-local-real"

2. **RealMotor**:
   - HTTP POST to 4R2 FastAPI service
   - Protected by CircuitBreaker (name="real_motor_http")
   - Used when force_http_real or service available

3. **MockMotor**:
   - Exists only for isolated unit tests / pilots
   - Explicitly not defaulted after 2026-06-23 cleanup

MasterOrchestrator + generate_fresh_evidence always exercise real path (verified in Docker logs: motor_type in every JSON).

## 4. Key Contracts

- **Input**: NumericEvidence(client_id, normative, representational, informational, physical)
- **Output**: MotorOutput(scores={"global": C_total, "C_NR":.., "C_RI":.., "C_IF":..}, ...)
- **C_total invariant**: lower = better coherence
- **Error paths**: 401 (missing x-api-key), 429 (rate limit 60/min), CircuitOpenError, 410 for retired routes

## 5. Hardening (production)

- RateLimitMiddleware (per-client 60/min)
- CircuitBreaker on motor and analysis stages
- Structured logging with extra={client_id, trace_id, stage}
- Auth on /analyze (strict); /health permissive for tests
- All via clean Docker + verify_production_hardening.py

## 6. Reproducibility & Evidence

- Determinism harness (scripts/determinism_harness.py): fixed inputs → identical numeric SHA
- generate_fresh_evidence.py → evidence/fresh/*.json + SHA list
- Every Docker run uses PYTHONPATH=core:antigravity_wings + pinned python:3.13-slim
- Complete test suite: **60/60 tests passing** covering core kernel, security hardening, and dynamic governance runtime.

## 7. Decisions & Rationale (see CANON_SPEC + CHANGES.md)

- SUM not product for C_total (operational, matches all current evidence)
- C_IF cosine + pad (consistency + correct perfect-case behavior)
- Loss uses C_total**2 (directional correctness)
- Local first (no external dep for core math)

This architecture keeps math pure, auditable and reproducible while allowing rich governance around it.
