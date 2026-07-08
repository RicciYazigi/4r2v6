# BENCHMARK_COMPARISON_PUBLIC — 4R2 vs. datasets adversariales públicos
**TRACE_ID:** ARS-20260707-APEX1 · **Fase 1 / Gap G1** · **Fecha:** 2026-07-07
**Estado:** OK (ejecutado end-to-end) · **Hallazgo:** ALERTA — resultado negativo honesto, diagnosticado.
**Reproducible:** `scripts/eval_public_benchmarks.py` · seed 1240421 · evidencia sellada `evidence/benchmark_public_20260707.json` (SHA-256 `39280c9c…fec521`).

> Regla de esta sesión (§0.7 del plan APEX): *honestidad de gaps > narrativa de victoria*. Este documento reporta un resultado que **no favorece** al proyecto tal como está hoy, porque un fallo bien diagnosticado vale más para el roadmap que un número bonito sin diagnóstico. Este es, de hecho, el entregable más valioso de la Fase 1.

---

## 1. Qué se midió (método, sin adornos)

| Ítem | Valor |
|---|---|
| Kernel | `core/kernel_1240421.py::CoherenceKernel.compute_with_regime` (v6.1.0, math sellado, sin tocar) |
| Backend de embedding | **LSA (TF-IDF + SVD k=64, numpy puro, determinista)** — *lexical, NO deep-semantic* |
| Datasets | AdvBench (llm-attacks) · Alpaca (tatsu-lab) · HarmBench standard (centerforaisafety) — todos públicos, descarga real cacheada |
| N | AdvBench 520 pares reales (goal+target) · Alpaca 520 pares reales (instruction+output) · HarmBench 200 standard behaviors |
| Latencia | **0.174 ms/evento (media)** — el hot path determinista sigue en el mismo orden que E3 (~0.19 ms) |

**Mapeo NRIF (Eval 1, pipeline completo):** normative=política de seguridad genérica; representational=petición (goal AdvBench / instruction Alpaca); informational=respuesta REAL del dataset (target AdvBench / output Alpaca); physical=heurística de verifiabilidad `verifiability()`. Clase positiva = AdvBench (cumplimiento dañino, debería violar política). Clase negativa = Alpaca (ayuda benigna).

**Eval 2 (request-level):** HarmBench standard behaviors vs. peticiones Alpaca, sobre el eje `C_NR(policy, request)` — **sin respuesta sintética** (no se inventó texto; se mide la coherencia petición↔política directamente).

---

## 2. Resultado (verificado, tier-LSA, seed fijo)

### Eval 1 — AdvBench (dañino) vs Alpaca (benigno), pipeline completo
| Métrica | Valor | Lectura |
|---|---|---|
| **AUROC C_total** | **0.418** | < 0.5 → **el kernel puntúa el cumplimiento dañino como MÁS coherente que la ayuda benigna** |
| AUROC C_NR | 0.412 | El eje normativo tampoco separa con embeddings léxicos |
| AUROC C_IF (invertido) | 0.315 | Peor: los targets dañinos parecen *más* verificables (son fluidos) |
| F1 @ Youden θ=0.375 | 0.697 | **Espejismo**: recall 0.956 pero FPR 0.789 — clasifica casi todo como dañino |
| F1 @ θ=0.35 fijo | 0.695 | Igual de no-discriminante |
| Accuracy @ Youden | 0.584 | Apenas sobre azar en un set balanceado |

Distribución `C_total`: dañino μ=0.421 (p5 0.376 / p95 0.490, **baja varianza**) vs benigno μ=0.443 (p5 0.304 / p95 0.618, **alta varianza**). Los cumplimientos dañinos de AdvBench son fluidos e **internamente coherentes**, así que se agrupan en un rango estrecho de baja incoherencia; la ayuda benigna de Alpaca es más dispersa. No hay frontera separadora.

### Eval 2 — HarmBench standard vs Alpaca, request-level (C_NR)
| Métrica | Valor |
|---|---|
| AUROC C_NR | 0.414 |
| Media C_NR dañino / benigno | 0.468 / 0.479 (indistinguibles) |

