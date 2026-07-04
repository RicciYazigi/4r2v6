# ADR-0004: Default to real motor (LocalCanonicalMotor), MockMotor only for isolated tests

**Date:** 2026-06-23  
**Status:** Accepted  

## Context
MasterOrchestrator and pilots previously defaulted to or easily fell back to MockMotor. For production-grade and audit, critical path must be real (either direct LocalCanonical or RealMotor HTTP).

## Decision
- MasterOrchestrator(use_real_motor=True) by default.
- LocalCanonicalMotor (direct import core/kernel_1240421) preferred for no-network real path.
- RealMotor (with CB "real_motor_http") for service-based.
- MockMotor explicitly removed from production paths; only instantiated in test-only pilots or unit tests with clear isolation.

## Consequences
- generate_fresh_evidence, brutal_end_to_end_runner, determinism_harness all exercise real path (verified in logs: motor_type=LocalCanonicalMotor, "No MockMotor in this execution path").
- Hardening tests cover CB on real path.
- Documentation (RUNBOOK, CANON_SPEC, ARCHITECTURE) updated.

**Impact on metrics:**
- Scores now come from actual kernel (cosine C_IF, correct Loss).
- No change to math; only to which implementation is exercised.

**Evidence:** Docker runs with "canonical-4.0-local-real", master.py comments, cleanup of Mock references, fresh evidence JSONs.

## Verification
- All E2E and fresh evidence runs confirm real motor.
- Production hardening verify exercises both local real and CB real paths.
- Grep and runtime logs in historial.
