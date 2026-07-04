# ANTIGRAVITY WINGS: FLAT CONTEXT STRUCTURE (2026-01-10)
> **STATUS:** AUDIT-GRADE CERTIFIED / CANON v1.0
> **VERSION:** 1.0.0 (FINAL FREEZE)
> **CONTEXT:** Consolidated source of truth for NotebookLM analysis.

---

## SECTION 1: SYSTEM VISIBILITY & STRATEGY

### 1.1. EXPLICACIÓN TÉCNICA (Architecture & Roadmap)
*(Source: `docs/EXPLICACION_RICCI_2026-01-08.md`)*

**Arquitectura Lógica:** Orquestación Centralizada con Componentes Desacoplados.
**Data Pipeline:**
1.  **Ingesta:** API Layer (`POST /analyze`). Protocolo HTTPS. Salida: `DecisionContract` estricto.
2.  **Orquestación:** `MasterOrchestrator` controla flujo sincrónico y manejo de fallos (FALLBACK).
3.  **Observación:** `SystemSnapshot` estandariza inputs heterogéneos.
4.  **Inferencia:** `Motor Bridge` (actualmente Mock, futuro Gemini). Protegido por `CircuitBreaker`.
5.  **Validación Dual:** Mario (Light - Negocio) vs Luigi (Shadow - Riesgo) arbitrados por `DualRuntimeOperator`.
6.  **Auditoría:** `Evidence Packer` genera `evidence_bundle` con `SHA-256`.

**Roadmap:**
1.  **Core Validado (DONE):** API, Manejo Errores, Docker, Mocks.
2.  **Conexión Real (PENDING):** `gemini_adapter.py`, `RealDataSource`.
3.  **Interfaz (PENDING):** Frontend App.

### 1.2. PILOTS DESIGN (Operational Strategy)
*(Source: `docs/PILOTS_DESIGN.md`)*

**Piloto Seguros ("Claims Fast-Track"):**
- **Reto:** Proceso asíncrono, evidencia multimedia.
- **Config:** `DataSource` imágenes + OCR. `CircuitBreaker` 30s.
- **Fusibles:** Hard Stop si póliza vencida. Escalate si pérdida total.
- **Agentes:** Luz valida descripción vs daño. Sombra busca metadatos inconsistentes.

**(Otros pilotos definidos: Banca "Transaction Guardian", Salud "Remote Triage")**

---

## SECTION 2: IMPLEMENTATION STATUS

### 2.1. EXECUTION REPORT (Insurance Pilot)
*(Source: `docs/REPORTE_IMPLEMENTACION_PILOTO_SEGUROS_2026-01-08.md`)*

**Estado:** VERIFICADO.
**Logros:**
- Implementado `DecisionContract` estricto (Pydantic v2).
- Creada infraestructura `pilots/insurance/` (Mocks, Launcher, Verify Script).
- Refactorizado `server.py` y `settings.py` para soporte dinámico.
- **Smoke Test Exitoso:** Validación 1:1 de contrato y existencia de Evidence Bundle.
- **Git Push:** Código asegurado en repositorio remoto.

---

## SECTION 3: CORE CODE & CONTRACTS

### 3.1. DECISION CONTRACT (The "Law")
*(Source: `antigravity_wings/api/decision_schema.py`)*

```python
class DecisionEnum(str, Enum):
    APPROVE = "approve"
    DEGRADE = "degrade"
    ESCALATE = "escalate"
    STOP = "stop"

class DecisionContract(BaseModel):
    trace_id: str
    decision: DecisionEnum
    confidence: float
    primary_reason: str
    secondary_factors: List[str]
    fusibles_triggered: List[str]
    agent_votes: Optional[AgentVotes]
    pilot_id: str
    policy_version: str
```

### 3.2. MASTER ORCHESTRATOR (The "Brain")
*(Source: `antigravity_wings/orchestration/master.py`)*

**Responsabilidad:** Ejecutar el pipeline completo (Cold -> Science -> Warm -> Audit).
**Garantías:** Siempre intenta empaquetar evidencia. Fallback robusto en caso de error.
**Fases:**
- `_run_observation_phase`: Build snapshot.
- `_run_notebook_and_numeric_phase`: Generate summary & vector.
- `_run_motor_phase`: Call Motor via CircuitBreaker.
- `EvidencePacker`: Persist & Hash.

### 3.3. API SERVER (The "Interface")
*(Source: `antigravity_wings/api/server.py`)*

- Endpoint: `POST /analyze/{client_id}`
- Response Model: `DecisionContract`
- Logic: Invokes `MasterOrchestrator`, maps response to Contract.

---

## SECTION 4: ARCHITECTURAL BASELINE

### 4.1. RADIOGRAFÍA 3D (System Map)
*(Source: `docs/RADIOGRAFIA_FINAL_3D.md`)*

**Capas:**
1.  **Web:** Launcher, API, Cockpit.
2.  **Orquestación:** Master, SessionManager.
3.  **Observación:** Observer, Registry, Tomography.
4.  **IA:** NumericTranslator, Kernel (Entropy/Coherence).
5.  **Ejecución:** MotorLoader, CircuitBreaker, Pilot.
6.  **Telemetría:** HealthMonitor, EvidencePacker.

**Flow:** Entrada -> Seguridad -> Persistencia -> Observación -> Tomografía -> Traducción -> Ciencia -> Motor -> Decisión Dual -> Sellado.

---

## SECTION 5: PILOT SPECIFICS (INSURANCE)

### 5.1. MOCKS (The "Simulation")
*(Source: `pilots/insurance/mocks.py`)*

- `InsuranceClaimSource`: Generates synthetic claim data (images, OCR, story).
- `ClaimsVisionMotor`: Simulates CV model. Returns risk score based on metadata consistency and narrative match.

### 5.2. VERIFICATION SCRIPT (The "Proof")
*(Source: `pilots/insurance/verify_pilot.py`)*

- Uses `FastAPI TestClient`.
- Validates response strictly against `DecisionContract` (Route A).
- Checks existence of Evidence Bundle files (`decision.json`, `HASH.txt`).
- **Result:** SUCCESS on 2026-01-08.
