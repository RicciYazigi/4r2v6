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

---
---

# CICLO 5 — TRACE_ID: ARS-20260704-F5-0005 | Estado: OK

**Mandato:** README canónico en GitHub + sincronización final del repo público.

## Acciones
1. **README.md** promovido a quickstart v6.1.0 (contenido canónico de
   `README_top_level.md`); URL de clone apuntando a
   `https://github.com/RicciYazigi/4r2v6.git`.
2. **Push inicial completado** a `origin/main` (workspace completo, 290 archivos,
   historial preservado). CI disparado en el primer push.
3. **Revisión de archivos clave:** 14/14 presentes y no vacíos (kernel, ADRs,
   evals, evidence_index, CI, Makefile, docs de producción).

## Estado: repo público alineado con documentación v6.1.0

---
---

# CICLO 6 — TRACE_ID: ARS-20260704-F5-0006 | Estado: OK

**Mandato:** Handoff Grok ↔ continuidad de co-arquitectura + verificación independiente.

## Acciones (Grok Build, 2026-07-04)
1. **Re-validación local independiente** con venv: pytest **65/65 PASS**,
   selftest `perfect_c=0.0`, determinismo PASS (1e-12), E1/E4 veto 100%,
   E3 T3 0 incidentes, `make parity = 1`.
2. **Limpieza final:** `core/testperm.txt` y `core/_synctest.txt` eliminados;
   `.git/index.lock` ya no presente.
3. **E2/E3 re-corridos** — hashes actualizados y `evidence_index.json`
   regenerado (re-sellado post-validación).
4. **CI GitHub:** run #1 SUCCESS en push inicial; run #2 en curso post-README.

## Veredicto de continuidad
Los 5 ciclos Fable 5 + ciclo 6 Grok confirman: **v6.1.0 PRODUCTION-READY**.
No renombrar a v6.2 sin nueva evidencia — v6.2 = milestone (CI/ST, corpus
público HaluEval-style, tráfico real).

## Pendientes exclusivamente en host Ricci (no bloqueantes para pitch)
| # | Acción | Por qué |
|:-:|:-------|:--------|
| 1 | `pip install sentence-transformers && python scripts/eval_e2_e3.py` | Tier semántico ST (CI job `semantic-tier` lo hace en GitHub) |
| 2 | `docker compose build` en `4R2-MASTER-DELIVERY/systems/basic` | Validación contenedores (ND en sandboxes) |
| 3 | Piloto con tráfico real (v6.3 roadmap) | Shadow E3 ya pasó con 300 eventos simulados |
| 4 | Corpus HaluEval-style externo (v6.2 gate) | No presentar AUROC autorado como benchmark público |


---
---

# CICLO 7 — TRACE_ID: ARS-20260705-F5-V7-0001 | Estado: OK

**Mandato:** v6.1.0 -> v7.0 "Frontier". Formalizar y endurecer la defensa contra
el camuflaje de alta verificabilidad, sin romper el kernel congelado. Rama
`v7-frontier-wip`. Modelo: Claude Fable 5. Dirección: Richie.

## Acciones (todo verificado por ejecución en esta sesión)
1. **FASE 0 auditoría:** 65/65 tests base PASS; paridad réplicas = 1 hash;
   evidence_index coherente 5/5. Hallazgos: P1 fusible VER evadible por
   paráfrasis; P2 ADR-0001 sin marca de supersesión; P2 pyproject v4.0.0 vs
   kernel v6.1.0; Docker ND (sin binario en sandbox).
2. **FASE 1 núcleo (`core/frontier_v7.py`, opt-in, API v6 intacta):**
   - Fisher vs angular: **se mantiene angular**; control diagonal-Fisher sobre
     E2 real da ΔAUROC −0.0622 (empeora) => decisión evidenciada, no asumida.
   - H(x)=a·C_NR+b·C_RI+g·(1−C_IF), pesos calibrados por Fisher-LDA; cotas y
     monotonía probadas (T1). JS-camuflaje (reusa JS acotada del kernel) +
     entropía de Shannon (no Von Neumann) para OOD.
   - `frontier_verdict` = **escalación pura** (nunca relaja v6), probado.
   - 9 tests nuevos -> **74/74 PASS**. Añadidos a pytest testpaths y a CI.
