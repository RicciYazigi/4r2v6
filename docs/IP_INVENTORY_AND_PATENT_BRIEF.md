# IP_INVENTORY_AND_PATENT_BRIEF — 4R2 v7.x
**TRACE_ID:** ARS-20260707-APEX2 · **Fase 2 / Gap G9** · **Fecha:** 2026-07-07
**Naturaleza:** briefing técnico de invención para entregar a un abogado de patentes. **NO es una solicitud de patente ni asesoría legal.** No soy abogado; esto no sustituye a un profesional de patentes. Es el insumo que un abogado necesita para trabajar rápido.

> **Reloj de novedad — acción con prioridad temporal (§4 del plan APEX):** el repositorio ha tenido commits públicos. En jurisdicciones de **novedad absoluta** (la mayoría fuera de EE.UU.), cada divulgación pública previa a la fecha de prioridad erosiona la patentabilidad. **Acción crítica pendiente (ND en esta sesión):** determinar la **fecha del primer commit público** desde GitHub (no fue legible desde el sandbox — `git` reportó rama corrupta). Esa fecha fija la ventana real y el abogado la necesita el día uno.

---

## 1. Resumen ejecutivo

4R2 combina tres piezas que, **por separado**, tienen forma de material abstracto o conocido, pero **combinadas en un sistema de runtime** presentan reivindicaciones de sistema/método defendibles:

1. Un **kernel matemático de coherencia** (fórmula `H(x) = α·C_NR + β·C_RI + γ·(1−C_IF)`, distancia angular, C_IF dual-path).
2. Un **mecanismo de recalibración térmica** de umbrales de seguridad en tiempo real (modelo tipo I²t).
3. Una **arquitectura de gobernanza de tres capas** con autoridad de escritura única vía token y **vector de reroute** en lugar de bloqueo binario.

**Tesis de patentabilidad (plausible, a validar por abogado):** la pieza (1) sola probablemente **no es elegible** (fórmula/algoritmo abstracto — *Alice/Mayo* en EE.UU.; Art. 52 EPC en Europa). Las piezas (2) y (3), envueltas como **método técnico aplicado a la seguridad de un sistema de cómputo en tiempo de ejecución**, son las candidatas reales.

---

## 2. Inventario: patentable vs. secreto comercial

| Activo | Descripción | Vía recomendada | Razón |
|---|---|---|---|
| Kernel `H(x)`, distancia angular, C_IF dual-path | fórmula de coherencia multicapa | **Publicación / defensiva** (o parte de claim de sistema, no aislada) | Matemática pura → baja elegibilidad aislada; publicar crea *prior art* defensivo que impide que otro lo patente |
| **Recalibración térmica I²t de umbrales** | acumulación de energía de desviación con memoria + decaimiento que dispara recalibración de fusibles en runtime | **Patente (método/sistema)** | Proceso técnico concreto sobre estado de un sistema; efecto técnico medible |
| **Autoridad de escritura única vía token de un solo uso** | mutación de política de runtime autorizada por token no reutilizable emitido por el Juez/Árbitro | **Patente (método/sistema)** | Mecanismo de control de integridad concreto; no abstracto |
| **Vector de reroute** | alternativa gobernada al bloqueo binario: redirigir preservando la necesidad legítima | **Patente (método/sistema)** | Novedad de comportamiento del guardrail; diferenciador frente a "block/allow" |
| Valores calibrados τ, T_trip, umbral de confianza del Juez (una vez calibrados con datos reales) | parámetros finos de operación | **Secreto comercial** | No aportan a la defensibilidad de patente y publicarlos la debilita; funcionan sin ser públicos |
| Corpus de calibración de dominio + pesos de seguridad auditados | datos + configuración | **Secreto comercial** | Ventaja operativa no divulgable sin pérdida |

---

## 3. Tres divulgaciones de invención candidatas (borrador para provisional US)

> Redactadas como *invention disclosures*, no como reivindicaciones legales. El abogado las convierte en claims.

**INV-A — Recalibración térmica de umbrales de seguridad en tiempo real por acumulación de energía de desviación.**
Un método donde un guardrail de IA mantiene, por sesión/camino, un acumulador con memoria y decaimiento exponencial que integra una señal escalar de criticidad puntual (análoga a I²t en protección eléctrica); al superar un umbral térmico, dispara una recalibración gobernada del umbral del fusible correspondiente, de modo que la sensibilidad del control **se adapta a la carga acumulada de desviación** en vez de a eventos aislados. Registro: `ADR-0009` (TRACE_ID ARS-20260707-0002), `ADR-0015` (persistencia snapshot).

