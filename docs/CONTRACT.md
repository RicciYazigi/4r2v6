# CONTRACT - 4R2 Coherence Engine (v4.0 Polished)

**CONTRACT_VERSION**: 4.0 (Polished, Audit-Grade)  
**Date**: 2026-06-23  
**Workspace**: Grok4r2 rempacado (clean copy)  
**See also**: docs/CANON_SPEC.md (authoritative math), docs/RUNBOOK.md (executable commands), docs/ADRs/, core/kernel_1240421.py

## Core Principles
- Lower C_total is always better.
- All critical paths use real computation (LocalCanonicalMotor default or RealMotor).
- Deterministic given fixed inputs.
- Landauer and Loss_4R2 use corrected formulas (C_total**2 penalty).
- Evidence is sealed with SHA256.

## Input Model (NumericEvidence)
```json
{
  "client_id": "example",
  "normative": [0.9, 0.8, 0.7, 0.6],
  "representational": [0.85, 0.75, 0.65, 0.55],
  "informational": [0.8, 0.7, 0.6, 0.5],
  "physical": [1000.0, 8.0, 50.0, 10.0]
}
```
Physical is always 4D: [FLOPS, mem_GB, energy_J, latency_ms].

## Primary Operation: Measure Coherence
**Local (preferred):** Direct call via MasterOrchestrator(use_real_motor=True) → LocalCanonicalMotor → kernel.

**Remote (alternative):** RealMotor HTTP POST to /api/coherence/measure (protected by CB).

**Response scores** (from kernel):
```json
{
  "global": 0.1670,   // C_total
  "C_NR": 0.0458,
  "C_RI": 0.0631,
  "C_IF": 0.3921,
  "motor_type": "LocalCanonicalMotor",
  "version": "canonical-4.0-local-real"
}
```

C_IF uses cosine (see ADR-0001).

## Landauer & Loss
- Landauer: lambda_landauer * decision_changes (normalized) or raw physical.
- Loss_4R2 = base + α * C_total**2 + γ * landauer (see ADR-0003).

## Defaults & Hardening
- Default motor: real (LocalCanonicalMotor).
- Rate limit: 60 req / 60s per client.
- Circuit breakers on real motor paths.
- Auth: x-api-key required on sensitive endpoints.

## Reproducibility
Use determinism_harness.py and generate_fresh_evidence.py (always via Docker). Sealed SHAs recorded in evidence/fresh/ and historial.

## Versioning
This CONTRACT v4.0 supersedes v3.0 (old KL, mocked auth notes, etc.). See ADRs and CANON_SPEC for decision history. Legacy CONTRACT inside 4R2-MASTER-DELIVERY/docs/ is historical.

**For execution details:** See docs/RUNBOOK.md.

## Fortificaciones 2026-06-27 (from backup42final.zip + prior search)

**From backup42final (high-value audits/kernels):**
- Kernel v5.x: Adds PSC (Protocolo Situación y Convivencia) for dynamic mode (LLM/agents), MOSEF enforcement, CCA observer. Maps to our dual runtime + 4R2_FUSES (e.g., Gate E = veto in AsymmetryBreaker).
- Brutal Audit V40: "Impuesto a la Incoherencia" as value prop; NRIF weights (F=16 high); gaps (calibration via our harness, hermetic FuseSpec via 4R2_FUSES extension, real hashes via seals).
- Other: CCA Design, MOSEF protocols, SurfSense/Obsidian 4R2 analysis – enrich AGW with "clinical observer" for better C_total in coexistence.

**Integration:**
- Updated CANON_SPEC, harness (Gemini + pilots), fuse_config, dual_runtime, pyproject.
- Pruebas: Docker confirmed C_total control, guards, real pipeline.

See historial for full excerpts/rationale. Strengthens contract with dynamic layer without altering core math (immutable kernel, cosine C_IF).

