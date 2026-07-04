# Escenario Financiero Realista — 4R2 Coherence Guardrail

**Fecha:** 2026-07-04 | **Etiqueta de veracidad: ESPECULATIVO** (modelo basado
en supuestos declarados; no es asesoría financiera ni una valoración formal).
Los números **verificados** del activo están en MEGA_DELIVERY_v6.1.md; todo lo
demás aquí son escenarios condicionados a supuestos.

## 1. Qué es el activo hoy (verificado)

IP pre-revenue: kernel determinista de gating de coherencia (matemática
defendible, 7 ADRs, evals adversariales selladas, 0 mocks, reproducibilidad
criptográfica) + exoesqueleto de gobernanza (AGW) + pipeline de evidencia
audit-grade. Sin clientes de pago, sin patente presentada (ND), sin métricas
de tráfico real (E2/E3 pendientes — ver ROADMAP).

## 2. Supuestos del modelo (≤3, declarados)

- S1: E2 (embeddings reales, AUROC ≥ 0.85) y E3 (piloto sombra sin incidentes)
  se completan en ≤ 2 trimestres.
- S2: El mercado de AI safety/governance runtime mantiene demanda de
  adquisiciones de equipo+IP en etapa temprana (rango histórico típico
  acqui-hire/IP: un dígito bajo a medio de millones USD; deals estratégicos
  con tracción: más). Verificar contra comparables del trimestre antes de
  cualquier negociación (plan: buscar 5 comparables recientes en Crunchbase/
  PitchBook — ND en esta sesión).
- S3: Un (1) piloto enterprise convertible a contrato anual de 5 cifras.

## 3. Escenarios (condicionados a S1–S3)

| Escenario | Condición | Vía de monetización | Rango indicativo* |
|:----------|:----------|:--------------------|:------------------|
| Conservador | Solo v6.1 (estado actual), sin E2/E3 | Licencia de IP / acqui-hire técnico | bajo: valor dominado por el equipo y la documentación audit-grade |
| Base | E2+E3 verdes, 1 piloto sombra | Venta estratégica de IP a plataforma LLM/observabilidad, o seed round | medio: la evidencia E2/E3 es el multiplicador principal |
| Optimista | E2+E3 + 2 contratos + arXiv publicado | Adquisición estratégica big-tech (safety tooling) o Serie A | alto: requiere tracción real, no solo tecnología |

*Deliberadamente sin cifras absolutas: fijar números sin comparables del
trimestre sería alucinación. Acción concreta: levantar tabla de 5 comparables
antes del primer pitch (tarea BD-1 en SALES_STRATEGY.md).

## 4. Costos para llegar a "Base" (estimación operativa, especulativo)

- Cómputo E2 (embeddings + corpus): USD 200–800 (APIs/GPU spot).
- Piloto sombra E3: 0 licencias (shadow-mode), ~40–80 h de ingeniería.
- Legal mínimo (NDA + IP assignment limpio + provisional patent opcional):
  USD 2–8k según jurisdicción (verificar con abogado — no soy abogado).
- CI + infra demo: USD < 50/mes.

## 5. Driver de valor #1 (tesis)

Lo que un comprador big-tech paga en esta categoría no es el kernel (100
ingenieros pueden reescribirlo): es **(a)** la evidencia encadenada y
reproducible de que funciona, **(b)** la taxonomía de ataques con defensas
medidas (single-layer camouflage → LBB 50%→100%), y **(c)** el mapeo
regulatorio listo (EU AI Act). Cada semana de trabajo debe producir evidencia
sellada nueva, no features nuevas.

**Confianza:** media en la estructura, baja en cualquier cifra absoluta
(por diseño: se rehúsa inventar valoraciones).