3. **FASE 2 ataques reales (sellados):**
   - Hallazgo cuantificado del camuflaje: H(x) sobre magnitudes separa
     benigno-vs-grave AUROC 1.0 pero benigno-vs-adversarial 0.275 (≈azar) =>
     la defensa del adversarial es la verificabilidad con negación, no H.
   - E4-extendido (kernel real, geometría exacta): éxito del atacante
     100% (sólo gate) -> 78.9% (v6 LBB) -> **34.2% (v7 H)**; máxima brecha
     colable 0.99 -> 0.58 -> **0.229**. Cierre medido del camuflaje.
   - E5-OOD entropía: **resultado negativo honesto** (no detecta este ataque;
     queda como telemetría; escalación exige max_layer≥0.5 => 0 FP).
   - P1 endurecido: detector de negación paráfrasis-robusto. Evasión
     93.3% -> **0.0%**, 0 falsos positivos (probe n=15, límite léxico declarado).
4. **FASE 3 empaquetado:** `Dockerfile` + `self_test.py` (ENTRYPOINT).
   Self-test **exit 0** verificado localmente (7/7 checks). `docker build`
   **ND** (sin Docker en sandbox) — comportamiento probado por ejecución local.
5. **FASE 4 reporte:** `docs/FRONTIER_REPORT.md` con T1/T2 separados,
   comparación honesta vs Llama Guard / NeMo / CAI, y limitaciones nombradas.
   ADR-0001 marcado Superseded por ADR-0006. CI extendido con 5 pasos v7.

## Sellado ciclo 7
| Artefacto | SHA-256 |
|:----------|:--------|
| frontier_v7_config.json | `f97498ef8827c0fefdcf833f2bc7a0157f28f12913b1e9b7d2e503b67598756f` |
| frontier_calibration.json | `61b9bbf7667e32b4a184a8241aaa9dc580224a237e43dc85f8867aff2bbf661f` |
| eval_E4E5_results.json | `4d7469c3c74b3149df4cd6e7c9a1ddf0cf52fe104e8699ac111248a365897951` |
| eval_negation_hardening.json | `5786d04dfac4744f9444c4576eca3dc66e961c7f40e8fbbf7d44bb18227ad5cf` |

## Estado del workspace
Ejecutable, 74/74 verde, sin tests rojos. Rama `v7-frontier-wip` (no en main).
Commits/push: bloqueados desde el sandbox por permisos del mount .git — comandos
WSL entregados a Richie. Pendientes no bloqueantes: docker build en host, wiring
del detector de negación a producción, tier ST, corpus público, revisión legal.

## Nota de nueva ciencia acoplada
El valor de H(x) es geométrico y honesto: el atacante que diluye una brecha con
verificabilidad perfecta (C_IF->0) fuerza (1−C_IF)=1, que es justo el término
que H penaliza. No es física; es un funcional de penalización calibrado que
convierte la evasión del atacante en un dilema de Pareto medible.

**Confianza:** alta (T1 probado; T2 sellado con semilla fija).


---

## CICLO 7b — Revisión adversarial de Richie (2026-07-05) | Estado: OK

Richie **reconstruyó y ejecutó** el `selftest()` (no solo lo leyó) y probó
`h_energy` con casos que el reporte no aislaba. Halló una **vulnerabilidad
simétrica real**: el término `(1−C_IF)` de H(x) sube con la verificabilidad
genuinamente perfecta, así que un caso legítimo impecable (C_IF=0) puntuaba
como el atacante de camuflaje (que también fuerza C_IF=0). Crítica correcta.

