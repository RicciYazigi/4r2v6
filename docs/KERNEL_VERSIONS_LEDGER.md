# 📊 KERNEL_VERSIONS_LEDGER.md

Este registro compara de forma exhaustiva las cinco variantes de fórmulas y pesos identificadas en el historial del Motor Cognitivo 4R2, analizando sus propiedades y los riesgos operacionales asociados.

---

## 1. Tabla Comparativa de las 5 Versiones

| Versión / Origen | Tipo de Agregación ($C_{total}$) | Pesos por Defecto ($w_{NR}, w_{RI}, w_{IF}$) | Rango | Métrica de Capa Informacional-Física ($C_{IF}$) | Estado Operacional |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1. Kernel del ZIP** | Multiplicativa (o Suma custom) | Dinámicos / Variables | $[0, 1]$ | Coseno ponderado con métricas físicas directas | Legacy Operativo |
| **2. Kernel v3.0** | Suma Ponderada | Equitativos ($\frac{1}{3}, \frac{1}{3}, \frac{1}{3}$) | $[0, 2]$ | Divergencia KL acotada ($\min(D_{KL}, 1.0)$) | Histórico de Tests |
| **3. README v5.2 / arXiv** | Suma Ponderada | No especificados | No especif. | Coseno con relleno de dimensiones | Transicional |
| **4. Whitepaper Dic 2025** | Suma Ponderada | Equitativos (implícitos) | $[0, 2]$ | Divergencia KL | Teórico / Académico |
| **5. Core v5.3.1 (Actual)** | Suma Ponderada | Proporcional 21 ($\frac{1}{21}, \frac{4}{21}, \frac{16}{21}$) | $[0, 2]$ | Coseno con alineación por zero-padding | Producción Activo |

---

## 2. Análisis del Riesgo Crítico en la Versión Actual (v5.3.1)

El uso de los pesos $\mathbf{w} = \{w_{NR}=\frac{1}{21}, w_{RI}=\frac{4}{21}, w_{IF}=\frac{16}{21}\}$ basados en la progresión estética del patrón $1:4:16$ presenta una vulnerabilidad de diseño de **Severidad Máxima (P0)**:

### El Punto Ciego de la Capa Física
Debido a que la capa Física ($w_{IF}$) recibe el **$76.19\%$** del peso total, mientras que la capa Normativa ($w_{NR}$) recibe únicamente el **$4.76\%$**, el sistema sufre de un sesgo de eficiencia:

*   **Escenario de Fuga Ética / Violación de Reglas:**
    Supongamos una transacción con una traición total de reglas de seguridad ($C_{NR} = 1.0$, valor pésimo) pero ejecutada de manera óptima por el hardware ($C_{RI} = 0.1$ y $C_{IF} = 0.1$, alineación de recursos excelente).
*   **Cálculo del Score Global ($C_{total}$):**
    $$C_{total} = \frac{1}{21} \cdot 1.0 + \frac{4}{21} \cdot 0.1 + \frac{16}{21} \cdot 0.1$$
    $$C_{total} = 0.0476 + 0.0190 + 0.0762 = \mathbf{0.1428}$$
*   **Decisión en Producción:**
    Dado que $0.1428 < 0.35$ (Zona Verde / Alta Confianza), el sistema clasificará la transacción como **completamente segura y estable**, permitiendo la fuga o violación de reglas sin disparar alertas ni fusibles.

---

## 3. Recomendación de Consolidación

Para eliminar este punto ciego y unificar el motor de forma auditable, proponemos:

1.  **Restaurar los pesos balanceados ($\frac{1}{3}, \frac{1}{3}, \frac{1}{3}$)** como la configuración segura por defecto en producción, garantizando que el alineamiento ético/normativo y la precisión representacional tengan el mismo peso e impacto que la optimización de hardware.
2.  **Tratar los pesos $1/21, 4/21, 16/21$ únicamente como un perfil experimental de optimización de hardware** (`physics_priority_profile`), el cual debe ser activado explícitamente y nunca correr por defecto en el Hard-Gate de seguridad.
3.  **Fijar esta decisión en un nuevo Registro de Decisiones de Arquitectura (ADR-0005)** que declare obsoletas las 4 fórmulas previas.
