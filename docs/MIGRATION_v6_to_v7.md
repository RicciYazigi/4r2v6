# Guía de migración v6.1.0 → v7.0 "Frontier"

**TL;DR:** v7.0 **no rompe nada**. El kernel v6.1.0 queda congelado; todas las
defensas nuevas viven en `core/frontier_v7.py` y son **opt-in**. Puedes seguir
usando la API v6.1.0 tal cual y activar el frontier solo cuando lo calibres.

## 1. ¿Qué NO cambia?

- La API pública del kernel (`CoherenceKernel`, `LayerState`, `Regime`,
  `compute_with_regime`, `measure_coherence_with_keys`) es **idéntica**.
- Los 65 tests originales siguen verdes; el determinismo, la paridad de réplicas
  (1 hash) y la evidencia sellada previa no se tocan.
- El veredicto v6.1.0 (gate θ + LBB + fusible VER) sigue siendo el mismo.

## 2. ¿Qué añade v7.0?

| Señal | Qué hace | Garantía |
|:------|:---------|:--------|
| `h_energy(C_NR,C_RI,C_IF,HParams)` | Score de brecha por capa H(x)=a·C_NR+b·C_RI+g·(1−C_IF); generaliza el LBB con una frontera calibrada | T1: cotas [0,1], monotonía |
| `camouflage_js(...)` | JS-divergencia contra referencia benigna | T1: [0, ln2] |
| `layer_entropy(...)` | Entropía de Shannon sobre el vector de brecha (telemetría OOD) | T1: [0, ln3] |
| `verifiability_negation(text)` | Detector de negación de control endurecido (paráfrasis-robusto) | T2: evasión 0% en probe n=15 (léxico) |
| `frontier_verdict(breakdown, base, cfg)` | Compone gate v6 + LBB + H + OOD; **solo escala** (nunca relaja v6) | T1: monotonía de escalación |

## 3. Cómo activar el frontier (opt-in, 3 pasos)

```python
import sys; sys.path.insert(0, "core")
import frontier_v7 as fv
from kernel_1240421 import CoherenceKernel, LayerState, Regime

# (1) Calibra H y la banda OOD sobre TUS datos etiquetados.
#     IMPORTANTE: el corpus debe incluir ataques en AMBOS ejes de brecha
#     (N-R y R-I), o la calibración degenera un peso a 0 (ver §5).
cfg = fv.FrontierConfig(
    fv.calibrate_h_from_rows(rows),      # rows: dicts con C_NR,C_RI,C_IF,label
    fv.calibrate_ood_band(rows),
    source="mi despliegue")

# (2) Corre el kernel v6.1.0 como siempre.
k = CoherenceKernel()
c_total, res = k.compute_with_regime(state, Regime())

# (3) Compón el veredicto v7 (solo puede endurecer el de v6).
out = fv.frontier_verdict(res["breakdown"], res["verdict"], cfg)
print(out["verdict"], out["escalations"])
```

Sin calibrar, el default de `HParams` deja la escalación de H **desactivada**
(`threshold=1.01`), de modo que un despliegue no calibrado se comporta como
v6.1.0 + LBB — nunca hereda un comportamiento sin validar.

## 4. Cableado del detector de negación a producción

Ya está cableado en `scripts/eval_e2_e3.py::verifiability` (usa
`verifiability_negation` en vez del regex estrecho). Para tu propio extractor de
verificabilidad, reemplaza tu detección de "bypass de control" por
`fv.verifiability_negation(response)`. E2 post-wiring: FPR 0.0, FNR 0.0,
veto 100%, AUROC 1.0 (sin regresión).

## 5. Dos trampas que ya cerramos (no las reabras)

1. **No pongas `g>0` a mano** en H(x). El término (1−C_IF) es no-discriminativo
   para el camuflaje (atacante y caso legítimo impecable tienen ambos C_IF=0).
   Deja que la calibración lo lleve a ~0 (ADR-0008). Un `g` balanceado mete
   ~15% de falsos positivos sobre tráfico de alta verificabilidad genuina.
2. **Calibra con ataques en ambos ejes.** Si tu corpus solo ataca C_NR, Fisher
   aprende `b=0` y el ataque en C_RI evade H. Verifica `a>0` y `b>0`
   (`degeneracy_check`), y mantén el test `test_calibration_covers_both_breach_axes`.

## 6. Verificación tras migrar

```bash
python -m pytest -q                              # 77/77
python scripts/frontier_calibrate.py             # calibración + control Fisher-vs-angular
python scripts/eval_e4_extended.py               # ataque de camuflaje ambos ejes
python scripts/eval_high_verifiability_fpr.py    # FPR alta-ver = 0, ambos pesos activos
python self_test.py                              # self-test del contenedor -> exit 0
```

Referencia completa de resultados y garantías T1/T2: `docs/FRONTIER_REPORT.md`.
Decisión de diseño de H(x): `docs/ADRs/0008-frontier-v7-h-energy-and-verifiability-term.md`.
