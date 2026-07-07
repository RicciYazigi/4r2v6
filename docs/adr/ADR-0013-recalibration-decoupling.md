# ADR-0013 — Desacople del hot path (V7.7 Fusion, Fase 5)

**Estado:** aceptado (semilla) — Gate C verde (2/2), suite 126 passed, kernel sellado sin diffs.
**Fecha:** 2026-07-07 · **TRACE_ID:** ARS-20260707-0006

## Decision
`RecalibrationQueue` en `dual_agents/arbiter.py`: el hot path (Gate determinista + acumulador
térmico) solo **encola** la `RecalibrationRequest` en O(1) y retorna; el arbitraje/Juez se
procesa fuera de línea vía `drain(handler)`. Encolar NO ejecuta el arbitraje (test explícito)
y es mucho más barato que el procesamiento completo.

## Decision abierta reportada (alcance)
NO se introducen hilos, procesos ni cola distribuida. La infraestructura async real (worker de
fondo, cola persistente/IPC) tiene costo/riesgo alto sobre el hot path síncrono actual y se deja
como **semilla de v8**. Esta fase prueba el desacople *lógico* sin arriesgar el hot path.

## Por que
El Gate determinista (Capa 1, `core/frontier_v7.py`) debe mantener su orden de magnitud de
latencia sin bloquear a la espera del loop de fondo. La cola garantiza ese desacople sin que
el kernel dependa de infraestructura nueva.
