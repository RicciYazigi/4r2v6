# Informe E2/E3 — Embeddings Reales y Piloto Sombra

**Fecha:** 2026-07-04 | **Kernel:** v6.1.0 | **Semilla:** 1240421 | **Estado: PASS**
**Harness:** `scripts/eval_e2_e3.py` (backend conmutable: auto-detecta
sentence-transformers; en este entorno corrió **LSA real** — TF-IDF+SVD k=64,
puro numpy, determinista, cero mocks).

## 1. Qué se midió (pipeline completo texto→gate)

240 casos de **texto real** (política, solicitud, respuesta) en 4 dominios
(insurance/banking/medical/technical) × 4 clases (on-topic, deriva leve,
grave, adversarial camuflado). Verificabilidad F extraída de **rasgos reales**
de la respuesta: solapamiento de groundedness, contenido numérico, marcadores
de cita, accionabilidad, y **negación de cumplimiento** ("without
verification", "skipping the two-factor step", "no rollback plan") — una
respuesta que afirma haber saltado controles es objetivamente menos
verificable.

## 2. Hallazgo central: la calibración es por-embedder y la defensa es por capas

El θ=0.35 (calibrado para el régimen sintético E1) quedó descalibrado para el
embedder LSA (FPR 8.3%, leves sobre-bloqueados). Y ninguna capa sola basta:

| Tier | Config | FPR on-topic | FNR grave | Veto adversarial | Aceptable |
|:-----|:-------|:---:|:---:|:---:|:---:|
| T1 | gate θ=0.35 default | 0.083 | 0.0 | 0.75 | 0.72 |
| T2 | gate θ*=0.4625 calibrado | 0.0 | 0.0 | **0.0** | 0.70 |
| **T3** | **θ* + LBB + fusible VER** | **0.0** | **0.0** | **1.00** | **1.00** |

θ* = punto medio entre p95(on-topic)=0.35 y p5(grave)=0.57, derivado de datos.
AUROC C_total: on-vs-grave **1.0**, on-vs-adversarial **1.0** (con F
negation-aware; sin ella, 0.80 — evidencia de que la verificabilidad es una
capa de señal indispensable, no un adorno).

## 3. E3 — Piloto sombra (config T3 recomendada)

300 eventos mezclados (70% benigno, 15% leve, 10% grave, 5% adversarial),
modo log-only: **0 incidentes** (ningún grave/adversarial ALLOW), FLAG benigno
0.0% (< 10% criterio), distribución ALLOW 210 / FLAG 90 / BLOCK 0, latencia
media **0.124 ms** p95 0.164 ms por evaluación (afirmación sub-ms: medida).

## 4. Límites declarados (anti-humo)

- Backend LSA es léxico; el tier semántico-difícil requiere el backend
  sentence-transformers (mismo harness, auto-upgrade al instalarlo en host).
- Corpus autorado (240 casos): valida el pipeline y la mecánica de gating; el
  siguiente nivel es corpus público (HaluEval-style) + tráfico real de piloto.
- E3 es sombra sobre stream simulado con mezcla realista, no tráfico de
  cliente: ese es el criterio del milestone v6.2 con un piloto amigo.

## 5. Recomendación de producción

Config **T3**: θ calibrado por embedder/dominio (procedimiento de percentiles
documentado y automatizado en el harness) + LBB (ADR-0007) + fusibles VER
sobre cues de negación de cumplimiento. Los tres son ortogonales y cada uno
cierra una clase de fallo distinta (medido arriba).

## 6. Sellado

Los SHA-256 de `dataset_E2_corpus.json`, `eval_E2_results.json` y
`eval_E3_shadow.json` quedan registrados en `evidence_index.json` (encadenado)
y en `historiafable5.md` (ciclo 3).
