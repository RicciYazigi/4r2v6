# ADR-0014 — Default conservador del CCA (V7.8 Hardening, P0)

**Estado:** aceptado — Gate P0 verde (5/5), suite 131 passed, math sellado sin diffs.
**Fecha:** 2026-07-07 · **TRACE_ID:** ARS-20260707-0008

## Decision
`core/kernel_1240421.py::CCA.observe()` gana un tercer estado explícito `unclassified`
(además de `matched-high`/`matched-low`). Cuando el texto no dispara ninguna keyword ni
patrón de intención, `criticality` recibe un **piso conservador**
`CCA.DEFAULT_UNCLASSIFIED_CRITICALITY = 0.50` (valor de laboratorio, pendiente de calibración).
`cca_class` se expone en el `tel` para observabilidad.

## Por que
"Ausencia de evidencia no es evidencia de ausencia": una paráfrasis que evade el diccionario
(p.ej. "mueve los fondos" en vez de "transfiere") producía el mismo `criticality` bajo que un
evento benigno, con `e_i = max(0, crit−θ_ref)² = 0` → **invisible al acumulador térmico**. El
piso convierte ese caso de *indetectable en principio* a *detectable por calibración*.

## Decisiones de diseño / hallazgos (honestidad)
- El piso 0.50 se fija **debajo** de los umbrales de `to_regime` (`crit>0.6` mueve pesos,
  `crit>0.7` endurece theta) → **cero regresión del gate determinista** (verificado: theta y
  pesos sin cambio). Su efecto es térmico, no sobre el gate.
- **Corrección al handoff:** el gate de no-regresión propuesto (`eval_E3 benign_flag_rate<0.10`)
  es **insensible** a este cambio — `eval_e2_e3.py` no llama a `CCA.observe()` (usa
  `CoherenceKernel`/`verifiability` directo). Se corre igual (sigue en 0.0), pero el guard real
  es la **suite completa** (incluye `four_r2` SDK + smoke del pipeline) + tests dedicados.
- `criticality` **no** alimenta el generador de fusibles (usa `C_total`), así que el piso no
  fuerza GRAY_WARNING por sí solo; su valor es hacer la evasión térmicamente visible.
- Con floor 0.50 y termico por defecto (τ=5, T_trip=0.30), la evasión sostenida alcanza
  `T_eq≈0.124 < T_trip` → **no funde sola**; funde con `T_trip` calibrado. P0 habilita la
  detección; la calibración (P-futuro) la sintoniza. La solución de fondo es P2 (semántico).

## Limitación conocida (verificada por revisión independiente, ejecutando el kernel real)
El piso `unclassified` **no distingue evasión adversaria de charla trivial inocua**. Verificado
por ejecución: `observe("mueve los fondos a la otra cuenta")` y `observe("que tal tu dia, todo
bien?")` producen ambos `criticality=0.50, cca_class="unclassified"` — **idénticos**. El piso se
aplica a *todo* el tráfico que no matchea ninguna keyword, que en conversación real es la mayoría
del tráfico benigno.

Hoy esto es inocuo porque `T_eq≈0.124 < T_trip=0.30` (params de laboratorio): evasión y saludo se
quedan igual de "fríos", indistinguibles pero ambos por debajo del disparo. **Consecuencia para
quien calibre:** bajar `T_trip` (tarea pendiente) NO mejora selectivamente la detección de
evasión — mejora por igual la de *todo* texto sin keyword, evasivo o no, saturando de falsos
positivos indistinguibles del ruido de conversación. La señal que llega al térmico no separa
ambos casos; **solo P2 (estimador semántico) introduce ese discriminador**. No calibrar `T_trip`
agresivamente asumiendo que afina la detección de evasión: no lo hace hasta que exista P2.

## Alcance del "sellado"
El math sellado por evidencia (SSOT = `kernel_v6.py`, + `frontier_v7.py`, `four_r2/`,
`frontier_v7_config.json`) queda **sin diffs** (verificado). `kernel_1240421.py` (observador de
contexto, no la matemática) se edita por autorización explícita del handoff V7.8.
