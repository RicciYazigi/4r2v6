# historiafable5.md — Bitácora Canónica del Ciclo Fable 5

**TRACE_ID:** ARS-20260704-F5-0001 | **Estado:** OK
**Fecha:** 2026-07-04 | **Modelo:** Claude Fable 5 (co-arquitecto del guardrail de coherencia)
**Dirección humana:** Richie | **Repo:** `4R2 repo maestro jul2026`
**Alcance:** Auditoría milimétrica end-to-end + corrección de gaps P0 + recalibración matemática + validación completa + sellado.

---

## A) Resumen ejecutivo (verificado)

El kernel canónico había migrado a la matemática v6 (métrica angular) **después**
del informe de cierre del 2026-07-03, dejando specs, umbrales y salvaguardas
calibrados para la escala anterior (`1 − cos`). Esta sesión detectó y corrigió
**3 vulnerabilidades P0 reales**, cerró 5 gaps doc↔código, recalibró todos los
umbrales del ecosistema a la escala angular, sincronizó las 4 réplicas del
kernel y re-validó todo el flujo end-to-end: **65/65 tests, determinismo
criptográfico PASS, pipeline 100% real (0 mocks)**.

Todo lo afirmado aquí está **verificado** por ejecución en esta sesión
(pytest + 5 scripts E2E + probes numéricos). Nada es especulativo.

---

## B) Hallazgos (auditoría milimétrica)

### P0 — Vulnerabilidades de seguridad corregidas

**P0-1. Blind-spot de clip silencioso en C_IF.**
`compute_C_IF` hacía `clip(physical, 0, 1)`. Telemetría cruda
`[900, 8, 50, 10]` → `[1,1,1,1]` → `C_IF = 0.0`: *certificado falso de
coherencia física perfecta* para cualquier caller con la convención legacy de F
(todos los tests raíz y varios scripts de producción la usan).
Evidencia pre-fix: escenario ADR-0005 daba `C_IF=0.0000, C_total=0.2500` (GREEN).
Post-fix: `C_IF=0.2477, C_total=0.3326` (GRAY → fusible GRAY_WARNING).

**P0-2. Umbral del gate en la escala equivocada.**
`Regime.theta` default `0.75` provenía de la escala `1 − cos` [0,2], pero el
gate v6 opera en escala angular [0,1] (ortogonal = 0.5). Resultado: el
Hard-Gate dejaba pasar prácticamente todo. Corregido a `0.35` (canon v6), con
mapeo formal `d_new = arccos(1 − d_old)/π`.

**P0-3. Inversión direccional en modo CRITICAL.**
`intent_level="CRITICAL"` ejecutaba `theta += 0.1` — **relajaba** el gate
exactamente cuando debía endurecerlo. Igual en `CCA.to_regime`
(crit>0.7 → θ=0.95, el más permisivo). Corregido: CRITICAL ⇒
`θ = max(0.15, θ − 0.10)`; CCA crítico ⇒ θ=0.25 (efectivo 0.15 por
composición con v6 — endurecimiento doble intencional, documentado).
Evidencia post-fix: `cca_and_promotion.py` → "Con régimen crítico:
C_total=0.1757, pasa_gate=**False**" (antes pasaba).

### Gaps doc↔código cerrados

