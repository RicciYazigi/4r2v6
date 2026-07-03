# WHAT_IS_NOT.md - Límites del Exoesqueleto

Para proteger la propiedad intelectual de la ciencia privada y asegurar la claridad ante auditores y partners, este documento define qué queda **fuera** de la jurisdicción de `antigravity_wings`.

---

## 1. Lo que NO es Antigravity Wings

- **NO es el Oráculo Científico**: El framework no contiene fórmulas de riesgo, modelos predictivos ni lógica de negocio específica. Eso pertenece exclusivamente al **Motor (Black Box)**.
- **NO es una Base de Datos de Clientes**: Aunque gestiona sesiones y perfiles, no es un CRM ni un sistema de almacenamiento persistente de PII a largo plazo. Es un **paso de auditoría**, no un maestro de datos.
- **NO es una Interfaz de Usuario de Negocio**: El Cockpit es para **operaciones técnicas y cumplimiento**. No sustituye a la consola operativa donde los analistas de negocio toman decisiones humanas.
- **NO es un Sistema de Prevención de Fraude**: Es un **exoesqueleto de coherencia**. Detecta si el sistema es íntegro y auditable, pero la "culpa" o el "riesgo" de fraude lo evalúa la ciencia inyectada.

---

## 2. Garantía de Proceso vs. Garantía de Decisión (Frontera Crítica)

> [!CAUTION]
> Antigravity Wings garantiza la **corrección técnica del proceso** (que el Motor fue llamado, que la evidencia se selló, que el circuito reaccionó).
> **NO garantiza la veracidad ni la sabiduría de la decisión.** Si el Motor toma una decisión catastrófica pero sigue el protocolo, el framework registrará esa catástrofe con fidelidad perfecta, pero no la impedirá a menos que rompa un fusible configurado.

---

## 2. Fronteras de Responsabilidad

| Concepto | Responsabilidad del Exoesqueleto | Responsabilidad de la Ciencia Privada |
| :--- | :--- | :--- |
| **Decisión** | Ejecutar fusibles y garantizar auditoría. | Definir el `score` y la recomendación. |
| **Datos** | Observar flujos y mapear el grafo. | Interpretar el significado de esos flujos. |
| **Resiliencia** | Abrir el circuito ante latencia. | Optimizar el rendimiento del cómputo. |
| **Evidencia** | Sellar el HASH.txt inmutable. | Garantizar que los inputs son científicamente válidos. |

---

## 3. Principio de Caja Negra

El principio fundamental es que `antigravity_wings` podría ser reemplazado por cualquier otro orquestador de auditoría sin que la Ciencia Privada se vea comprometida, y viceversa. La interfaz `MotorInterface` es la única "aduana" entre ambos mundos.
