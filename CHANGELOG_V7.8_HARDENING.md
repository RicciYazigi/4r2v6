# CHANGELOG — V7.8 "HARDENING"

**Estado final:** P0 y P1 cerrados con gates en verde. P2 = documento de scoping (fuera de
alcance de esta ronda, por diseño). Suite completa **137 passed** (V7.7 dejó 126 + 11 nuevos:
5 de P0, 6 de P1). **Math sellado sin diffs** (`core/kernel_v6.py` SSOT, `core/frontier_v7.py`,
`four_r2/`, `evidence/frontier_v7_config.json`). Evals sellados intactos
(`veto_accuracy_kernel_LBB=1.0`, `benign_flag_rate=0.0`). Verificado por corrida real.

**Origen:** handoff V7.8 "Hardening" 2026-07-07, sobre V7.7 ya mergeado a main (`c1467bb`). Cierra
las dos brechas del `V7.7_FUSION_ARQUITECTURA_Y_WORKFLOW.md §9` (CCA heurístico, memoria térmica
volátil), en el orden dictado por la dependencia de datos `CCA → criticality → e_i → T_t`.

## Decisión de secuencia (verificada)
El acumulador térmico consume `criticality`, que produce el CCA. Si el CCA está ciego (evasión de
keywords), persistir la temperatura persiste una lectura ya falsa. Por eso **P0 (integridad de la
señal) va antes que P1 (durabilidad del estado)**. Los dos son independientes en implementación
pero P0 es upstream en el modelo de amenaza.

## P0 — Default conservador del CCA  ·  Gate P0 ✅ (5 tests)  ·  ADR-0014
`core/kernel_1240421.py::CCA.observe()` gana estado explícito `unclassified` con piso
`DEFAULT_UNCLASSIFIED_CRITICALITY = 0.50` (lab, pendiente calibración). "Ausencia de evidencia no
es evidencia de ausencia": una paráfrasis que evade el diccionario ("mueve los fondos" vs
"transfiere") dejaba `e_i=0` → invisible al térmico; ahora produce `e_i>0`.
- **Cero regresión del gate:** 0.50 está debajo de los umbrales de `to_regime` (0.6 pesos, 0.7
  theta) → theta y pesos sin cambio (verificado).
- **Corrección al handoff:** `eval_E3 benign_flag_rate` es **insensible** al CCA (`eval_e2_e3.py`
  no llama a `observe()`); se corre igual (sigue 0.0) pero el guard real es la suite + `four_r2` +
  smoke.
- **Hallazgo honesto:** con floor 0.50 y térmico por defecto la evasión sostenida alcanza
  `T_eq≈0.124 < T_trip=0.30` → hace la evasión **visible**, no la funde sola; fundir es calibración
  de `T_trip`. La solución de fondo es P2.

## P1 — Snapshot periódico del térmico  ·  Gate P1 ✅ (6 tests)  ·  ADR-0015
`ThermalAccumulator` persiste `{camino→T, last_t}` + `saved_at` a JSON con escritura atómica,
cadencia por eventos o segundos. Al recargar aplica decaimiento `exp(-Δt/τ)` por tiempo
transcurrido. **Fail-safe:** snapshot ausente/corrupto → arranca en cero sin excepción. Reloj
inyectable para tests deterministas. Alcance mínimo (JSON local, no base distribuida — eso es
semilla v8).

## P2 — Estimador semántico  ·  scoping únicamente  ·  `docs/V7.8_P2_SEMANTIC_ESTIMATOR_SCOPING.md`
Solución de fondo a la integridad del CCA. NO implementado. Documento traza el criterio: costo de
latencia (el gate corre sub-ms; un embedder lo saca de ese orden), decisión inline vs async, y la
recomendación de cablearlo como **capa async enriquecedora** sobre la `RecalibrationQueue`/Juez ya
existentes, no inline.

## Archivos
Modificados: `core/kernel_1240421.py` (CCA observer; NO la matemática sellada),
`antigravity_wings/thermal/accumulator.py` (snapshot).
Nuevos: `tests/test_cca_conservative_default.py`, `tests/test_thermal_snapshot.py`,
`docs/adr/ADR-0014`, `docs/adr/ADR-0015`, `docs/V7.8_P2_SEMANTIC_ESTIMATOR_SCOPING.md`, este CHANGELOG.

## Etiquetado de veracidad
**Demostrable:** decaimiento en recarga = `exp(-Δt/τ)` exacto; escritura atómica (tmp+rename);
piso debajo de umbrales de regime ⇒ gate invariante. **Empírico con límites:** 11 tests nuevos
(seed fijo / N explícito). **Pendiente/plausible:** `DEFAULT_UNCLASSIFIED_CRITICALITY=0.50`,
cadencia de snapshot, y `τ` en segundos son valores de laboratorio sin calibrar contra tráfico
real. **ND:** eficacia real contra evasión adversaria depende de P2 (semántico), no entregado.