**G-1.** CANON_SPEC/ADR-0001/informe documentaban `C_IF` coseno-pad y rangos
[0,2]; el código real usaba `1 − mean(clip(F))`. Resuelto con el **dual-path**
(ADR-0006 D2) + reescritura de CANON_SPEC a v6.0.1.
**G-2.** `CoherenceKernel.PHYSICS_PRIORITY_PROFILE` prometido por ADR-0005 y
CANON_SPEC §7 **no existía en el código**. Añadido registro completo
`WEIGHT_PROFILES` (balanced / physics_priority / normative_priority /
regime_default).
**G-3.** Zonas operativas (GREEN/GRAY/RED = 0.35/0.65) y decisión GO
(`< 0.65`) sin recalibrar a la nueva escala. Recalibradas: GREEN < 0.28,
GRAY 0.28–0.39, RED > 0.39 (severity critical > 0.55), GO < 0.39.
**G-4.** Números de verificación de ADR-0005 (esperaban `C_NR≈1.0` para
vectores ortogonales) inválidos en escala angular (ortogonal = 0.5). Enmienda
añadida a ADR-0005; garantía de seguridad recomputada: brecha antipodal
aporta ≥ 1/3 ⇒ nunca GREEN (caso canónico medido: 0.6667 ⇒ RED/BLOCK).
**G-5.** Réplicas del kernel: sincronizadas 4/4 a un único SHA-256 y
`__pycache__` purgado (ver §F).

### Evaluación de lo que NO se tocó (decisión razonada)

- `measure_coherence_with_keys`: contrato API congelado (Frozen Contract,
  test_p1_hardening) — sin cambios.
- `kernel_v6.py`: matemáticamente sólido (métrica verdadera, JS acotada,
  fail-closed, simplex interno). Es la fuente de verdad; el wrapper se alineó
  a él, no al revés.
- BeliefTracker (log-odds pooling κ=0.7/0.4 + decaimiento Ebbinghaus),
  CalibratedEvaluator (Platt centrado) y DomainKernel: correctos y testeados.
- `kernel_1240421_old_broken.py` permanece en `core/` solo como referencia
  histórica (candidato a `archive/` en el próximo ciclo; no se eliminó para
  preservar trazabilidad del ledger de versiones).

---

## C) Cambios aplicados (diff lógico)

| # | Archivo | Cambio |
|:-:|:--------|:-------|
| 1 | `core/kernel_1240421.py` | v6.0.1: dual-path C_IF; `_verifiability_proxy`; θ default 0.35; CRITICAL endurece (−0.10, piso 0.15); CCA θ 0.25/0.35; registro `WEIGHT_PROFILES`; docstring de versión |
| 2 | `4R2-MASTER-DELIVERY/systems/basic/packages/kernel/kernel_1240421.py` | réplica sincronizada (mismo SHA) |
| 3 | `4R2-MASTER-DELIVERY/systems/enhanced/packages/kernel/kernel_1240421.py` | réplica sincronizada |
| 4 | `4R2-MASTER-DELIVERY/tests/kernel_1240421.py` | réplica sincronizada |
| 5 | `antigravity_wings/.../orchestration/master.py` | θ fallback 0.75 → 0.35 |
| 6 | `antigravity_wings/.../fuse_config/generator.py` | zonas GRAY 0.28–0.39, RED > 0.39, critical > 0.55 |
| 7 | `scripts/cca.py` | θ crítico 0.95→0.25, base 0.75→0.35 |
| 8 | `scripts/end_to_end_validation.py` | GO < 0.65 → GO < 0.39 |
| 9 | `docs/ADRs/0006-angular-metric-and-dual-path-cif.md` | **nuevo** — decisión formal completa |
| 10 | `docs/CANON_SPEC.md` | reescrito a v6.0.1 (fórmulas exactas, zonas, evidencia) |
| 11 | `docs/ADRs/0005-weights-consolidation.md` | enmienda 2026-07-04 (números de verificación) |
| 12 | `README.md` | ledger actualizado a v6.0.1 |
| 13 | `historiafable5.md` | **este archivo** |

Nota operativa: durante la sesión se detectó un desfase de caché del mount
Windows↔sandbox que truncaba vistas de archivos recién editados; se resolvió
re-escribiendo los archivos completos y verificando `compile()` + tamaño antes
de cada paso de validación. Ningún archivo quedó en estado parcial (verificado
por pytest y por compilación explícita).

---

## D) Experimentos y métricas (hipótesis | métrica | criterio | resultado)

