# Supuestos y Límites del Sistema (Assumptions & Limits)

Este documento define las fronteras de responsabilidad del framework Antigravity Wings v1.0, de acuerdo con las recomendaciones de la auditoría externa.

## 1. Garantía de Proceso vs. Garantía de Decisión

> [!IMPORTANT]
> Antigravity Wings es un **exoesqueleto de control**. Garantiza que el flujo de datos, la recolección de evidencia y la ejecución del Motor sigan el protocolo auditable.
> **NO garantiza la veracidad científica ni la seguridad de la decisión tomada por el Motor.**
> La responsabilidad de la "ciencia" (los algoritmos de decisión dentro del Motor) recae íntegramente en los desarrolladores del Motor.

## 2. Confianza en el Motor (Trusted Code)

- El framework asume que el código del Motor es **confiable**.
- No existe un mecanismo de sandboxing o aislamiento total de recursos para el Motor.
- Un Motor malicioso o con bugs críticos de memoria puede afectar la estabilidad del host.

## 3. Seguridad de Datos en Notebook Bridge

- El `NotebookClient` transforma perfiles técnicos en narrativa Markdown para su ingesta en NotebookLM.
- **Privacidad:** El operador es responsable de no incluir datos sensibles (PII) en los logs o evidencias que serán enviadas a plataformas externas como NotebookLM.
- El framework no realiza una sanitización automática de secretos dentro de la narrativa.

## 4. Integridad del Entorno de Ejecución

- El framework depende de la integridad del sistema de archivos local para el `ProfileStore`.
- Se recomienda el uso de **discos cifrados** y controles de acceso a nivel de SO para proteger las evidencias y perfiles históricos.
- Los hashes (SHA-256) detectan corrupción o manipulación accidental, pero no protegen contra un atacante con privilegios de escritura que pueda regenerar los hashes.

## 5. Latencia y Presupuesto de Tiempo (SLOs)

- El `CircuitBreaker` protege contra bloqueos individuales.
- El tiempo total de ejecución del pipeline depende de la complejidad del Motor.
- En entornos de alta carga, es responsabilidad del integrador monitorizar el "Time-to-Decision" mediante el endpoint de `/metrics`.

---
*Veredicto Auditoría 08/01/2026: GO para Pilotos Controlados.*
