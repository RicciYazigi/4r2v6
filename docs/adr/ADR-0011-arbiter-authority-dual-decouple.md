# ADR-0011 — Árbitro autoridad + desacople Mario/Luigi (V7.7 Fusion, Fase 3)

**Estado:** aceptado — Gate B verde (4/4), suite 126 passed, kernel sellado sin diffs.
**Fecha:** 2026-07-07 · **TRACE_ID:** ARS-20260707-0004

## Decision
- `mario_decision`/`luigi_decision` dejan de ser el mismo valor duplicado. Luigi = lente
  PESIMISTA = política canónica de severidad (cota conservadora). Mario = lente OPTIMISTA
  (solo detiene ante `critical`; el resto lo lee como GO).
- Nuevo `ArbiterAuthority.arbitrate(mario, luigi)` en `dual_agents/arbiter.py`: regla
  **conservadora** (el más restrictivo gana, ranking GO<DEGRADE<ESCALATE<STOP), **nunca
  promedia**. Devuelve `DisagreementRecord` con el desacuerdo preservado.
- El desacuerdo se expone en `RuntimeDecisionResponse.meta` (`dual_disagreement`,
  `mario_position`, `luigi_position`, `arbiter_rule`).

## Por que
Por construcción `mario_rank <= luigi_rank`, así que `final == luigi == política canónica`
→ **cero regresión** en la decisión final, pero ahora el desacuerdo es real y trazable. El
disenso de Mario (GO donde el sistema hizo STOP) es justamente la señal de "fusible
potencialmente sobre-restrictivo" que alimenta el reroute (F2) y la recalibración (F4).

## Que se resolvio / descarto
- **Contradicción del handoff resuelta:** F3 pedía "Árbitro = único escritor de FuseSpec" y
  F4 "Juez = único escritor". Se unifican en `ArbiterAuthority` (único objeto que muta
  FuseSpec); el Árbitro consolida, el Juez (F4) autoriza vía token. Ver ADR-0012.
- **Descartado** que el optimismo de Mario pueda reducir la decisión: el Árbitro siempre
  toma la cota conservadora; Mario nunca debilita la seguridad.
