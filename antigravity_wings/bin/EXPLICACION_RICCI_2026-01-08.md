# EXPLICACIÓN TÉCNICA DEL SISTEMA (V1.0 AUDIT-GRADE)
**Fecha:** 2026-01-08
**Estado:** CORE ESTABLE / MOCK MOTOR / API REST

## 1. Arquitectura Lógica del Sistema

El sistema opera bajo una arquitectura de **Orquestación Centralizada con Componentes Desacoplados**. No es monolítico; separa la lógica de negocio (Exoesqueleto) de la lógica científica (Motor).

### Flujo de Datos (Data Pipeline)

1.  **Ingesta (API Layer):**
    *   Endpoint: `POST /analyze/{client_id}`.
    *   Protocolo: HTTPS + API Key Authentication.
    *   Payload: JSON con metadata y referencias a archivos (futuro: binary upload).
    *   Salida: `DecisionContract` estricto (Pydantic v2).

2.  **Orquestación (MasterOrchestrator):**
    *   Rol: Controlador de flujo sincrónico.
    *   Responsabilidad: Garantizar que **pase lo que pase** (error en motor, timeout, fallo de red), el sistema devuelva una decisión válida y empaquete la evidencia.
    *   Mecanismo: `try/except` global con estrategias de `FALLBACK` (Escalate/Stop).

3.  **Observación & Inferencia (Observation Phase):**
    *   Objeto: `SystemSnapshot`.
    *   Función: Estandarizar inputs heterogéneos (bancos, seguros, salud) en una estructura de grafo (`TomographyGraph`) que el sistema pueda entender.

4.  **Inferencia Científica (Motor Bridge):**
    *   **Estado Actual:** `MockMotor` (Simulación determinista).
    *   **Lógica:** Recibe vectores numéricos (`NumericEvidence`), retorna `RiskScore` (0.0 - 1.0).
    *   **Protección:** Envuelto en `CircuitBreaker` (Patrón de Resiliencia). Si el motor tarda >30s o falla 3 veces, el circuito se abre y el sistema responde `ESCALATE` automáticamente (Fail-Safe).

5.  **Validación Dual (Agentic Layer):**
    *   **Mario (Light):** Optimiza para aprobación (negocio). Busca razones para el "SÍ".
    *   **Luigi (Shadow):** Optimiza para riesgo (seguridad). Busca razones para el "NO" (anomalías, fraudes).
    *   **Arbitraje:** `DualRuntimeOperator` cruza ambos reportes. Si Luigi detecta riesgo > Umbral, su veto es vinculante.

6.  **Auditoría (Evidence Packer):**
    *   Output: `evidence_bundle/`.
    *   Contenido: `decision.json` (Resultado), `profile.json` (Estado completo del sistema), `HASH.txt` (Integridad SHA-256).
    *   Garantía: Reproducibilidad forense. Con el bundle, puedes reconstruir la decisión exacta años después.

## 2. Estado de Implementación Técnica

### Lo que SI tenemos (Core Validado):
*   **API Robusta:** FastAPI con validación de tipos estricta (`DecisionContract`).
*   **Manejo de Errores:** No crashea. Si algo falla, degrada y escala.
*   **Aislamiento:** Docker containers listos para despliegue.
*   **Simulación de Realidad:** `pilots/insurance/mocks.py` emula latencias y respuestas de un sistema de visión real.

### Lo que FALTA (Para Producción):
1.  **Motor Real (Gemini Integration):**
    *   Reemplazar `mocks.py` por `gemini_adapter.py`.
    *   Implementar autenticación OAuth2/API Key con Google Cloud Vertex AI.
    *   Manejo de cuotas y costos de tokens.

2.  **Ingesta Real de Archivos:**
    *   Actualizar `DataSource` para leer bytes reales de imágenes (S3, Azure Blob, o multipart/form-data) en lugar de URLs simuladas.

3.  **Frontend (Cliente):**
    *   Desarrollar la interfaz de usuario (Mobile/Web) que consuma la API.

## 3. Siguientes Pasos (Roadmap Técnico)

1.  **Fase 1 (Completada):** Hardening del Core. El sistema es seguro y auditables.
2.  **Fase 2 (Conexión):** Implementar `gemini_adapter.py` para inyectar inteligencia real.
3.  **Fase 3 (Interfaz):** Construir la capa de presentación (App).
4.  **Fase 4 (Despliegue):** Infraestructura en Nube (AWS/GCP) con balanceo de carga.

---
**Nota:** El sistema está diseñado para ser agnóstico al modelo. Hoy es un Mock, mañana es Gemini, pasado mañana un modelo local Llama 3. El cambio es transparente para el resto de la arquitectura.
