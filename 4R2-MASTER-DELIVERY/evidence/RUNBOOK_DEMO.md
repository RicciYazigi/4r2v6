# 🚀 RUNBOOK: Demo de 5 Minutos (Audit-Grade)

Este runbook permite ejecutar una demostración técnica impecable del sistema 4R2, utilizando el stack **BASIC** para velocidad y el stack **ENHANCED** para profundidad de seguridad.

## Escenario 1: El Corazón del Motor (BASIC Stack)
*Objetivo: Mostrar la medición de coherencia en tiempo real y el costo de Landauer.*

1.  **Levantar Sistema**:
    ```powershell
    ./EJECUTAR_AHORA.ps1
    # Seleccionar [1] BASIC SYSTEM
    ```
2.  **Validar Health**: Verificar que el Cockpit cargue en `http://localhost:5173`.
3.  **Realizar Medición**:
    - Usar el botón "Measure Coherence" en la UI.
    - Observar el desglose de $C_{NR}$, $C_{RI}$ y $C_{IF}$.
    - Mostrar el **Landauer Cost** (evidencia física de la decisión).

## Escenario 2: Blindaje Adversarial (ENHANCED Stack)
*Objetivo: Demostrar el Protocolo de Armado y la Gate E (Seguridad).*

1.  **Cambiar a Enhanced**:
    ```powershell
    docker-compose -f systems/enhanced/docker-compose.yml up -d --build
    ```
2.  **Protocolo de Armado**:
    - Intentar medir sin armar (Error 403 esperado).
    - Ejecutar comando de armado:
      ```bash
      curl -X POST http://localhost:4000/api/arm -H "Authorization: Bearer dev-hash"
      ```
3.  **Gate E en Acción**:
    - Realizar una medición con alta divergencia (datos inconsistentes).
    - Observar cómo la **Gate E** bloquea la respuesta si la coherencia cae por debajo del umbral de seguridad.

---
**Evidencia Consolidada en:** `evidence/RealEngineReport.md`
