# antigravity_wings — OPERATION_MANUAL.md

> Versión: 0.1  
> Público: Equipo técnico, auditores, operadores de riesgo / confiabilidad.  
> Alcance: Operación del exoesqueleto antigravity_wings alrededor de un Motor (Black Box).

---

## Índice

1. [Visión General](#visión-general)
2. [Cómo integrar un nuevo cliente](#1-cómo-integrar-un-nuevo-cliente)
   - 1.1. Preparar entorno
   - 1.2. Integración vía API (modo servicio)
   - 1.3. Integración directa en Python (modo librería)
3. [Cómo crear nuevos DataSource](#2-cómo-crear-datasource-nuevos)
   - 2.1. Interfaz `DataSource`
   - 2.2. Ejemplos típicos
   - 2.3. Registro en `SourceRegistry`
4. [Cómo conectar un nuevo Motor](#3-cómo-conectar-un-nuevo-motor)
   - 3.1. Implementar `MotorInterface`
   - 3.2. Exponerlo vía `MOTOR_PATH` / `MOTOR_CLASS`
   - 3.3. Guardrails y Circuit Breaker (qué hace el framework por ti)
   **NOTA HISTÓRICA / ACTUALIZADO 2026-06-23**: Default es real (LocalCanonical o RealMotor). Mock solo para tests. Ver core/kernel_1240421.py y CANON_SPEC.
5. [Cómo interpretar el Cockpit](#4-cómo-interpretar-las-secciones-del-cockpit)
   - 4.1. Salud del Sistema
   - 4.2. Monitor de Decisiones
   - 4.3. Explorador de Auditoría
6. [Cómo responder a eventos críticos](#5-cómo-responder-a-eventos-críticos)
   - 5.1. Circuito OPEN (Motor / Notebook)
   - 5.2. Guardrail activado
   - 5.3. Alto porcentaje de fallbacks
   - 5.4. Otros eventos relevantes
7. [Buenas prácticas operativas](#6-buenas-prácticas-operativas)

---

## Visión General

`antigravity_wings` es un **exoesqueleto de coherencia, auditoría y mitigación de riesgo** que se monta alrededor de un **Motor científico** tratado como *caja negra*.

Capacidades clave:

- **Observación multi-fuente** del sistema del cliente (logs, APIs, archivos).
- **Tomografía** de decisiones y flujos (grafo estructural).
- **Análisis dual** (Luz/Sombra) y consolidación de reportes.
- **Workspace de Notebook** (Markdown optimizado para NotebookLM u otro cuaderno).
- **Traducción determinista** de informes → evidencia numérica.
- **Motor (Black Box)** protegido por:
  - Guardrails (NaN/Inf, evidencia corrupta),
  - Circuit Breaker (latencia excesiva, fallos repetidos).
- **Fusibles digitales** (FuseSpecs) + **perfil congelado por cliente** (`ClientProfile`).
- **Operación en caliente** con `DualRuntimeOperator` (GO/DEGRADE/STOP/ESCALATE).
- **Auditoría sellada** (decision.json + profile.json + snapshot.json + HASH.txt).
- **Telemetría en vivo** en `system_status.json` + **Cockpit web**.

---

## 1. Cómo integrar un nuevo cliente

Hay dos formas principales de integrar un cliente:

- **Modo Servicio (recomendado)**: llamando a la API HTTP (`/analyze`, `/status`, `/evidence`).
- **Modo Librería**: instanciando las clases desde Python y usando el `MasterOrchestrator` directamente.

### 1.1. Preparar entorno

Variables de entorno recomendadas:

```bash
export AGW_ENV=prod              # o dev, stage
export AGW_RUNTIME_ROOT=/var/antigravity_wings/runtime_data
export AGW_API_KEY=supersecret   # clave para proteger la API
export MOTOR_PATH=/path/to/my_motor_impl.py
export MOTOR_CLASS=MyRealMotor
```

Luego:

```bash
pip install fastapi uvicorn
python launcher.py
# Servicio en http://localhost:8000
```

### 1.2. Integración vía API (modo servicio)

#### 1.2.1. Endpoint: POST /analyze/{client_id}

- **Objetivo**: Ejecutar TODO el pipeline para una decisión runtime.
- **Request**:

```http
POST /analyze/bank_xyz
X-API-Key: supersecret
Content-Type: application/json

{
  "node_id": "decision_1",
  "payload": {
    "amount": 5000,
    "currency": "USD",
    "customer_segment": "gold"
  },
  "context": {
    "channel": "web",
    "session_id": "abc123"
  }
}
```

- **Respuesta** (ejemplo):

```json
{
  "client_id": "bank_xyz",
  "node_id": "decision_1",
  "trace_id": "bank_xyz_1a2b3c4d",
  "decision": "go",
  "reasons": [
    "light: all fuses pass or warn",
    "shadow: no critical issues"
  ],
  "state_color": "green",
  "cost_level": "low",
  "light_decision": "go",
  "shadow_decision": "go"
}
```

- Esta llamada:
  - Crea una **sesión aislada** para `bank_xyz`.
  - Ejecuta todo el pipeline.
  - Genera un paquete de evidencia en disco.
  - Actualiza `system_status.json`.

#### 1.2.2. Endpoint: GET /status

- **Objetivo**: Telemetría global para Cockpit.
- **Request**:

```http
GET /status
X-API-Key: supersecret
```

- **Respuesta** (ejemplo resumido):

```json
{
  "timestamp_utc": "2025-01-06T12:30:00Z",
  "steps": {
    "motor": {
      "call_count": 10,
      "error_count": 2,
      "avg_latency_ms": 120.5,
      "last_latency_ms": 95.3,
      "last_error": "CircuitOpenError(...)"
    },
    "runtime_operator": { ... }
  },
  "circuits": {
    "motor": {
      "name": "motor",
      "state": "closed",
      "failure_count": 0,
      "last_failure_time": null,
      "last_latency_ms": 95.3,
      "open_since": null,
      "safe_mode": false
    }
  },
  "decisions": {
    "total_decisions": 25,
    "total_fallbacks": 3
  },
  "decisions_breakdown": {
    "go": 18,
    "degrade": 2,
    "stop": 1,
    "escalate": 4
  }
}
```

#### 1.2.3. Endpoint: GET /evidence/{client_id}/{trace_id}

- **Objetivo**: Navegar y descargar paquetes de auditoría.
- **Búsqueda**:

```http
GET /evidence/bank_xyz/bank_xyz_1a2b3c4d
X-API-Key: supersecret
```

- **Respuesta**:

```json
{
  "client_id": "bank_xyz",
  "trace_id": "bank_xyz_1a2b3c4d",
  "packages": [
    {
      "session_id": "bank_xyz_20250106T120000Z_a1b2c3d4",
      "package_name": "bank_xyz_bank_xyz_1a2b3c4d_20250106T120100Z",
      "path": "/var/antigravity_wings/.../evidence/bank_xyz_bank_xyz_1a2b3c4d_20250106T120100Z",
      "files": [
        "decision.json",
        "profile.json",
        "snapshot.json",
        "HASH.txt"
      ]
    }
  ]
}
```

- **Descarga de archivo**:

```http
GET /evidence/bank_xyz/bank_xyz_1a2b3c4d?package=bank_xyz_bank_xyz_1a2b3c4d_20250106T120100Z&file=decision.json
X-API-Key: supersecret
```

---

### 1.3. Integración directa en Python (modo librería)

Si quieres usar el orquestador directamente:

```python
from pathlib import Path
from antigravity_wings.orchestration.session_manager import SessionManager
from antigravity_wings.api.telemetry import HealthMonitor
from antigravity_wings.motor_bridge.loader import MotorLoader
from antigravity_wings.resilience.circuit_breaker import CircuitBreakerConfig
from antigravity_wings.fuse_config.generator import FuseConfigGenerator
from antigravity_wings.orchestration.master import MasterOrchestrator
from antigravity_wings.observation.registry import SourceRegistry
from antigravity_wings.api.models import RuntimeDecisionRequest

root = Path("/var/antigravity_wings/runtime_data")
session_mgr = SessionManager(root / "sessions")
health = HealthMonitor(root / "system_status.json")
motor_loader = MotorLoader()
circuit_cfg = CircuitBreakerConfig()
fuse_gen = FuseConfigGenerator()

orchestrator = MasterOrchestrator(
    session_manager=session_mgr,
    health_monitor=health,
    motor_loader=motor_loader,
    circuit_config=circuit_cfg,
    fuse_generator=fuse_gen,
)

registry = SourceRegistry()
# registry.register(...) → tus DataSource reales

req = RuntimeDecisionRequest(
    client_id="bank_xyz",
    node_id="decision_1",
    trace_id="manual_trace_001",
    payload={"amount": 5000, "currency": "USD"},
    context={"channel": "batch_job"},
)

session, decision, evidence_dir = orchestrator.run_full_pipeline(
    client_id="bank_xyz",
    runtime_request=req,
    source_registry=registry,
)
```

---

## 2. Cómo crear DataSource nuevos

### 2.1. Interfaz `DataSource`

Ubicado en `antigravity_wings/observation/registry.py`:

```python
class DataSource(ABC):
    @property
    @abstractmethod
    def name(self) -> str: ...

    @abstractmethod
    def collect(self) -> List[Dict[str, Any]]:
        """Devuelve una lista de dicts con datos genéricos."""
```

Reglas:

- `name`: único en el registro.
- `collect()`:
  - No lanza excepciones no controladas (o se capturan internamente).
  - Retorna `List[Dict[str, Any]]`.  
    Cada dict puede tener lo que necesites; el Observer solo añade `source_name`.

### 2.2. Ejemplos típicos

#### 2.2.1. Logs de archivo

```python
from antigravity_wings.observation.registry import DataSource
from typing import List, Dict, Any
from pathlib import Path
import json

class FileLogSource(DataSource):
    def __init__(self, name: str, path: Path):
        self._name = name
        self._path = path

    @property
    def name(self) -> str:
        return self._name

    def collect(self) -> List[Dict[str, Any]]:
        if not self._path.is_file():
            return []
        records: List[Dict[str, Any]] = []
        with self._path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                    records.append(rec)
                except json.JSONDecodeError:
                    records.append({"raw_line": line})
        return records
```

#### 2.2.2. Fuente HTTP (API externa)

```python
import requests
from antigravity_wings.observation.registry import DataSource

class HttpApiSource(DataSource):
    def __init__(self, name: str, url: str, timeout: float = 5.0):
        self._name = name
        self._url = url
        self._timeout = timeout

    @property
    def name(self) -> str:
        return self._name

    def collect(self) -> List[Dict[str, Any]]:
        resp = requests.get(self._url, timeout=self._timeout)
        resp.raise_for_status()
        data = resp.json()
        if isinstance(data, list):
            return [d for d in data if isinstance(d, dict)]
        elif isinstance(data, dict):
            return [data]
        return []
```

### 2.3. Registro en `SourceRegistry`

```python
from antigravity_wings.observation.registry import SourceRegistry
from pathlib import Path

registry = SourceRegistry()
registry.register(FileLogSource("app_logs", Path("/var/log/myapp.log")))
registry.register(HttpApiSource("risk_signals", "https://api.example.com/risk_signals"))
```

Este `registry` se pasa al `MasterOrchestrator.run_full_pipeline(...)`.

---

## 3. Cómo conectar un nuevo Motor

### 3.1. Implementar `MotorInterface`

`MotorInterface` está en `motor_bridge/interface.py`:

```python
class MotorInterface(ABC):
    @abstractmethod
    def evaluate(self, evidence: NumericEvidence) -> MotorOutput:
        ...
```

Ejemplo (en un archivo externo, p.ej. `/opt/antigravity/my_motor_impl.py`):

```python
# my_motor_impl.py
from antigravity_wings.motor_bridge.interface import MotorInterface
from antigravity_wings.api.models import NumericEvidence, MotorOutput

class MyRealMotor(MotorInterface):
    def __init__(self):
        # Cargar modelos, configuraciones, etc.
        ...

    def evaluate(self, evidence: NumericEvidence) -> MotorOutput:
        # Tu ciencia interna (no se documenta aquí).
        score = 0.7  # placeholder
        return MotorOutput(
            client_id=evidence.client_id,
            scores={"global": score},
            ranges={},
            config_blob={"impl": "MyRealMotor"}
        )
```

### 3.2. Exponerlo vía `MOTOR_PATH` / `MOTOR_CLASS`

En el entorno donde corres `launcher.py`:

```bash
export MOTOR_PATH=/opt/antigravity/my_motor_impl.py
export MOTOR_CLASS=MyRealMotor
python launcher.py
```

`MotorLoader`:

- Carga el módulo `my_motor_impl.py`.
- Encuentra la subclase de `MotorInterface`.
- La instancia.
- `MasterOrchestrator` la envuelve con:
  - Guardrails (NaN/Inf),
  - CircuitBreaker.

### 3.3. Qué hacen los Guardrails y Circuit Breaker

- **Guardrails** (`GuardedMotor`):
  - Revisa `NumericEvidence.feature_vector`:
    - Si hay NaN/Inf → NO llama a tu Motor.
    - Registra el incidente.
    - Devuelve `MotorOutput` de fallback con:
      - `guardrail_triggered = True`,
      - `suggested_runtime_decision = "escalate"`.

- **CircuitBreaker**:
  - Mide latencia y fallos de `motor.evaluate`.
  - Si:
    - se supera `failure_threshold` (N fallos seguidos), o
    - se supera `max_latency_sec` (por ejemplo 5s),
  - Abre el circuito:
    - futuras llamadas fallan rápido con `CircuitOpenError`.
    - se devuelve un `MotorOutput` de fallback.
  - Después de `recovery_timeout_sec`, intenta reabrir (HALF_OPEN).

---

## 4. Cómo interpretar las secciones del Cockpit

El Cockpit se sirve en:

- `http://localhost:8000/cockpit`

Contiene 3 bloques principales.

### 4.1. Salud del Sistema

**Panel “Latencia por Paso”** (tabla):

- Columnas:
  - **Paso**: nombre del componente (`observation`, `tomography`, `light`, `shadow`, `arbiter`, `notebook`, `numeric`, `motor`, `runtime_operator`).
  - **Llamadas**: cuántas veces se ha ejecutado ese paso.
  - **Errores**: número de ejecuciones con excepción.
  - **Latencia Prom. (ms)**: media de tiempo por llamada en milisegundos.
  - **Última Latencia (ms)**: tiempo de la última llamada.

Lectura típica:

- Latencias bajas/estables → sistema fluido.
- Errores crecientes en un paso (ej. `notebook`) → problema con ese componente.
- Latencia alta en `motor` → revisar CircuitBreaker and Motor.

**Panel “Estado de Circuitos”**:

- Cada circuito (ej. `motor`) aparece como un “chip” con:
  - Nombre.
  - Estado: 
    - **CLOSED** (verde): tráfico normal.
    - **HALF_OPEN** (amarillo): fase de prueba tras OPEN.
    - **OPEN** (rojo): cortado, en modo Safe.

Interpretación:

- Estado **OPEN** sostenido:
  - Motor no es confiable o está saturado.
  - Se están devolviendo fallbacks (ver sección decisiones).

---

### 4.2. Monitor de Decisiones

**Resumen**:

- **Total decisiones**: número total de decisiones runtime evaluadas.
- **Total fallbacks**: decisiones marcadas como uso de fallback (guardrails, circuit breaker, errores globales).
- **Fallback %**: `(fallbacks / total) * 100`.

**Por tipo**:

- Contadores de:
  - GO
  - DEGRADE
  - STOP
  - ESCALATE

Interpretación:

- GO alto, fallbacks bajos → sistema saludable.
- ESCALATE alto, fallbacks altos → mucho caso raro o problemas en fuentes/Motor.
- STOP alto → configuración muy estricta o muchos errores críticos.

---

### 4.3. Explorador de Auditoría

Formulario:

- **Client ID**: ID del cliente (ej. `bank_xyz`).
- **Trace ID**: ID de la traza de decisión (lo devuelve `/analyze`).

Resultados:

- Lista de paquetes de evidencia:
  - **Session**: sesión donde se generó.
  - **Package**: nombre del directorio de evidencia.
  - **Files**:
    - `decision.json`: decisión runtime (GO/STOP/..., razones).
    - `profile.json`: ClientProfile completo usado (tomografía, Luz/Sombra, MotorOutput, fusibles).
    - `snapshot.json`: datos observados en fase Cold.
    - `HASH.txt`: hashes SHA-256 de los 3 JSON (sello de integridad).

Auditoría:

- Verificar `HASH.txt`:
  - Recalcular SHA-256 de cada JSON.
  - Comparar con lo registrado.
  - Si coinciden → integridad preservada.

---

## 5. Cómo responder a eventos críticos

### 5.1. Circuito OPEN (Motor / Notebook)

**Detección**:

- En `/status` → `circuits.motor.state == "open"`.
- En Cockpit → chip rojo “OPEN”.

**Causas típicas**:

- Motor:
  - Tiempos de respuesta elevados (más allá de `max_latency_sec`).
  - Fallos repetidos de `evaluate`.

**Acción recomendada**:

1. **Ver logs del Motor**:
   - Logs internos del Motor (tuyos).
   - Logs del GuardedMotor: mira `guardrail_reason` y `motor_error`.

2. **Revisar configuración de CircuitBreaker**:
   - `failure_threshold` demasiado bajo para tu realidad.
   - `max_latency_sec` muy agresivo.

3. **Ver Fallbacks en Cockpit**:
   - ¿Aumentan los fallbacks?
   - ¿Las decisiones finales son mayormente ESCALATE?

4. **Acción operativa**:
   - Si OPEN es transitorio (se cierra solo) → puede ser un pico.
   - Si permanece OPEN:
     - considerar desactivar llamadas al Motor temporalmente,
     - investigar causa raíz,
     - quizá pasar a modo “Book Your Service” hasta estabilizar.

---

### 5.2. Guardrail activado

**Detección**:

- En `MotorOutput.config_blob`:
  - `guardrail_triggered = True`.
- En evidencia:
  - `numeric_evidence.metadata["corrupt"] == True` o similar.
- En logs:
  - Mensajes de `GuardrailViolationError` (NaN/Inf).

**Causas típicas**:

- Evidencia numérica inválida:
  - Features con NaN/Inf.
  - Errores en `NumericTranslator`.

**Acción recomendada**:

1. **Revisar NumericTranslator**:
   - ¿Hay divisiones por cero?
   - ¿Hay transformaciones que produzcan NaN/Inf?

2. **Ver Snapshot y Tomografía**:
   - ¿La entrada de datos del cliente cambió?
   - ¿Entraron campos que no se esperaban?

3. **Corregir pipeline de features**:
   - Añadir normalización.
   - Manejar explícitamente valores faltantes o extremos.

4. **Auditoría**:
   - Analizar varios `decision.json` y `profile.json` afectados.
   - Documentar qué datos estaban causando el fallo.

---

### 5.3. Alto porcentaje de fallbacks

**Detección**:

- En `/status`:
  - `decisions.total_fallbacks / decisions.total_decisions` elevado.
- En Cockpit:
  - `Fallback %` alto (ej. > 10–20%, según política interna).

**Causas típicas**:

- Cambios en el sistema del cliente sin re‑tomografía.
- Problemas con fuentes de datos (APIs caídas, logs incompletos).
- Problemas en NotebookLM (si se usa, p.ej. API down).
- Problemas en Motor (como circuito OPEN o errores frecuentes).

**Acción recomendada**:

1. **Clasificar los fallbacks**:
   - ¿Provienen de:
     - Guardrails (evidencia corrupta),
     - CircuitBreaker (Motor),
     - Otros errores globales?

2. **Rehacer Tomografía**:
   - Ejecutar nuevamente el pipeline Cold (solo observación + tomografía + Luz/Sombra + Notebook + numeric).
   - Ver si el grafo cambió (nuevos nodos críticos).

3. **Revisar integración con el cliente**:
   - ¿Han cambiado flujos?
   - ¿Han introducido nuevos endpoints / servicios?

4. **Política interna**:
   - Documentar umbrales de tolerancia:
     - Ej.: Fallback% > 5% → alerta.
     - Fallback% > 15% → revisión obligatoria.

---

## 5.4. Otros eventos relevantes

- **Errores en Notebook**:
  - `notebook` step con errores altos en `/status`.
  - Acción: revisar credenciales de NotebookLM, latencia de red, tamaño de documentos.

- **Errores en Observación**:
  - `observation` con muchos `error_count`.
  - Acción: revisar DataSources (paths de logs, endpoints HTTP, permisos).

- **STOP elevado**:
  - Demasiados `STOP` en decisiones.
  - Acción:
    - revisar configuración de fusibles (umbrales demasiado bajos),
    - revisar lógica en `DualRuntimeOperator` (puedes ajustarla sin tocar ciencia).

---

## 6. Buenas prácticas operativas

1. **Separar entornos**:
   - dev, stage, prod con `AGW_ENV`.
   - Distintas `AGW_RUNTIME_ROOT` por entorno.

2. **API key obligatoria en prod**:
   - `AGW_API_KEY` siempre configurado en prod.
   - Rotación periódica de claves.

3. **Log estructurado y rotación**:
   - Integrar con syslog / ELK / Datadog / etc.
   - No loguear payloads sensibles.

4. **Backups y retención de evidencia**:
   - Respaldar `runtime_data/sessions` y `runtime_data/system_status.json`.
   - Política de retención por compliance (ej. 1 año).

5. **Revisión periódica programada (Scheduler)**:
   - Usar `SimpleScheduler` o un cron externo para:
     - re‑ejecutar pipeline Cold,
     - refrescar perfiles,
     - recalibrar fusibles.

6. **Playbooks de incidente**:
   - Circuito `motor` OPEN → runbook específico.
   - Guardrails activados repetidamente → runbook de pipeline de features.
   - Fallback alto → runbook de revisiones con cliente.

7. **Documentación por cliente**:
   - Mantener notas por cliente:
     - qué DataSources se usan,
     - qué invariantes principales persigue ese cliente (aunque no estén codificadas aquí),
     - qué Motor se está usando (si hay variantes).

---

Con este manual, un equipo técnico/auditor puede:

- Entender cómo se integra un cliente.
- Entender dónde enchufar fuentes y Motor.
- Leer correctamente los indicadores del Cockpit.
- Tener una respuesta operativa clara ante eventos de resiliencia y guardrails.

Si quieres, podemos hacer también un `docs/ONBOARDING_CHECKLIST.md` que sea literalmente una checklist de 1 página para:  
“nuevo cliente → pasos 1–10”, desde intake de documentación hasta primer `/analyze` y validación de Cockpit.  
