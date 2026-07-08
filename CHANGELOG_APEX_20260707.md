# CHANGELOG_APEX — 2026-07-07
**Sesión:** APEX (Fable 5) sobre V7.8 Hardening. **Dirección humana: Richie.**
**Baseline entrada:** `137 passed`. **Baseline salida:** `142 passed` (137 + 5 audit). **Math sellado: sin diffs.**

## Cerrado esta sesión

### FASE 1 / G1 — Benchmark contra datasets públicos  ·  Estado: OK ejecutado / ALERTA hallazgo negativo
- `scripts/eval_public_benchmarks.py` — AdvBench + HarmBench (harmful) vs Alpaca (benign), mapeo NRIF, kernel real, seed 1240421.
- `evidence/benchmark_public_20260707.json` (SHA-256 `39280c9c…fec521`).
- `docs/BENCHMARK_COMPARISON_PUBLIC.md`.
- **Resultado (empírico con límites, tier-LSA):** AUROC AdvBench-vs-Alpaca **0.418** (C_total) — el kernel con backend léxico **NO separa** cumplimiento dañino de ayuda benigna; HarmBench request-level AUROC 0.414. Latencia 0.174 ms/evento.
- **Diagnóstico (verificado):** una respuesta que cumple con una petición dañina es *internamente coherente* → un gate de coherencia puntual es ciego a ella. Confirma cuantitativamente G2/G3 y **re-prioriza la Fase 3**. NO es defecto de corrección (142 tests verdes); es límite de alcance del gate con embedding léxico + política genérica.
- **ND:** tier deep-semantic (sentence-transformers) no ejecutable en sandbox; harness idéntico listo para correrlo.

### FASE 2 / G9 — IP inventory + patent brief  ·  Estado: OK
- `docs/IP_INVENTORY_AND_PATENT_BRIEF.md` — inventario patentable vs secreto comercial, 3 divulgaciones de invención (INV-A térmico I²t, INV-B token de escritura única, INV-C reroute), registro de fecha vía ADRs/TRACE_ID, estrategia repo público/privado, prior-art honesto (DeepContext/TRACE).
- **Acción crítica con reloj (ND):** fecha del primer commit público (no legible en sandbox — `git` reportó rama corrupta). Fija la ventana de novedad; requerida por el abogado.

### FASE 5 / G6 — Registro tamper-evident  ·  Estado: OK (demostrable)
- `antigravity_wings/antigravity_wings/audit/hash_chain.py` + `scripts/verify_audit_chain.py` + `antigravity_wings/tests/test_audit_chain.py` (5/5).
- `docs/AUDIT_CHAIN_DESIGN.md` con mapeo EU AI Act Art. 12 / NIST / HIPAA y límites declarados.
- **Demostrable:** alterar entrada intermedia → verificador detecta en el punto exacto (broken_at=3).

## NO hecho (checkpoint honesto — corte explícito)
- **Fase 3 (G2+G3)** estimador semántico: no iniciado. Ahora con justificación cuantitativa (Fase 1). Requiere sesión dedicada + sentence-transformers.
- **Fase 4 (G4+G5)** wiring end-to-end + worker async: no iniciado. Incluye cablear el audit-chain (G6) al `DualRuntimeOperator`.
- **Fase 6/7** piloto + pentest scope + colaboradores: dependen de 1-5.
- **Gate G1:** NO se declara "passed" — se declara **ejecutado con resultado negativo diagnosticado**, que es el entregable correcto según §0.7 del plan.

## Etiquetado de veracidad
demostrable: audit-chain tamper-evidence, 142 tests verdes, math sin diffs · empírico con límites: AUROC/F1/latencia benchmark (tier-LSA, seed, N) · plausible: métricas de competidores (auto-reportadas), elegibilidad de patente · ND: tier deep-semantic, fecha primer commit público.

## Archivos nuevos
scripts/eval_public_benchmarks.py · scripts/verify_audit_chain.py · antigravity_wings/antigravity_wings/audit/{__init__,hash_chain}.py · antigravity_wings/tests/test_audit_chain.py · evidence/benchmark_public_20260707.json · docs/{BENCHMARK_COMPARISON_PUBLIC,IP_INVENTORY_AND_PATENT_BRIEF,AUDIT_CHAIN_DESIGN}.md · CHANGELOG_APEX_20260707.md
