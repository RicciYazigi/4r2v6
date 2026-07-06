# ROADMAP DEFINITIVO — 4R2 Coherence Guardrail

**Base congelada:** v6.1.0 (2026-07-04) — ADR-0001…0007, 65/65 tests,
E1/E4 sellados, determinismo probado, 4 réplicas 1 hash.
**Regla de avance:** ningún milestone se declara sin evidencia ejecutada
(gates A/B/C; si falta → STOP-THE-LINE).

## v6.1.x — Hardening inmediato (0–2 semanas)
- [x] LBB + wrapper fail-closed (ADR-0007) — **hecho, evidencia E4**
- [x] Dataset E1 + evals E1/E4 selladas — **hecho**
- [x] Archivo de kernel legacy + evidence_index regenerado — **hecho**
- [ ] `docker build` basic/enhanced verificado en host con Docker (ND en
  sandbox de esta sesión; comando: `docker compose build && docker compose up -d
  && bash verify.sh` en cada system). Gate A.
- [ ] CI (GitHub Actions): pytest + determinism + eval E1/E4 + hash-parity de
  réplicas en cada push. Gate A.

## v6.2 — Realismo de señal (2–8 semanas)
- [x] **E2-lex hecho** (LSA real, AUROC 1.0/1.0, T3 aceptable 1.0 — ver docs/E2_E3_REPORT.md); pendiente tier sentence-transformers en host. E2 original: evaluación con **embeddings reales** (sentence-transformers o API) sobre
  corpus público etiquetado (e.g. HaluEval/TruthfulQA adaptados a NRIF).
  Métrica: AUROC de C_total vs etiquetas humanas; criterio ≥ 0.85. Gate B.
- [x] **E3-sim hecho** (300 eventos, 0 incidentes, FLAG benigno 0%, 0.124ms — ver docs/E2_E3_REPORT.md); pendiente tráfico real de cliente. E3 original: piloto sombra (shadow-mode) sobre tráfico real de un caso amigo
  (insurance pilot), 2 semanas, tasa FLAG < 10%, cero incidentes ALLOW-grave.
- LBB por dominio vía DomainKernel (calibración por percentiles del dominio).
- Migración FastAPI lifespan + `datetime.now(timezone.utc)` (deuda cosmética).

## v6.3 — Enterprise readiness (8–16 semanas)
- Observabilidad: OpenTelemetry + panel de zonas (GREEN/GRAY/RED) en cockpit.
- Multi-tenant: perfiles de peso y θ por tenant firmados (config governance —
  cierra el vector "weight gaming" documentado en E4).
- Mapeo regulatorio EU AI Act (Art. 9 gestión de riesgo, Art. 12 logging,
  Art. 14 supervisión humana → banda FLAG) + SOC2 Type I readiness.
- Whitepaper arXiv v2 con resultados E2/E3 (envío real).

## v7 — Producto (16+ semanas)
- SDK (pip package) + gateway sidecar (deploy 1-línea junto a cualquier LLM).
- Certificación de determinismo reproducible por terceros (auditoría externa).
- Data-room M&A: evidencia encadenada completa, IP chain-of-title, demo
  black-box.

## Riesgos vivos
- **P1** Falsos positivos FLAG en dominios creativos → mitigar con perfil
  `creative` + banda FLAG (revisión, no bloqueo).
- **P1** Calidad de embeddings acota el techo del sistema (E2 lo mide).
- **P2** Deprecations FastAPI/datetime — sin impacto matemático.

---

## Milestones consolidados (actualización 2026-07-04, ciclo 4)

| Milestone | Contenido | Criterio de cierre (gate) | Estado |
|:----------|:----------|:--------------------------|:------:|
| **v6.1.0** | Kernel angular + LBB + evals E1/E4 + E2-lex/E3-sim + docs + CI + README | 65/65, veto 100%, 0 incidentes, evidencia sellada | **CERRADO** |
| **v6.2** | E2-st (el job `semantic-tier` del CI lo corre solo en el primer push a GitHub y sube el artifact) + CI verde + calibración LBB/θ por dominio + Docker validado en host | AUROC ST reportado + badge CI verde + parity=1 | CI listo; ejecución en GitHub/host |
| **v6.3** | Piloto sombra con TRÁFICO REAL de cliente amigo (2 semanas) + observabilidad OTel | 0 incidentes reales, FLAG < 10%, informe firmado | Pendiente |
| **v7.0-Frontier (core)** | Módulo opt-in `frontier_v7.py`: H(x) calibrado (ambos ejes), JS camuflaje, Shannon OOD, negación endurecida cableada a producción; 2 vulnerabilidades simétricas cazadas y cerradas ((1−C_IF) y eje C_RI) | 77/77 tests, veto ambos ejes, FPR alta-ver 0.0, evidencia sellada, ADR-0008 | **CERRADO (rama v7-frontier-wip)** |
| **v7 (producto)** | SDK pip + sidecar + arXiv enviado + data-room M&A + Docker build en host | Paquete instalable + submission ID + data-room revisado | Pendiente |
