# RADIOGRAFÍA_FINAL_3D.md - Antigravity Wings
> **STATUS: CANONICAL**  
> **VERSION: 1.0 (POST-AUDIT)**

Este documento representa la "Tomografía 3D" del sistema: la visión definitiva de cómo se conectan las capas de infraestructura, ciencia canónica y auditoría.

---

## 1. Arquitectura de Conexiones (Tomografía)

```mermaid
graph TD
    subgraph "Capa Web (Cockpit & API)"
        LA[launcher.py] --> SV[api/server.py]
        SV --> CP[cockpit/ dashboard]
        SV --> SEC[api/security.py]
        SV --> MET[/metrics Prometheus]
    end

    subgraph "Capa de Orquestación"
        SV --> MO[orchestration/master.py]
        MO --> SM[orchestration/session_manager.py]
        SM --> DB[(sessions.db SQLite)]
        MO --> SCH[orchestration/scheduler.py]
    end

    subgraph "Capa de Observación y Tomografía"
        MO --> OB[observation/observer.py]
        OB --> REG[observation/registry.py]
        MO --> TB[tomography/builder.py]
    end

    subgraph "Capa de IA (Kernel 1240421)"
        MO --> NUM[numeric/translator.py]
        NUM --> KER[core/kernel.py N-R-I-F]
        KER --> ENT[Entropy Loss / Coherence]
    end

    subgraph "Capa de Ejecución (Motor Bridge)"
        MO --> MB[motor_bridge/loader.py]
        MB --> CB[resilience/circuit_breaker.py]
        MB --> PM[pilots/chatbot_motor.py]
    end

    subgraph "Capa de Telemetría y Evidencia"
        MO --> HM[api/telemetry.py]
        MO --> EP[api/evidence_packer.py]
        EP --> IDX[CANON_MANIFEST.json SHA-256]
    end

    %% Conexiones cruzadas
    HM --> |Exporta| STS[system_status.json]
    EP --> |Sella| PKG[Audit Package]
```

---

## 2. Flujo de una Decisión (Audit-Grade)

1.  **Entrada**: `POST /analyze/{client_id}` con payload de negocio.
2.  **Seguridad**: Verificación de `AGW_API_KEY` y sanitización del payload.
3.  **Persistencia**: `SessionManager` indexa la traza en **SQLite**.
4.  **Observación**: `SourceRegistry` recolecta evidencias crudas.
5.  **Tomografía**: `TomographyBuilder` construye el grafo de estado del cliente.
6.  **Traducción**: `NumericTranslator` prepara los vectores para la ciencia.
7.  **Ciencia Canónica**:
    *   **Evaluación N-R-I-F**: El Kernel 1240421 evalúa coherencia normativa, representacional, informacional y física.
    *   **Coherencia Total**: Resultado matemático inmutable del proceso.
8.  **Motor Piloto**:
    *   `MotorLoader` inyecta la lógica del chatbot (o cualquier piloto).
    *   `CircuitBreaker` garantiza que si el motor falla, Antigravity Wings toma el control.
9.  **Decisión Dual**: `DualRuntimeOperator` arbitra entre Luz y Sombra bajo la Constitución v1.0.
10. **Sellado**: `EvidencePacker` genera un paquete con **SHA-256** de cada artefacto y un manifiesto `evidence_index.json`.

---

## 3. Identificación de Gaps & Roadmap

### Gaps Identificados (Control de Calidad)
*   **Aislamiento de Docker**: El sistema es sensible a colisiones de puertos si no se definen variables de entorno limpias.
*   **Redacción de PII**: Actualmente se redacta de forma básica en el `EvidencePacker`. Se recomienda un motor de NER (Named Entity Recognition) para auditoría de alto nivel.
*   **Visualización 3D**: El Cockpit es funcional y premium, pero la visualización del grafo de tomografía sigue siendo textual/JSON.

### Roadmap de Evolución
1.  **Modo Doctor 2.0**: Automatización del `SimpleScheduler` para auditorías nocturnas de coherencia histórica.
2.  **Multitenancy**: Migración del índice SQLite a PostgreSQL para despliegues en clusters.
3.  **Cifrado Nativo**: Integración de KMS (Key Management Service) para cifrar los paquetes de evidencia en reposo.

---

Este sistema cumple con el estándar **Audit-Grade**. La infraestructura es invisible, la ciencia es auditable, y la coherencia es matemática.