**INV-B — Autoridad de escritura única vía token de un solo uso para mutación de política de runtime.**
Un método donde ninguna capa observadora puede mutar la política activa; solo una autoridad árbitro puede escribir un fusible, y únicamente mediante un token de un solo uso emitido tras evaluación de un Juez, haciendo toda mutación de política **atribuible, no repetible y auditable**. Registro: `ADR-0011` (ARS-20260707-0004), `ADR-0012` (Juez), `ADR-0013` (desacople recalibración).

**INV-C — Reroute gobernado como alternativa al bloqueo binario.**
Un método donde un fusible que dispara no termina necesariamente en STOP: el sistema selecciona un **vector de reroute** que preserva la necesidad legítima subyacente (`preserves_need`) redirigiendo a una ruta alternativa conocida, bajo autorización de la misma autoridad árbitro. Registro: `ADR-0010` (ARS-20260707-0003).

---

## 4. Registro de fecha de invención (evidencia interna)

Cadena de ADRs con TRACE_ID sella la **fecha de concepción interna** (distinta de la fecha de divulgación pública, que es el reloj legal):

| Invención | ADR | TRACE_ID | Fecha ADR |
|---|---|---|---|
| I²t térmico | ADR-0009 | ARS-20260707-0002 | 2026-07-07 |
| Reroute | ADR-0010 | ARS-20260707-0003 | 2026-07-07 |
| Autoridad árbitro/token | ADR-0011 | ARS-20260707-0004 | 2026-07-07 |
| Persistencia térmica | ADR-0015 | (V7.8 P1) | 2026-07-07 |

**Caveat de honestidad:** las fechas de los ADR reflejan la fecha de *documentación*, no necesariamente la de *primera concepción*. El historial de commits (`historiafable5.md`, git) contiene la cronología real y debe adjuntarse al abogado como registro primario.

---

## 5. Estrategia repo público vs. privado (a partir de ya)

1. **Mantener público:** interfaz, arquitectura conceptual, kernel matemático (si se opta por publicación defensiva), harness de evaluación. Esto sostiene credibilidad/reproducibilidad sin dañar patente de sistema.
2. **Mover a repo privado:** valores calibrados finos (τ, T_trip, umbral Juez), corpus de calibración, pesos de seguridad auditados. Candidatos a secreto comercial.
3. **Congelar antes de nuevas divulgaciones:** no publicar detalles de implementación de INV-A/B/C hasta que exista solicitud provisional o decisión explícita de vía defensiva.

---

## 6. Prior art — honestidad (crítico para no sobre-reclamar)

Existe línea de investigación 2026 cercana que **el abogado debe conocer para evitar reivindicaciones inválidas**: DeepContext (RNN con estado sobre embeddings turno-a-turno), TRACE/MAGE/AgentAuditor/TrajAD (detección de deriva de intención en trayectoria). La intuición central de 4R2 (un gate puntual es ciego a la acumulación) **ya está validada por el campo — no es descubrimiento exclusivo**. La defensibilidad de 4R2 no está en "detectar deriva" (prior art existente) sino en la **combinación específica**: recalibración térmica gobernada + autoridad de escritura única por token + reroute. INV-A/B/C deben redactarse para distinguirse explícitamente de ese prior art. Contexto de mercado: M&A real reciente (Lakera→Check Point, Protect AI→Palo Alto) confirma apetito adquisitivo y sube la vara probatoria.

---

## 7. Próximos pasos (≤3) + decisiones a confirmar
1. **[Crítico/reloj]** Obtener fecha del primer commit público (GitHub) → fija ventana de novedad. **(ND — pendiente humano/WSL)**
2. Contratar abogado de patentes US; entregar este brief + cadena de ADRs + `historiafable5.md`. Evaluar provisional (12 meses de prioridad, bajo costo).
3. **Decisión a confirmar (Richie):** ¿kernel matemático por vía **defensiva/publicación** o incluirlo como sustrato de claim de sistema? Afecta qué se congela hoy.

## 8. Etiquetado de veracidad
- Existencia y fechas de ADR/TRACE_ID: **verificado** (leídos del repo).
- Elegibilidad de patente de cada activo: **plausible** (criterio técnico general; requiere abogado).
- Fecha del reloj de novedad: **ND** (no legible en sesión).
- Confianza global: **media** (inventario sólido; conclusiones legales fuera de mi competencia).