| Experimento | Métrica | Criterio | Resultado |
|:------------|:--------|:---------|:----------|
| Suite completa | pytest | 65/65 | ✅ **65 passed** (1.36s) |
| Selftest kernel | perfect_c / dirección de Loss | 0.0 / L_bad > L_perfect | ✅ `{perfect_c: 0.0, bad_c: 0.5833, loss_correct_direction: True}` |
| Selftest v6 | ALL_PASS | True | ✅ True |
| P0-1 cerrado | C_IF con F crudo | > 0 y sensible a desalineación | ✅ 0.2477 (escenario ADR-0005), 0.3210 (ejemplo docker) |
| P0-3 cerrado | θ CRITICAL | < θ base | ✅ 0.25 (CCA) / 0.15 efectivo; caso crítico ahora **pasa_gate=False** |
| Brecha antipodal | C_total | ≥ 0.333 (nunca GREEN) | ✅ 0.6667 → RED/BLOCK |
| E2E canónico | C_total / gate | GO coherente | ✅ C_total=0.2952 → GO (< 0.39) |
| Brutal E2E | mocks en camino crítico | 0 | ✅ "100% REAL - NO MOCKS"; motor `canonical-5.2-local-real` |
| Determinismo | 20 runs, tol 1e-12 | bit-idéntico | ✅ PASS; ver hashes §F |
| Pilotos | ASYM veto + fusibles | VETO en EXISTENTIAL+PASSIVE | ✅ PASSED |
| Réplicas | SHA-256 únicos | 1 | ✅ 1 hash (4 copias) |

Riesgos residuales: P1 — endurecimiento del gate puede aumentar falsos
positivos (FLAG) en pilotos con C_total 0.28–0.39; mitigación: banda FLAG
(θ+0.15) escala a revisión, no a bloqueo. P2 — deprecations cosméticas
(FastAPI `on_event`, `utcnow()`); sin impacto matemático ni de seguridad.

---

## E) Fórmulas canónicas vigentes (v6.0.1)

```
d(a,b)      = arccos(clip(â·b̂, −1, 1)) / π                ∈ [0,1]
C_NR        = d(N, R) ;  C_RI = d(R, I)
C_IF        = 1 − mean(F)            si F ∈ [0,1]^4  (verificabilidad)
            = d(pad(Î), pad(F̂))      si F es telemetría cruda (legacy)
C_total     = Σ w_j · C_j  ,  w en el simplex, default (1/3,1/3,1/3)
R_irr       = JS(π_t ‖ π_{t−1})                            ∈ [0, ln 2]
L_4R2       = base + α·max(0, C_total)² + γ·R_irr + δ·K_contra
Gate        : ALLOW ≤ θ | FLAG ≤ θ+0.15 | BLOCK resto ; θ=0.35 ; fail-closed
CRITICAL    : θ ← max(0.15, θ − 0.10)   (endurece, jamás relaja)
Zonas       : GREEN < 0.28 | GRAY 0.28–0.39 | RED > 0.39
Mapeo legacy: d_new = arccos(1 − d_old) / π
```

---

## F) Sellado criptográfico

(Los SHA-256 finales del kernel y de la evidencia de determinismo se anexan al
final de este archivo por el paso de sellado automatizado.)

- Determinismo (kernel numérico): `513f3d9bcab8341354971fd56df170679c3081caef2539e91ee8db43320fef7d`
- Determinismo (pipeline scores): `676d2452e30bedf8158e98ffa89f659b9a3b4032d0d3937e8d0e5e8c5b479457`
- Evidencia sellada: `9dc7de6d65f0428f74a79c2a6f42c3f4e8539f3538c7776b7770564f47db68e3`

---

## G) Próximos pasos (≤3) + decisiones a confirmar

1. **Mover `core/kernel_1240421_old_broken.py` a `archive/`** y regenerar
   `evidence_index` encadenado con los hashes de este ciclo.
2. **Recalibrar el ejemplo de zonas del deck de compradores y el draft arXiv**
   a la escala angular (misma tabla de §E) antes de cualquier data-room.