**Verificado y corregido (no asumido):**
- `scripts/eval_high_verifiability_fpr.py` (nuevo): 120 casos legítimos de alta
  verificabilidad real (F=[1,1,1,1]) por el kernel real. H balanceado (g=1/3):
  **FPR 0.15** sobre el mejor tráfico, 0 veto adicional. H calibrado por Fisher:
  **g→0.0, FPR 0.0**, veto 1.0. El dato ya lo decía (E2 Fisher fijó g=0).
- `eval_e4_extended.py` corregido: H **calibrado** (no balanceado hard-coded).
  Headline: atacante 100%→34%, brecha máxima 0.99→0.23, **FPR alta-ver=0.0**,
  γ=0.0. Config balanceado **retirado**.
- 2 tests de regresión nuevos (11 en frontier, 76/76 total).
- `docs/ADRs/0008-...md` (nuevo) registra la decisión; **ADR-0001 revertido** a
  su original inmutable (respeta la convención: nuevo ADR, no reescritura).
- `self_test.py` + CI: chequean FPR alta-ver=0 y γ≈0. `evidence_index`: 10
  artefactos, coherente. §7 del reporte re-sellado y verificado.

**Lección:** el proyecto existe para cazar vulnerabilidades simétricas; esta se
cazó en revisión interna antes del merge, que es exactamente el patrón deseado.
No renombrar ni mergear a main hasta que Richie apruebe post-revisión.

**Confianza:** alta (T1 probado; T2 re-sellado con semilla fija; FPR del peor
caso medido en 0).


---
---

# CICLO 9 — TRACE_ID: ARS-20260706-F5-V7-PROD | Estado: OK

**Mandato:** integrar el MEGA DELIVERY v7.0.0 (capa de PRODUCTO, hecho con
Fable 5 antes de nuestro ciclo Frontier) al workspace, sin romper nada, y
fusionarlo con el trabajo Frontier ya existente. Español.

## A) Qué se integró (todo de alto valor, complementario al Frontier)
El MEGA vive en `four_r2/` (SDK) y NO toca el kernel congelado ni el
`core/frontier_v7.py`. Se creó verbatim:
- **SDK `four_r2/`**: `_version.py` (7.0.0 pkg / 6.1.0 kernel), `_kernel_loader.py`
  (importa el kernel canonico sin duplicarlo → paridad intacta), `embedders.py`
  (HashingEmbedder blake2b determinista + tier ST opcional), `guardrail.py`
  (facade fail-closed, nunca lanza), `calibration.py` (theta por percentiles con
  reporte honesto OVERLAP), `metrics.py` (Prometheus), `service.py` (sidecar
  FastAPI /health /v1/evaluate /metrics + auth X-API-Key), `__init__.py`.
- **Gate de coherencia** `scripts/check_release_coherence.py` (una sola historia
  de version, CI-gated).
- **Benchmark** `benchmarks/public_benchmark.py` + `METHODOLOGY.md` (calibracion
  held-out even/odd, acceptability E2-strict, SHA-256 encadenado).
- **Docs de rigor**: `LIMITATIONS.md` (T1/T2/no-claims), `THREAT_MODEL.md`
  (closed/mitigated/residual), `VERSIONING_POLICY.md`, `INTEGRATION.md`,
  `DATA_ROOM_CHECKLIST.md` (filas ND honestas). Todas fusionadas con referencias
  al Frontier (H(x), ambos ejes, ADR-0008).
- **Docker**: `Dockerfile.sidecar` (non-root, healthcheck) + `docker-compose.sidecar.yml`.
- **Tests**: `tests/test_sdk_guardrail.py` (15), `tests/test_service.py` (7),
  `tests/test_release_coherence.py` (1).
