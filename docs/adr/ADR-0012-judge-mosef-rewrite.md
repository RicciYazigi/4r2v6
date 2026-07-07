# ADR-0012 — El Juez (MOSEF reescrito) (V7.7 Fusion, Fase 4)

**Estado:** aceptado — Gate C verde (5/5), suite 126 passed, kernel sellado sin diffs.
**Fecha:** 2026-07-07 · **TRACE_ID:** ARS-20260707-0005

## Red-team del apply_mosef original
`if psc["gravity"] > 0.8 and not psc["reversibility"]: return "BLOCK"`. Casos que rompe:
1. Devuelve BLOCK duro → viola "redirigir, nunca cortar".
2. `reversibility` binario y default True → prácticamente nunca disparaba.
3. Sin umbral de confianza → recalibraría ante cualquier pico (ruido).
4. Usa heurística nueva (`context['risk']`) en vez del acumulador térmico real (F1).

**Decisión: se REESCRIBE, no se extiende.**

## Decision
- Nuevo `Judge` en `dual_agents/arbiter.py`: consume la `RecalibrationRequest` del acumulador
  térmico (F1) y exige **confianza mínima** antes de emitir un token de escritura.
  Confianza = base(accumulation 0.5 / spike 0.4) + 0.3·corroboración_Luigi + 0.2·margen_sobre_T_trip.
  Umbral default 0.6.
- `ArbiterAuthority.write_fuse(fuse, params, token)` es la **única** vía de mutación de
  FuseSpec; sin token válido del Juez → `PermissionError`. Token de un solo uso.
- `OptionalPSC.apply_mosef` en `master.py` reescrito para delegar en el Juez (ya no bloquea).

## Que se descarto
- Confianza basada en `gravity` heurístico → reemplazada por señal térmica real.
- BLOCK como salida → el Juez autoriza/niega *recalibración*, no corta.
- Recalibrar por evento único de ruido → el umbral lo impide (test explícito).