3. **Piloto de regresión de falsos positivos**: correr los 2 pilotos
   (insurance/chatbot) contra la banda FLAG 0.35–0.50 y fijar θ por dominio
   si la tasa de FLAG > 10%.

Decisión a confirmar por Richie: ¿se archiva definitivamente la escala
`1 − cos` (borrar ejemplos legacy de ADR-0001) o se mantiene como apéndice
histórico? Recomendación: apéndice histórico (trazabilidad para due diligence).

---

## H) Memoria

```json
{
  "hechos": [
    "Kernel canónico = wrapper v6.0.1 sobre kernel_v6 (métrica angular, fail-closed)",
    "3 P0 corregidos: clip silencioso C_IF, theta 0.75 en escala errónea, CRITICAL relajaba el gate",
    "Zonas recalibradas: GREEN<0.28, GRAY 0.28-0.39, RED>0.39; gate theta=0.35; mapeo arccos(1-x)/pi",
    "65/65 tests, determinismo PASS (20 runs, 1e-12), 0 mocks en camino critico, 4 replicas 1 hash"
  ],
  "decisiones": [
    "ADR-0006 aceptado: metrica angular canon + dual-path C_IF + recalibracion de gate",
    "WEIGHT_PROFILES registrado en el kernel (cumple ADR-0005)",
    "kernel_v6.py intacto como fuente de verdad matematica",
    "measure_coherence_with_keys sin cambios (Frozen Contract)"
  ],
  "tareas": [
    "Archivar kernel_1240421_old_broken.py y regenerar evidence_index",
    "Actualizar deck/arXiv a escala angular",
    "Regresion de falsos positivos FLAG en pilotos"
  ]
}
```

---

**I) Confianza:** alta (todo verificado por ejecución en esta sesión).

*Salida de un pipeline orquestado ('ARQ Orchestrator – Modo Arsenal') sobre un
LLM. Agregación multi-rol validada por veracidad, privacidad y gates (A/B/C).
Dirección humana: Richie.*

---

## Anexo de sellado (automatizado, 2026-07-04)

| Artefacto | SHA-256 |
|:----------|:--------|
| kernel_1240421.py (4 réplicas, 1 hash) | `a664334546f297b592d0c9325e4384c6443737830f1a5f3f2bce8cd5cde0926b` |
| kernel_v6.py | `faeb964ea38f941facb588dd29307425cbf073d49fc67a09971af9ee549eedc6` |
| CANON_SPEC.md v6.0.1 | `5f7872077d629f3b2c955cade54254d88fcb82fa8fadd6540656aea9128ad4bc` |
| ADR-0006 | `a7cb94d68ac0883ed52a722dc9fe2a67db458a234103b7a9459fee2f7bd90b97` |

---
---

# CICLO 2 — TRACE_ID: ARS-20260704-F5-0002 | Estado: OK

**Mandato:** cierre total production-ready (prompt Grok evaluado; decisiones propias autorizadas por Ricci).

## Decisión de arquitectura sobre el prompt de Grok
Se ejecutó el fondo (evals, limpieza, migración, whitepaper, roadmap) pero NO
el renombre a "v6.2" sin evidencia: el freeze probado es **v6.1.0** y v6.2
queda como milestone en ROADMAP_DEFINITIVO.md. Grok afirmaba "commit de
ADR-0006 realizado": verificado (72dad8b) — correcto.

## Acciones e hallazgos del ciclo
1. **ADR-0007 — Layer Breach Breaker.** Hallazgo estructural propio: con pesos
   1/3, ninguna capa puede superar C_total=0.35 (dilución convexa) ⇒ ataques
   de capa única pasaban el gate. Confirmado por E4: veto crudo 50% (A1
   camuflaje normativo 0/20, A4 inflación de verificabilidad 0/20).
   Fix: max(C_NR,C_RI)≥0.75⇒BLOCK; ≥0.60⇒FLAG. Post-fix: veto 100%.
