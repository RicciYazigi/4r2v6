# 📚 4R2 Definitive Scientific & Mathematical Blueprint (v5.3.1)

Este documento constituye el **Contrato Científico-Matemático Definitivo** del Motor Cognitivo 4♻️2 y su exoesqueleto Antigravity Wings. Formaliza las relaciones de coherencia, la calibración de umbrales y la integración de fusibles de seguridad en producción.

---

## 1. El Framework Ontológico de Capas (NRIF) - [DOCUMENTED]

El estado cognitivo y físico del sistema se representa en cada ciclo $i$ mediante una tétrada de vectores reales normalizados (embeddings semánticos y métricas físicas):

$$\mathbf{S}_i = \{N_i, R_i, I_i, F_i\}$$

Donde:
*   **$N_i$ (Capa Normativa):** Vector de metas, directrices éticas y restricciones (dim: $D_{sem}$).
*   **$R_i$ (Capa Representacional):** Embedding del estado del contexto interno y memoria semántica (dim: $D_{sem}$).
*   **$I_i$ (Capa Informacional):** Vector que representa la respuesta o acción inferida (dim: $D_{info}$).
*   **$F_i$ (Capa Física):** Métricas de consumo de recursos en hardware (siempre dim: $4$):
    $$\vec{F}_i = [FLOPS, \text{Memoria (GB)}, \text{Energía (J)}, \text{Latencia (ms)}]$$

---

## 2. Álgebra del Coherence-Kernel (Algoritmo 1240421) - [DOCUMENTED]

El kernel opera exclusivamente bajo la convención de **Distancia Geométrica (Cero es Coherencia Perfecta)**. Esto unifica la polaridad y evita falsos positivos.

### A. Normalización Numérica Estable
Se define el operador de normalización robusta $\mathcal{N}(\vec{v})$:

$$\mathcal{N}(\vec{v}) = \frac{\vec{v}}{\|\vec{v}\| + \epsilon} \quad (\text{donde } \epsilon = 10^{-8})$$

### B. Coherencias Parciales (Distancia de Coseno)
1.  **Distancia Normativo-Representacional ($C_{NR}$):**
    $$C_{NR} = 1.0 - \mathcal{N}(N_i) \cdot \mathcal{N}(R_i)$$
2.  **Distancia Representacional-Informacional ($C_{RI}$):**
    $$C_{RI} = 1.0 - \mathcal{N}(R_i) \cdot \mathcal{N}(I_i)$$
3.  **Distancia Informacional-Física ($C_{IF}$):**
    Dado que $D_{info} \neq 4$ por lo general, se realiza un relleno con ceros (zero-padding) del vector más corto hasta igualar la dimensión del más largo, y se re-normaliza:
    $$C_{IF} = 1.0 - \mathcal{N}(I_{aligned}) \cdot \mathcal{N}(F_{aligned})$$

### C. Coherencia Total Ponderada ($C_{total}$)
Para reflejar la proporción cuántica-cognitiva $1:4:16$ del marco ontológico de capas y cumplir con la restricción de convexidad estadística y normalización del kernel ($\sum w = 1.0$), los pesos se definen como la normalización del denominador 21:

$$C_{total} = w_{NR} C_{NR} + w_{RI} C_{RI} + w_{IF} C_{IF}$$

Donde:
*   $$w_{NR} = \frac{1}{21} \approx 0.0476$$
*   $$w_{RI} = \frac{4}{21} \approx 0.1905$$
*   $$w_{IF} = \frac{16}{21} \approx 0.7619$$

---

## 3. Termodinámica de la Computación (Loss & Landauer) - [DOCUMENTED]

### A. Costo de Landauer Operacional
La disipación energética por borrado de información lógica se calcula como una analogía operacional calibrada:

$$L_{landauer} = \lambda_{landauer} \cdot \Delta_{changes}$$

### B. Función de Pérdida 4♻️2 ($Loss_{4R2}$)
La función de pérdida para optimización se define de manera monótona con la distancia de incoherencia:

$$Loss_{4R2} = L_{base} + \alpha \cdot C_{total}^2 + \gamma \cdot L_{landauer}$$

---

## 4. Calibración en 3 Bandas e Integración de Fusibles - [DOCUMENTED]

La toma de decisiones de seguridad (Cockpit y DualRuntimeOperator) se rige por tres zonas de coherencia basadas en la distribución de la cola de la distancia de coseno:

```
[ C_total ] ─── < 0.35 ───> ZONA VERDE  ──> Inferencia Nominal. Genera VerificationGuard (VER).
            ─── [0.35, 0.65] ──> ZONA GRIS   ──> Riesgo de Drift. Genera Warning Fuse (Severidad: Medium).
            ─── > 0.65 ───> ZONA ROJA   ──> Colapso/Incoherencia. Genera Critical Fuse (FAIL-CLOSED/STOP).
```

### A. Blindaje de Seguridad contra Bypass (P0 Resoluto)
*   El fusible de verificación (`VER`) utiliza estrictamente el score de calidad calculado en el servidor (`coherence_score` o `1.0 - global_distance` calculado del kernel) en lugar de extraer el campo `coherence` o `value` del payload del cliente.
*   **Fail-Closed Activo:** Si el score del motor no se encuentra disponible o es nulo, el fusible evalúa por defecto como `"BLOCK"`, previniendo que la omisión de campos por parte del cliente evada la seguridad.

### B. Fail-Loud de Fusibles Desconocidos (Causa 3 Resoluta)
*   Cualquier especificación de fusible cuyo tipo sea desconocido o no soportado por el operador dual genera una excepción explícita (`ValueError`), interrumpiendo inmediatamente la ejecución.

---

## 5. Agregación de Riesgo ($R_i$) y Operador de Reducción - [ROADMAP]

La siguiente capa teórica de reducción de entropía está planificada para futuras implementaciones:

### A. Agregación de Riesgo ($R_i$)
El riesgo cognitivo combina ineficiencias físicas, contradicciones semánticas e inestabilidad temporal:

$$R_i = \rho_1 I_{total} + \rho_2 S_{window} + \rho_3 T_i$$

Donde:
*   **$I_{total}$ (Incoherencia total):** $\lambda_1 I_{contra} + \lambda_2 I_{state}$ (requiere integración con modelos NLI DeBERTa-v3).
*   **$S_{window}$ (Saturación de contexto):** $\eta_1 S_{len} + \eta_2 \hat{H}$ (Entropía de Shannon sobre tópicos).
*   **$T_i$ (Inestabilidad / Thrashing):** Frecuencia y magnitud de cambios abruptos en decisiones lógicas consecutivas.

### B. El Operador de Reducción 4♻️2 (Purga de Contexto)
Cuando el riesgo cognitivo excede la tolerancia del sistema ($R_i \ge \tau$), se activa la purga termodinámica de contexto:
1.  **`SELECT`:** Extrae únicamente los claims con mayor peso e importancia semántica.
2.  **`COMPRESS`:** Abstrae el historial disperso en esquemas estructurados de alta densidad.
3.  **`DISCARD`:** Elimina por completo el texto muerto e historial crudo para restablecer la entropía del sistema a niveles mínimos.