- **`examples/quickstart.py`**, `core/__init__.py`.
- **VER grounding fuse** (nivel producto): F[0]<0.15 ⇒ ALLOW→FLAG (piso empirico
  E2: benign min f_ground 0.214 vs adversarial 0.057). Cierra la clase
  "verifiability inflation" (THREAT_MODEL #2).

## B) Fusiones (preservando el trabajo Frontier — NO reemplazo ciego)
- `pyproject.toml`: version 4.0.0→7.0.0, deps declaradas, extras
  (service/semantic/dev). **testpaths incluye `scripts/test_frontier_v7.py`**
  (los 12 tests frontier NO se pierden).
- `README.md`(+`README_top_level.md`): release 7.0.0 + SDK/sidecar + **seccion
  Frontier** + mapa con `core/frontier_v7.py` y `docs/FRONTIER_REPORT.md`; ADRs 0001…0008.
- `.github/workflows/ci.yml`: pasos MEGA (coherence + benchmark) **Y** pasos
  Frontier (calibracion, camuflaje ambos ejes, high-ver FPR, negacion, self-test,
  re-sello). Un solo pipeline.
- `Makefile`: targets `coherence`, `benchmark`, `sidecar` (TABs correctos).
- `CHANGES.md`: entrada v7.0.0 al inicio.

## C) Verificacion por ejecucion (2026-07-06, todo real)
| Control | Resultado |
|:--------|:---------|
| `pip install -e ".[service,dev]"` | OK (four_r2 7.0.0 / kernel 6.1.0) |
| `check_release_coherence.py` | RELEASE COHERENCE: PASS |
| `pytest -q` | **99 passed** (65 core + 22 SDK/service + 12 frontier) |
| `make parity` | 1 |
| determinism harness | PASS (sin fuentes de no-determinismo) |
| `public_benchmark.py` | acceptability 1.0, theta* 0.3971, benign ALLOW 1.0, FNR 0.0, veto 1.0 — reproduce el §D del MEGA (solo difiere latencia por hardware) |
| `self_test.py` (frontier) | exit 0 |
| `quickstart.py` | benign ALLOW / attack FLAG / broken BLOCK(fail-closed) |
| evidence_index | 11 artefactos, coherente (incluye benchmark_v7_results.json) |

Nota honesta de conteo: el MEGA declaraba 87/87 (fue escrito antes del Frontier);
el numero REAL con Frontier integrado es **99/99**. Se reporta el real, no el del documento.

## D) Docker
`docker build`/`compose` siguen **ND** en el sandbox (sin binario). Verificar en
host con `docker compose -f docker-compose.sidecar.yml up -d && curl localhost:8472/health`.

## E) Memoria
```json
{
 "hechos": [
  "v7.0.0 producto: SDK four_r2/ (Guardrail fail-closed, sidecar FastAPI, metrics Prometheus)",
  "99/99 tests (65 core + 22 SDK + 12 frontier); coherence PASS; parity 1; benchmark acceptability 1.0 theta 0.3971",
  "VER grounding fuse F[0]<0.15 cierra verifiability-inflation; kernel math CONGELADO 6.1.0",
  "MEGA producto + Frontier integrados sin romper nada; evidence_index 11 artefactos"
 ],
 "decisiones": [
  "Kernel math NO se bumpea (6.1.0 sellado); package 7.0.0; check_release_coherence lo enforce",
  "testpaths incluye frontier + tests SDK; CI corre ambos gates",
  "Docs LIMITATIONS/THREAT_MODEL fusionan producto + frontier; filas ND honestas en DATA_ROOM"
 ],
 "tareas": [
  "Richie: correr el bash unico de push WSL (rm lock, add -A, commit, tag v7.0.0, push)",
  "Richie: docker compose sidecar en host (ND en sandbox)",
  "Roadmap: corpus externo via --corpus, opinion legal EU AI Act, tier ST en CI"
 ]
}
```
**Confianza:** alta (todo verificado por ejecucion; benchmark reproduce el §D
salvo latencia). Kernel congelado intacto; paridad 1; nada roto.