2. **Bug fail-closed del wrapper.** El eval E4-A3 (zero-vector) crasheaba el
   wrapper (KeyError C_total) — un guardrail que lanza excepción no es
   fail-closed. Fix: resultado v6 sin C_total ⇒ 1.0/BLOCK/breakdown vacío.
3. **Dataset E1** (300 casos, 4 dominios, semilla 1240421, ground-truth
   geométrico exacto) + **eval E1/E4**: FPR 0.0 (n=100), FNR 0.0 (n=60),
   veto adversarial 100% (n=80). Sellado SHA-256.
4. **Migración test_pilot_contexts.py** a F∈[0,1]⁴ + regresión anti
   silent-clip (C_IF legacy 0.3210 > 0 verificado).
5. **Limpieza:** kernel_1240421_old_broken.py → archive/; evidence_index.json
   regenerado (generador parcheado para Python 3.10: datetime.UTC).
6. **Kernel v6.1.0** estampado y re-sincronizado 4/4 réplicas → 1 hash.
7. **Docs producción:** ADR-0007, ROADMAP_DEFINITIVO, arXiv_submission_v6,
   FINANCIAL_SCENARIO (especulativo, sin cifras inventadas), SALES_STRATEGY,
   MEGA_DELIVERY_v6.1, CANON_SPEC §9, README ledger v6.1.0.
8. **Docker: ND** (sin Docker en sandbox). Plan exacto en MEGA_DELIVERY §5.
9. Revalidación total: pytest 65/65 · determinismo PASS · brutal 100% real ·
   pilotos PASS.

## Sellado del ciclo 2
| Artefacto | SHA-256 |
|:----------|:--------|
| kernel v6.1.0 (4 réplicas, 1 hash) | `24c7b26c6752a3fbc9bb506c314191e12c518b2d133ee46dd8144fc2e3c7af9f` |
| dataset_E1.json | `da23cad533ffbf8290bc25ef1d33ae8b665b985ae9b0d162d1c35ff4627b2f6e` |
| eval_E1_E4_results.json | `de6056dbd699ccb43ff1ea7cbc73b6a8ea9841c418253363f4820f6091e91c43` |
| evidencia determinismo | `9dc7de6d65f0428f74a79c2a6f42c3f4e8539f3538c7776b7770564f47db68e3` |

Mensaje de commit sugerido si el lock persiste:
feat(security): v6.1.0 ADR-0007 Layer Breach Breaker + fail-closed wrapper; evals E1/E4 (veto 50%->100%); production docs package

---
---

# CICLO 3 — TRACE_ID: ARS-20260704-F5-0003 | Estado: OK

**Mandato:** E2 con embeddings reales + E3 piloto sombra + cierre 100% production-ready.

## Acciones y hallazgos
1. **E2 ejecutado con embedder real** (LSA TF-IDF+SVD k=64 puro numpy,
   determinista, cero mocks; el harness auto-detecta sentence-transformers y
   se auto-mejora en un host con torch — ND en sandbox, declarado).
   Corpus: 240 casos de texto real, 4 dominios × 4 clases. F extraída de
   rasgos reales de la respuesta, incluida **negación de cumplimiento**.
2. **Hallazgo de calibración:** θ=0.35 (régimen sintético) quedó descalibrado
   para LSA (FPR 8.3%). Procedimiento de calibración por percentiles
   automatizado: θ* = 0.4625.
3. **Hallazgo de defensa en profundidad (medido por tiers):**
   T1 gate default: veto adversarial 75%. T2 solo calibrado: veto 0%.
   **T3 (θ* + LBB + fusible VER): FPR 0.0, FNR 0.0, veto 100%, aceptable 1.0.**
   AUROC on-vs-grave 1.0; on-vs-adversarial 0.80 sin F negation-aware → 1.0
   con ella (la verificabilidad es capa de señal indispensable).
4. **E3 piloto sombra:** 300 eventos (70/15/10/5), modo log-only, config T3:
   **0 incidentes**, FLAG benigno 0.0% (<10%), latencia media 0.124 ms /
   p95 0.164 ms (afirmación sub-ms ahora MEDIDA).
