# ADR-0010 — Vector de reroute (V7.7 Fusion, Fase 2)

**Estado:** aceptado — Gate B verde (4/4), suite completa 115 passed, kernel sellado sin diffs.
**Fecha:** 2026-07-07 · **TRACE_ID:** ARS-20260707-0003

## Decision
Un fusible que salta deja de terminar necesariamente en STOP puro.
- Nuevo modelo `RerouteOption` en `api/models.py` (route_id, description, preserves_need,
  estimated_friction, target_node, metadata).
- `RuntimeDecisionResponse` gana `reroute_options: List[RerouteOption]` — **aditivo, default
  vacio**: consumidores previos del schema no se rompen.
- `DualRuntimeOperator` acepta un `reroute_registry: Dict[node_id, List[RerouteOption]]`
  **opt-in** (default `{}`). Nueva capa `_consult_reroute()`: si la politica base es STOP y hay
  ruta registrada para el nodo -> `ESCALATE` + opciones; si no hay ruta -> STOP se mantiene.

## Por que
El escenario guardia-perro-ambulancia (necesidad innegociable + camino bloqueado) exige
preservar la intencion original via ruta alternativa en vez de cortar en seco. STOP puro es
correcto como *default* seguro, no como *unica* salida.

## Que se descarto / decisiones de diseno
- **Descartado** mutar `_apply_enforcement_policy()` para mezclar severidad->decision con
  logica de reroute. El mapeo severidad->decision es el nucleo fail-closed y debe seguir
  auditable de forma aislada. El reroute vive en una capa separada (`_consult_reroute`)
  encima de la politica pura. (El handoff pedia "extender" la policy; se extendio el *flujo*
  de enforcement, no la funcion pura — se documenta la desviacion deliberada.)
- **Descartado** downgrade STOP->GO: seria abandonar fail-closed. Se eligio STOP->ESCALATE:
  no es corte en seco pero exige decision/escalada, coherente con "reroute = ruta alternativa
  que preserva la necesidad, con supervision".
- **Opt-in por nodo**: sin registro, el comportamiento es identico al previo (STOP puro). El
  wiring real del registro (quien puebla las rutas) es del Arbitro/Juez, Fases 3-4.

## Alcance
`mario_decision`/`luigi_decision` SIGUEN duplicados a proposito — su desacople es Fase 3, no
esta fase. No se toca el kernel sellado.
