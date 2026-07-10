# E2/E3 — corrección de calibración (gap θ) + hallazgo de contribución del kernel

**Fecha:** 2026-07-10 · Harness: `scripts/eval_e2_e3_honest.py` (LSA determinista, seed 1240421).

## Qué se corrigió (gap #2)
El harness original (`eval_e2_e3.py`) derivaba `theta*` de los percentiles del **mismo
dato** que evaluaba y reportaba T2/T3 sobre **todo** el set = *fit-on-test*. La versión
honesta hace **split estratificado train/test 50/50**, ajusta el embedder LSA **solo en
train**, deriva `theta*` **solo de train** (0.4628) y reporta las métricas headline sobre
el split **TEST no visto**.

## Resultado del split honesto (TEST held-out, n=120)
| Métrica | Valor |
|---|---|
| AUROC on-vs-grave | 1.000 |
| AUROC on-vs-adversarial | 1.000 |
| T3 (θ*+LBB+VER-fuse): FPR_on / FNR_grave / veto_ADV | 0.0 / 0.0 / 1.0 |

El split **no cambia** los números perfectos. **Conclusión honesta #1:** el "AUROC 1.0"
NO era un artefacto de calibración — es que el corpus es **trivialmente separable**
(sintético/plantillas: los "graves" son off-topic evidente tipo *pizza/superhéroes*; los
adversariales contienen frases de bypass explícitas). Es validación de la **mecánica del
pipeline**, no de capacidad discriminativa. No debe presentarse como benchmark ni como
evidencia del motor.

## El hallazgo mayor (control de ablación)
Midiendo el veto adversarial de T3 **con** y **sin** el VER-fuse (cue de negación):

| Config sobre TEST adversarial | veto |
|---|---|
| T3 (con VER-fuse) | **100%** |
| gate de coherencia SOLO (sin fuse) | **0%** |

**Conclusión honesta #2:** el 100% de la detección adversarial lo hace el **detector
léxico de negación** (`verifiability_negation`, que capta "without verification",
"skipping two-factor", "no rollback", "failing tests" — puestas por construcción en las
plantillas). El **gate de coherencia del kernel aporta 0%** en esta tarea. Es el mismo
patrón medido en todo el ecosistema: la discriminación no emerge de la "física de
coherencia" sino de una capa léxica/keyword.

## Recomendación
- Usar `eval_e2_e3_honest.py` como calibración de referencia (no fit-on-test).
- En cualquier pitch: NO citar el "T3 AUROC 1.0 / veto 100%" como capacidad del motor.
  El framing honesto: *validación de mecánica de gating sobre corpus sintético; la
  detección adversarial la aporta el fusible de negación, no la coherencia*.
- Para una medida real: corpus no-templado + adversario que NO use las frases-cue, y el
  tier semántico (sentence-transformers) — es el gate v6.2 ya identificado.
