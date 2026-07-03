# antigravity_wings

Exoesqueleto de coherencia y mitigación de riesgo alrededor de un Motor (Black Box).

## Qué es esto

Este repo NO contiene lógica científica interna; el "Motor" se representa como caja negra.

- **Motor (Black Box)**: Kernel propietario que evalúa evidencia numérica y devuelve configuraciones de fusibles
- **Exoesqueleto (Antigravity Wings)**: Este repo — agentes + tomografía + operación + observabilidad

**Principio fundamental**: "No existe coherencia sin contexto". Antes de evaluar con el motor, construimos el mapa del sistema del cliente.

---

## Componentes del Exoesqueleto

- **Intake automatizado**: Email/Form → request de información autorizada
- **Observación del sistema del cliente**: Captura de flujos/docs sin intervenir
- **Tomografía (mapa/grafo estructural)**: Nodos/aristas + criticidad
- **Agentes Duales (Mario / Luigi / Árbitro)**:
  - **Mario (Forward Scan)**: Inventario de capacidades, márgenes seguros, redundancias
  - **Luigi (Backward Scan)**: Puntos sin retorno, cascadas de fallo, gaps operativos
  - **Árbitro**: Consolidación con trazabilidad de desacuerdo
- **Bridge a Notebook Workspace (NotebookLM)**: Memoria contextual por cliente
- **Traducción a evidencia numérica**: Determinista, report → feature vector/matriz
- **Interfaz de Motor (Black Box) + MockMotor**: HISTÓRICO / ACTUALIZADO 2026-06-23: Contract + stub para testing aislado. Default actual: real (LocalCanonical desde core/kernel_1240421.py o RealMotor). Ver nota en docs y core.
- **Generación de fusibles (FuseSpec)**: Dónde/qué/umbral/severidad
- **Perfiles congelados por cliente (ClientProfile)**: Snapshot auditable, versionado
- **Operador dual en caliente (DualRuntimeOperator)**: Ejecución 24/7 de fusibles

---

## Flujo End-to-End (Automatizado)

```
Cliente
  → (Email/Form Intake)
  → Validador de permisos + Checklist de información
  → Carga segura de documentos autorizados (Drive/Storage)
  → Creación de cuaderno NotebookLM por cliente
  → Observación (captura de flujos + metadatos)
  → Tomografía 3D (grafo nodos/aristas + criticidad preliminar)
  → Mario Report (forward scan: capacidades, redundancias)
  → Luigi Report (backward scan: riesgos, puntos sin retorno)
  → Árbitro (consolidación + registro de desacuerdo)
  → NotebookLM (memoria contextual del caso; resumen solo de fuentes cargadas)
  → Traductor numérico (determinista: reportes/summary → evidencia estructurada)
  → Motor (Black Box: recibe números, devuelve rangos + recomendaciones)
  → Generador de fusibles (FuseSpec: dónde/qué/umbral/severidad)
  → Instalación en sistema del cliente:
      • modo SHADOW (solo observa y reporta)
      • modo SOFT (interviene solo en extremos)
      • modo HARD (política completa)
  → Monitoreo continuo + alertas + escalamiento humano si hay "rojo" o gaps
```

**Escalamiento humano se activa por**:
- Gaps de información
- Inconsistencias entre Mario/Luigi
- Falta de evidencia crítica
- Permiso insuficiente
- Riesgo alto detectado
- Punto irreversible sin protección

---

## Modelo de Servicio

### A) "Book Your Service" (tipo doctor)
- Evaluación puntual + alineamiento
- Recomendación de próxima revisión
- Cadencia variable según riesgo/salud del sistema

### B) "Integrate Yourself" (24/7)
- Agentes residentes + fusibles activos
- Alertas automáticas
- Intervención humana solo si zona amarilla/roja o falta info

---

## Arquitectura Dual (Mario/Luigi)

**Renombre**: ya no "Luz/Sombra" → ahora "Mario/Luigi" (evita sesgos semánticos, mantiene lenguaje operacional)

- **Mario (Agente Forward)**: Lee desde el inicio → capacidades, márgenes, redundancias
- **Luigi (Agente Backward)**: Lee desde el final → puntos sin retorno, cascadas de fallo, riesgos
- **Árbitro**: Consolida sin mezclar conclusiones; mantiene trazabilidad de desacuerdo

**Operador Dual en Runtime**:
- Mario view → decision (optimista: GO/DEGRADE)
- Luigi view → decision (pesimista: STOP/ESCALATE si high severity)
- Arbiter → decision final (toma la más conservadora)
- Color state: green (GO) / yellow (DEGRADE/ESCALATE) / red (STOP)

---

## Seguridad y Privacidad

- **No IP disclosure**: Motor queda como Black Box; lógica propietaria en repos privados
- **Aislamiento por cliente**: Cada cliente tiene su workspace/cuaderno/perfil
- **Permisos explícitos**: Solo documenta/accede lo autorizado explícitamente
- **Minimización de datos**: Solo lo necesario para análisis
- **Audit trail**: Perfil congelado + versiones + hashes

---

## Quick Start

```bash
# Demo end-to-end con MockMotor
python -m antigravity_wings.scripts.demo_pipeline

# O con Makefile
make demo

# Tests smoke
make test
```

---

## Auditoría y Certificación (Canon v1.0)

Este repositorio ha sido certificado como **Audit-Grade** en enero 2026.

- **Commit SHA**: `760ffbbb9e4af35a6f1fb7001b0b09724316d0f14`
- **Rama Canónica**: `canon-v1.0-freeze`
- **Manifiesto de Integridad**: [CANON_MANIFEST.json](CANON_MANIFEST.json) (Hashes SHA-256 certificados).
- **CI Status**: [![Audit-Grade Gate CI](https://github.com/RicciYazigi/antigravity_wings/actions/workflows/audit_gate.yml/badge.svg)](https://github.com/RicciYazigi/antigravity_wings/actions/workflows/audit_gate.yml)
- **Referencia Canónica**: [CANON_V1_0_PILOT_READY.md](docs/CANON_V1_0_PILOT_READY.md).
- **Estado de Auditoría**: 🟢 **VERIFICADO (JULES 2024 SOLVENTADO)**.

Para verificar la integridad del canon:
```bash
# Verificar hashes del manifiesto
python get_real_hashes.py
```

