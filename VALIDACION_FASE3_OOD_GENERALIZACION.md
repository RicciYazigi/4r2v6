# Validación de generalización del detector C_NI (governance_mode) — OOD + adversarial

**Fecha:** 2026-07-09 · autor del set: co-arquitecto (out-of-distribution respecto a
Antigravity). Set: `experiments/ood_hard_eval.jsonl` — 42 triples (21/21), 8 dominios
NUEVOS (salud, trading, RRHH, infosec, legal, moderación, retención, compras, PII,
medicación), con 20 casos adversariales.

## Pregunta
El detector C_NI (distancia angular policy↔response) daba AUROC ~0.8 en el set curado
de Antigravity (50 muestras). ¿Generaliza a datos nuevos y a un adversario que redacta
la violación en el lenguaje de la política?

## Resultado
| Embedder | AUROC global | Casos DIRECTOS | Casos ADVERSARIALES |
|----------|--------------|----------------|---------------------|
| Léxico | 0.624 | 0.868 | 0.230 |
| Semántico | 0.628 | 0.810 | 0.350 |

## Lectura honesta
1. **Generaliza en lo directo:** en casos no-adversariales de dominios nuevos, AUROC
   0.81–0.87 — consistente con el 0.8 del set original. El detector es un filtro de
   primera pasada útil para cumplimiento de política "de buena fe".
2. **Se rompe ante el adversario:** cuando la respuesta VIOLA la política pero está
   redactada con su mismo vocabulario ("en cumplimiento de la política de retención,
   eliminé los registros…"), C_NI la ve "cerca" de la política y la deja pasar. AUROC
   0.23–0.35 = **peor que el azar (invertido)**: es engañable de forma sistemática.
   Simétricamente, un rechazo correcto redactado con lenguaje dramático/lejano se marca
   como violación (falso positivo).
3. Es una limitación **estructural** de "distancia de embeddings = coherencia", no de
   calibración: theta/pesos no lo arreglan. Es la misma vulnerabilidad de camuflaje ya
   vista en el proyecto (adversarial camouflage).

## Implicación (posicionamiento)
- El modo gobernanza es válido como **detector de primera línea para no-adversarios**.
- NO debe presentarse como robusto para un modelo de amenaza con adversario que conoce
  el mecanismo — que es justamente el threat model relevante para un guardrail.
- El set original de 50 daba 0.8 porque sus violaciones eran mayormente directas; el
  0.8 NO es un número de robustez adversarial.

## Límites del propio experimento
Adversarial n=20 (10/10) y directo n=22: N pequeño, IC amplio; pero el efecto es fuerte
y consistente entre léxico y semántico (ambos <0.5 en adversarial). Set autoral (yo),
etiquetas honestas; conviene ampliarlo si se quiere un número publicable.
