# Estrategia de Venta / BD — 4R2 Coherence Guardrail v6.1

**Fecha:** 2026-07-04 | **Etiqueta:** plausible (estrategia; sin contactos
reales aún — CRM se llena con personas verificadas, no inventadas).

## 1. Posicionamiento (una frase)

"Guardrail de coherencia determinista y auditable para agentes LLM en
producción: veredicto ALLOW/FLAG/BLOCK en sub-milisegundo, fail-closed,
con evidencia criptográfica que un auditor puede reproducir bit a bit."

## 2. ICP (perfiles de comprador, en orden)

1. **Plataformas LLM / labs** (equipos de safety tooling y enterprise): compran
   IP+equipo; les importa la taxonomía de ataques y el determinismo.
2. **Observabilidad/MLOps** (monitoreo de modelos): 4R2 como módulo de
   governance runtime; les importa el overhead sub-ms e integración sidecar.
3. **Regulados** (seguros, banca, salud — vía pilotos): les importa EU AI Act
   Art. 9/12/14 y la banda FLAG como "human oversight" demostrable.

## 3. Narrativa de demo (black-box, 10 min)

1. Tráfico on-topic → 100% ALLOW (FPR 0.0, en vivo).
2. Ataque A1 (violación normativa camuflada con física perfecta) → gate
   convexo lo dejaría pasar; **LBB lo bloquea en vivo**.
3. Input envenenado (zero-vector) → BLOCK fail-closed, sin excepción.
4. Repetir la corrida → hashes idénticos (determinismo ante el prospecto).
Nunca exponer el kernel; deck A/B según audiencia (técnica/ejecutiva).

## 4. Secuencia de contacto (plantilla)

- Toque 1 (LinkedIn/email corto): problema (agentes que se desvían en prod) +
  1 métrica dura (veto adversarial 50%→100%, evidencia sellada) + pregunta.
- Toque 2 (+5 días): whitepaper arXiv + oferta de demo black-box de 15 min.
- Toque 3 (+7 días): caso piloto sombra sin costo, 2 semanas, cero riesgo
  (shadow-mode: no toca decisiones de producción).
Regla: nunca prometer métricas de E2/E3 antes de tenerlas selladas.

## 5. CRM (nombre | foco | razón | canal | estado)

| Nombre | Foco | Razón | Canal | Estado |
|:-------|:-----|:------|:------|:-------|
| ND (llenar con targets verificados) | safety tooling | taxonomía ataques + evidencia | intro tibia > frío | pendiente BD-1 |

## 6. Tareas BD inmediatas

- **BD-1**: tabla de 5 comparables de adquisición (Crunchbase/PitchBook) y 10
  targets nombrados con contacto verificable. Sin esto, no hay pitch.
- **BD-2**: deck A (técnico, con E1/E4) y deck B (ejecutivo, con roadmap
  regulatorio). Insumos ya existen en docs/.
- **BD-3**: completar E2/E3 (el multiplicador de valoración; ver ROADMAP).

## 7. Qué NO hacer

No vender "termodinámica" (el propio CANON la declara analogía); vender
**determinismo + evidencia + taxonomía de ataques**. No cifras de valoración
sin comparables. No demos con mocks: el diferenciador es que nada es mock.
