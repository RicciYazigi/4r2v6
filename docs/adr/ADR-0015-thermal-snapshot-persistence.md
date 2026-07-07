# ADR-0015 — Snapshot periódico del acumulador térmico (V7.8 Hardening, P1)

**Estado:** aceptado — Gate P1 verde (6/6), suite 137 passed, math sellado sin diffs.
**Fecha:** 2026-07-07 · **TRACE_ID:** ARS-20260707-0009

## Decision
`ThermalAccumulator` gana persistencia opcional: `snapshot_path`, `snapshot_every_events`,
`snapshot_every_seconds`. Guarda `{camino -> T, last_t}` + `saved_at` (wall-clock) a JSON con
escritura **atómica** (tmp + `os.replace`). Al arrancar carga el último snapshot aplicando
**decaimiento por Δt transcurrido** (`exp(-(now-saved_at)/τ)`) antes de seguir acumulando.

## Por que
`T_t` vivía solo en memoria del proceso: un reinicio (crash/deploy/OOM) borraba toda la memoria
de deriva sostenida. El snapshot acota el blast-radius de un reinicio a la ventana desde el
último guardado.

## Decisiones de diseño (honestidad)
- **Fail-safe, no fail-closed:** snapshot ausente o corrupto → arranca en cero **sin excepción**.
  Perder temperatura no es un riesgo de seguridad inmediato, es pérdida de contexto histórico.
- **Decaimiento en recarga con wall-clock:** implica que `τ` debe interpretarse en **segundos**
  para que el decaimiento de recarga sea físico. El decaimiento por-evento sigue usando el `t`
  lógico del caller; en recarga se pone `last_t=None` para no decaer dos veces.
- **Reloj inyectable (`now_fn`):** permite testear el decaimiento de recarga de forma
  determinista (sin `sleep`).
- **Alcance mínimo deliberado:** JSON local, no base distribuida ni sistema de eventos async
  (eso es la semilla v8 de la Fase 5 de V7.7). Es I/O periódico simple.

## Modelo de amenaza (explícito, no sobrevendido)
El escenario "atacante fuerza reinicio del sidecar para limpiar su historial térmico" asume que
puede forzar el reinicio (DoS) o sincronizarlo con un deploy/crash orgánico. Es real pero
**condicional** — no explotable en cada request como sí lo era la evasión de keywords (P0). Por
eso P0 fue antes; P1 acota, no elimina, este vector.