5. **Piloto insurance re-verificado** post-v6.1.0: veto en caliente OK.
6. Limpieza: __pycache__/.pytest_cache purgados y añadidos a .gitignore.
   core/testperm.txt y core/_synctest.txt: bloqueados por permisos del mount —
   borrar a mano en Windows (única basura restante).
7. Docs sincronizados: docs/E2_E3_REPORT.md (nuevo), ROADMAP (E2-lex/E3-sim
   marcados hechos con alcance declarado), MEGA_DELIVERY §7 addendum, README.
8. evidence_index.json regenerado (5 artefactos E1+E2+E3 encadenados).
9. pytest 65/65 · réplicas 4/4 un hash · determinismo previo vigente.

## Sellado ciclo 3
| Artefacto | SHA-256 (32) |
|:----------|:-------------|
| dataset_E2_corpus.json | `e16d05ba8703c805f9b2b85518c5f745` |
| eval_E2_results.json | `c4fd0763eab3531e4730c6a1e5102b8d` |
| eval_E3_shadow.json | `9ed3764f79b58e03b5e25c24040e4732` |

## Estado final del workspace
PRODUCTION-READY con 2 acciones manuales de Ricci: (1) `del .git\index.lock`
+ commit; (2) `docker compose build` en host. Pendientes de roadmap (no
bloqueantes): E2-st en host con torch, piloto con tráfico real, CI.

---
---

# CICLO 4 — TRACE_ID: ARS-20260704-F5-0004 | Estado: OK

**Mandato:** consolidación final del workspace para GitHub + pitch Big Tech.

## Acciones
1. **Checklist ciclo 1-3:** 21/21 archivos clave verificados presentes y no vacíos.
2. **E2-st (sentence-transformers): ND en sandbox** (torch ~900MB excede el
   entorno; 2 intentos, declarado). Resolución arquitectónica: el CI incluye el
   job `semantic-tier` que instala sentence-transformers, corre el MISMO
   harness `scripts/eval_e2_e3.py` (auto-detecta el backend) y sube
   `eval_E2_results.json` como artifact — **los números ST se generan solos en
   el primer push a GitHub**, o en host local con
   `pip install sentence-transformers && python scripts/eval_e2_e3.py`.
3. **CI creado:** `.github/workflows/ci.yml` — pytest + paridad de hashes de
   las 4 réplicas (falla si ≠1) + determinismo + E1/E4 (exige veto 1.0) +
   E2/E3 (exige 0 incidentes) + selftest (exige perfect_c=0.0) + job ST opcional.
4. **README_top_level.md:** setup 60s, quickstart de verificación completa,
   ejemplo de uso mínimo, make targets, mapa del repo, regla de evidencia.
5. **Makefile:** targets locales sin docker (test-local, evals, determinism,
   parity).
6. **ROADMAP:** tabla de milestones consolidada (v6.1.0 CERRADO → v6.2 CI/ST →
   v6.3 tráfico real → v7 SDK/arXiv/data-room).
7. **evidence_index.json final** regenerado con E1+E2+E3 encadenados.
8. Validación final: pytest 65/65 · make parity = 1 · workspace limpio.

## Nota de honestidad para el pitch
Corpus público (HaluEval-style) adaptado a NRIF: NO ejecutado aún (requiere
descarga externa) — está en el gate de v6.2 junto con E2-st. No presentar
AUROC del corpus autorado como si fuera de benchmark público.

## Estado: workspace GitHub-ready
Comandos finales de Ricci (Windows):
  del .git\index.lock & del core\testperm.txt & del core\_synctest.txt
  git add -A && git commit -m "feat: v6.1.0 consolidated - E2/E3 evals, CI, README, roadmap"
  git remote add origin <URL> && git push -u origin main
El primer push dispara el CI: 6 checks core + números sentence-transformers.
