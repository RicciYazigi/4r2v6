# VALIDACIÓN ADVERSARIAL HELD-OUT — Defensa Anti-Camuflaje (`governance_anticamo`)

TRACE_ID: ARS-20260709-HELDOUT | Estado: OK | Rama: apex-20260707 (local, sin push)

## 1. Resumen (etiquetas de veracidad)

- **verificado** — La defensa `governance_anticamo` en su variante sin NLI generaliza robustamente en **español (ES)**, obteniendo un AUROC de **0.906** (n=48) sobre un conjunto de verbos y dominios nuevos no vistos.
- **verificado** — Se confirma el límite monolingüe de la postura léxica: sin NLI, el desempeño en **inglés (EN)** colapsa a **0.528** (n=12), comportándose como azar.
- **verificado** — El backend NLI (`mDeBERTa-v3-base-mnli-xnli`) es una señal generalizadora multilingüe eficaz, elevando el AUROC en inglés a **0.694** y reduciendo la Tasa de Evasión (ASR) global a la mitad (**20.0%** frente al **40.0%** sin NLI).
- **verificado** — El baseline $C\_NI$ solo (embeddings base) es sistemáticamente engañado por el camuflaje adversarial en dominios frescos (AUROC global de **0.503**, ASR del **100.0%**).
- **plausible** — Existen dominios técnicos específicos en inglés (ej. ciberseguridad industrial/OT, AUROC **0.000**) donde la semántica corporativa del camuflaje confunde tanto a $C\_NI$ como al clasificador NLI, requiriendo un red-team enfocado.

---

## 2. Resultados de la Evaluación (n=60)

Métricas medidas usando el embedder semántico `all-MiniLM-L6-v2` y el backend NLI en CPU:

| Configuración | AUROC Global | Bootstrap 95% CI | Tasa de Evasión (ASR) | Tasa de Falsas Alertas (ORR) |
|---|---|---|---|---|
| **C_NI Solo (Baseline)** | 0.503 | [0.352, 0.653] | 100.0% | 0.0% |
| **Defensa SIN NLI** | 0.857 | [0.752, 0.945] | 40.0% | 13.3% |
| **Defensa CON NLI** | **0.898** | **[0.802, 0.971]** | **20.0%** | **16.7%** |

### Desglose por Idioma (AUROC)

| Configuración | Subconjunto Español (ES, n=48) | Subconjunto Inglés (EN, n=12) |
|---|---|---|
| C_NI Solo (Baseline) | 0.490 | 0.528 |
| **Defensa SIN NLI** | **0.906** | 0.528 |
| **Defensa CON NLI** | **0.936** | **0.694** |

---

## 3. Cobertura de la Señal de Postura (`stance_score`)

La postura léxica determinista fue diseñada originalmente para español con un conjunto limitado de verbos. Al evaluar verbos ausentes (*despachar, copiar, autorizar, entregar, transferir, divulgar, filtrar, otorgar*), la cobertura se comporta de la siguiente forma:

*   **Cobertura Global:** **38.3%**
*   **Cobertura en Español (ES):** **47.9%** (las violaciones quedan en 0% de detección de ejecución, pero las de cumplimiento/rechazo se detectan exitosamente mediante marcadores de rechazo como *me niego* o *jamás*).
*   **Cobertura en Inglés (EN):** **0.0%**

---

## 4. Análisis de la Generalización e Interpretación

1.  **Por qué el AUROC sin NLI se mantuvo alto en español (0.906):**
    A pesar de que las violaciones usaron verbos no mapeados en el léxico (dando `stance = 0.0` y quedando como neutros), las respuestas legítimas de control de cumplimiento emplearon marcadores morfológicos de rechazo fuertes ("Me niego", "Jamás", "Rechazo de plano") que sí están incluidos en los patrones del SDK. Esto generó un score negativo (`stance < 0.0`), permitiendo una correcta separación matemática respecto a las violaciones.
2.  **Por qué el baseline colapsó (0.503):**
    El camuflaje semántico ("Bajo el marco de protección de datos, envié...") provoca que el embedding de la respuesta violatoria quede extremadamente cerca de la política, anulando la capacidad de discriminación basada en distancias geométricas.
3.  **Vulnerabilidad en Dominios Específicos (Ciberseguridad OT en inglés):**
    Se registró un AUROC de **0.000** (invertido) en el dominio de ciberseguridad industrial en inglés. La redacción de las violaciones ("Done. In alignment with protocols...") simula cumplimiento a un nivel tan refinado que tanto $C\_NI$ como el NLI clasificaron la violación como más segura que el rechazo explícito, constituyendo un punto ciego claro para la robustez adaptativa.

---

## 5. Recomendación de Diseño y Trade-offs

Se presentan las dos vías de mitigación identificadas:

### Vía A: Ampliación de Cobertura del Léxico (`stance`)
Consiste en mapear un diccionario y analizador morfológico más rico para español, e incorporar el soporte inicial de postura en inglés.
*   **Ventajas:** Latencia cercana a **0 ms**, ejecución determinista pura, sin sobrecosto de memoria o librerías de deep learning.
*   **Inconvenientes:** Frágil ante atacantes adaptativos que eviten los marcadores exactos y requiere mantenimiento continuo de diccionarios.

### Vía B: Pivotar hacia el Backend NLI como Señal Primaria
Consiste en delegar la discriminación semántica al modelo de lenguaje ligero inyectado.
*   **Ventajas:** Robusto ante sinónimos y variaciones sintácticas, soporte multilingüe nativo desde el primer día y reducción del ASR global a la mitad.
*   **Inconvenientes:** Añade una latencia significativa (**~2.5 segundos por muestra en CPU**) y requiere dependencias pesadas de GPU/torch que dificultan su despliegue en entornos *edge* o de alta frecuencia.