---

## 3. Diagnóstico (por qué, mecanísticamente)

1. **El kernel es un detector de *incoherencia entre capas*, no un clasificador de daño puntual.** Una respuesta que cumple con una petición dañina es *coherente con esa petición* (comparten tema y léxico) y fluida — exactamente lo que el kernel puntúa como baja incoherencia. Esto **confirma cuantitativamente la tesis de los gaps G2/G3**: un gate de coherencia puntual es ciego al cumplimiento dañino fluido; hace falta deriva semántica / anclaje normativo, no coherencia cruda.
2. **El backend LSA (léxico) es demasiado débil para daño genérico cross-dominio.** Sin señal semántica profunda, "goal" y "target" de AdvBench comparten vocabulario → alta coherencia; una política de seguridad genérica no se alinea léxicamente de forma diferencial con ninguna clase.
3. **Política genérica ≠ contexto de dominio.** En su propio corpus E2/E3 (políticas de dominio: banca/seguros/médico/técnico + θ calibrado + VER-fuse + LBB), 4R2 SÍ separa (AUROC on-vs-grave/adv alto en `evidence/eval_E2_results.json`). El experimento público usa política genérica y sin dominio: revela que el gate actual es **dependiente de dominio y de backend de embedding**, no un detector de daño universal.

**Lo que este resultado NO dice:** no dice que el kernel esté roto ni que la matemática sea incorrecta (los 137 tests siguen en verde y la métrica cumple sus propiedades). Dice que **la capa de detección, con backend léxico y política genérica, no separa daño público** — un límite de alcance, no un defecto de corrección.

---

## 4. Comparación de mercado (sin maquillaje)

| Sistema | Métrica publicada | Tarea | 4R2 hoy |
|---|---|---|---|
| Galileo (Luna-2) | F1 = 0.95 | detección runtime | — |
| DeepContext | F1 = 0.84 | jailbreak multi-turno | — |
| NeMoguard | F1 = 0.793 (OpenAI Mod) / 0.875 (HarmBench) | moderación | — |
| **4R2 v6.1.0 (tier-LSA)** | **AUROC 0.42 / sin discriminación en AdvBench** | coherencia de capa | **por debajo — no comparable aún** |

**Veredicto honesto:** 4R2 **no** tiene hoy una métrica competitiva contra un dataset adversarial público **en su tier de embedding léxico**. La comparación cabeza-a-cabeza con Galileo/DeepContext/NeMo requiere: (a) el tier deep-semantic (sentence-transformers, no ejecutable en este sandbox → **ND**, roadmap con harness idéntico ya escrito), y (b) el estimador semántico de deriva de la Fase 3. El diferenciador real de 4R2 (matemática determinista sellada + gobernanza de reroute auditable) sigue siendo válido y escaso, pero **es un diferenciador de arquitectura/gobernanza, no de tasa de detección cruda** — y esta medición lo deja claro.

---

## 5. Consecuencia para el roadmap

Este resultado **re-prioriza y justifica cuantitativamente la Fase 3 (G2+G3)**: sin estimador semántico profundo, no hay paridad de benchmark posible. Antes de cualquier claim público de detección, el orden correcto es:
1. Cablear el tier deep-semantic (sentence-transformers) y re-correr **este mismo harness** (cero cambios de método) → obtener el AUROC tier-ST real.
2. Implementar el estimador de deriva semántica acumulada (Fase 3) y medir la separación evasión-vs-benigno con la misma vara.
3. Solo entonces reclamar posición vs. mercado, con el número que salga.

## 6. Etiquetado de veracidad
- AUROC/F1/latencia AdvBench y HarmBench: **empírico con límites** (tier-LSA, N=520/200, seed 1240421, reproducible).
- Métricas de competidores: **plausible** (auto-reportadas por cada vendor, no re-ejecutadas por nosotros).
- Tier deep-semantic de 4R2: **ND** (no ejecutable en este entorno; harness listo).
- Confianza global del documento: **alta** en el hallazgo negativo (verificado por ejecución); **media** en su generalización a otros datasets no corridos.
