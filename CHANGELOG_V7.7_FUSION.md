# CHANGELOG — V7.7 "FUSION"

**Estado final:** DONE. 5 fases cerradas con gates en verde. Suite completa **126 passed**
(baseline 102 + 24 nuevos). `core/frontier_v7.py`, `core/kernel_v6.py`, `core/kernel_1240421.py`,
`four_r2/` y `evidence/frontier_v7_config.json` **sin diffs** (kernel sellado intacto).
Todo el trabajo vive en `antigravity_wings/`. Verificado por corrida real de tests, no narrativo.

**Origen:** handoff V7.7 "Fusion" 2026-07-07 (ARS-20260707-0001). Branch `v7-frontier-wip`.

## Definición de "hecho" — cumplida
- [x] 5 fases con sus gates en verde (A, B, B, C, C).
- [x] Suite completa (existente + nueva) en verde: 126 passed.
- [x] Kernel sellado sin diffs (verificado con `git diff --stat`).
- [x] CHANGELOG auditable (este archivo) + un ADR por fase (ADR-0009..0013).

## Baseline
Suite = **102 passed** antes de tocar nada. (Nota de entorno: el `.venv` del repo está
vacío/inaccesible desde el sandbox Linux; harness reproducible en `/tmp/pytools` con
`PYTHONPATH="/tmp/pytools:./core:./antigravity_wings:." python3 -m pytest -q`.)

## Fase 1 — Modelo térmico I²t  ·  Gate A ✅ (9 tests)  ·  ADR-0009
`antigravity_wings/thermal/accumulator.py`. Integra `CCA.observe()` en el tiempo con memoria y
decaimiento: `T_t = T_{t-1}·exp(-Δt/τ) + e_i`, `e_i = max(0, criticality-θ_ref)²`. Al cruzar
`T_trip` emite `RecalibrationRequest` (NO BLOCK). Distingue `spike` (pico único) de
`accumulation` (sostenido). Hallazgo verificado: existe temperatura de equilibrio
`T_eq = e/(1-exp(-Δt/τ))`; si `T_eq < T_trip`, carga sostenida nunca funde — I²t real, define
la "carga sostenida segura" por fusible. No toca el kernel.

## Fase 2 — Vector de reroute  ·  Gate B ✅ (4 tests)  ·  ADR-0010
`RerouteOption` + `RuntimeDecisionResponse.reroute_options` (aditivo, default vacío).
`DualRuntimeOperator(reroute_registry=...)` opt-in por nodo. Capa `_consult_reroute` separada de
la política pura de severidad: STOP con ruta registrada → ESCALATE + opciones; sin ruta → STOP
(fail-closed). Escenario guardia-perro-ambulancia verificado; la razón del bloqueo se conserva
en `reasons` (trazabilidad).

## Fase 3 — Desacople Mario/Luigi + Árbitro  ·  Gate B ✅ (4 tests)  ·  ADR-0011
`mario_decision`/`luigi_decision` dejan de estar duplicados: Luigi = lente canónica (pesimista),
Mario = lente optimista. `ArbiterAuthority.arbitrate` = regla conservadora (el más restrictivo
gana, nunca promedia) con `DisagreementRecord`. Desacuerdo expuesto en `meta`. Por construcción
`final == luigi == canónica` → cero regresión. Contradicción del handoff (dos "únicos escritores")
resuelta unificando en `ArbiterAuthority`.

## Fase 4 — El Juez (MOSEF reescrito)  ·  Gate C ✅ (5 tests)  ·  ADR-0012
Red-team del `apply_mosef` original (BLOCK duro, reversibility binario, sin umbral, heurística
ajena) → REESCRITO. `Judge` consume la `RecalibrationRequest` térmica y exige confianza ≥ umbral
(default 0.6) antes de emitir un token. `ArbiterAuthority.write_fuse` es el único mutador de
FuseSpec; sin token válido → `PermissionError`; token de un solo uso. Evidencia insuficiente
(ruido) NO recalibra (test explícito).

## Fase 5 — Desacople del hot path  ·  Gate C ✅ (2 tests)  ·  ADR-0013
`RecalibrationQueue`: el hot path solo encola (O(1)) y retorna; el arbitraje se procesa fuera de
línea vía `drain()`. **Decisión abierta reportada:** la infraestructura async real (worker de
fondo / cola persistente) se deja como **semilla de v8** por costo/riesgo sobre el hot path
síncrono; aquí se prueba el desacople lógico sin tocar la latencia del Gate determinista.

## Archivos nuevos / modificados (todo bajo antigravity_wings/, sin kernel)
Nuevos: `antigravity_wings/thermal/accumulator.py`, `thermal/__init__.py`;
`tests/test_thermal_accumulator.py`, `tests/test_reroute_vector.py`, `tests/test_dual_arbiter.py`,
`tests/test_judge_mosef.py`, `tests/test_recalibration_decoupling.py`;
`docs/adr/ADR-0009..0013`.
Modificados: `api/models.py` (+RerouteOption, +reroute_options), `operators/dual_runtime.py`
(reroute + desacople dual), `dual_agents/arbiter.py` (+ArbiterAuthority/Judge/RecalibrationQueue),
`orchestration/master.py` (apply_mosef reescrito).

## Etiquetado de veracidad
Garantías **matemáticas demostrables**: monotonía del ranking conservador; T_eq como suma
geométrica acotada; token de un solo uso. Garantías **empíricas con límites explícitos**: los
24 tests con seed fijo / N explícito. Parámetros `τ, T_trip, θ_ref, umbral_confianza` son de
laboratorio, etiquetados **plausibles**, pendientes de calibración empírica real por fusible.
