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
