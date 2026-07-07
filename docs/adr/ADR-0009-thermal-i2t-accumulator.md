# ADR-0009 — Acumulador termico I2t (V7.7 Fusion, Fase 1)

**Estado:** aceptado — Gate A verde (9/9), suite completa 111 passed (baseline 102 + 9), kernel sellado sin diffs.
**Fecha:** 2026-07-07 · **TRACE_ID:** ARS-20260707-0002

## Decision
Se anade `antigravity_wings/antigravity_wings/thermal/accumulator.py`: un acumulador con
memoria y decaimiento exponencial que integra la senal puntual de `CCA.observe()` en el
tiempo, en vez de evaluarla como evento aislado.

- Energia por evento: `e_i = max(0, criticality - theta_ref)^2` (penaliza cuadraticamente
  la desviacion sobre el umbral; analogo a I^2).
- Acumulador por camino: `T_t = T_{t-1} * exp(-dt/tau) + e_i`.
- Al cruzar `T_trip` NO se corta: se emite `RecalibrationRequest` hacia el Arbitro (Fase 3).
- `trip_mode` distingue **spike** (la energia del evento solo ya cruza) de **accumulation**
  (hizo falta calor retenido de eventos previos).

## Por que
El gate puntual (Capa 1) no puede detectar fusion por acumulacion de eventos leves
sostenidos: cada uno pasa el gate individualmente. El acumulador cierra ese punto ciego
sin tocar el kernel sellado — consume solo escalares (`criticality`, `theta_ref`).

## Que se descarto / hallazgo
- **Descartado** disparar BLOCK directo al cruzar el umbral: viola el principio "redirigir,
  nunca cortar total" de V7.7. El acumulador solo *solicita* recalibracion.
- **Hallazgo de calibracion (verificado):** existe una temperatura de equilibrio para carga
  sostenida, `T_eq = e/(1 - exp(-dt/tau))`. Si `T_eq < T_trip`, una serie infinita de eventos
  leves NUNCA funde (disipacion == inyeccion). Esto es I2t real, no un bug: define una "carga
  sostenida segura" por fusible. La calibracion (tau, T_trip, theta_ref) es por-camino y debe
  ajustarse empiricamente en Fase 4 (Juez), no quedar sellada aqui.

## Alcance
Modulo nuevo aislado. No toca `core/kernel_1240421.py`, `core/frontier_v7.py`, `four_r2/`.
Aun NO conectado al enforcement (eso es Fase 3). Params por defecto tau=5.0, T_trip=0.30,
theta_ref=0.35 son de laboratorio, etiquetados **plausibles**, pendientes de calibracion real.
