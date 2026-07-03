# CONTRACT - 4R2 Coherence Engine API (Historical)

**HISTORICAL NOTE (2026-06-23):** This is the legacy v3.0 CONTRACT from earlier iterations.  
**Current authoritative version:** See `/docs/CONTRACT.md` (v4.0) in the rempacado root.  
It references CANON_SPEC.md, RUNBOOK.md, ADRs, real motor defaults (LocalCanonicalMotor), cosine C_IF, corrected Loss, etc.

Original content below preserved for reference.

---

Este documento define el contrato técnico oficial para la integración con el Motor 4R2.

**CONTRACT_VERSION**: 3.0 (Audit-Grade) (legacy)
**PORT**: 8000
**AUTH**: Bearer Token (Mocked)

## Endpoints Principales

### 1. Medición de Coherencia
`POST /api/coherence/measure`

**Request Body (JSON):**
```json
{
  "normative": [0.9, 0.8, 0.7],
  "representational": [0.85, 0.75, 0.65],
  "informational": [0.8, 0.7, 0.6],
  "physical": [1000.0, 8.0, 50.0, 10.0]
}
```
*   `physical` format: `[FLOPS, memory_GB, energy_Joules, latency_ms]`

**Response Body (JSON):**
```json
{
  "C_NR": 0.05,
  "C_RI": 0.08,
  "C_IF": 0.12,
  "C_total": 0.083,
  "timestamp": "2026-01-15T..."
}
```

### 2. Coste de Landauer
`POST /api/coherence/landauer`

**Request Body:**
```json
{
  "decision_changes": 5,
  "normalize": true
}
```

### 3. Función de Pérdida 4R2
`POST /api/coherence/loss-4r2`

**Request Body:**
```json
{
  "base_loss": 0.5,
  "coherence_total": 0.083,
  "decision_changes": 5,
  "alpha": 1.0,
  "gamma": 1.0
}
```

## Protocolos de Seguridad
- Se requiere cabecera `Authorization: Bearer <token>`.
- Todos los inputs son validados mediante esquemas Pydantic v2 internos del motor.
