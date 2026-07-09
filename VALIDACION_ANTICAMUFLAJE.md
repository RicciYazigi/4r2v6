# VALIDACIÓN — Defensa anti-camuflaje del modo gobernanza (`governance_anticamo`)

TRACE_ID: ARS-20260709-ACAM | Estado: OK | Rama: apex-20260707 (local, sin push)

## 1. Resumen (etiquetas de veracidad)

- **verificado** — C_NI (embeddings policy↔response) es estructuralmente engañable
  por camuflaje adversarial: AUROC 0.230 léx / 0.350 sem (n=20, peor que azar).
  Reproducido en esta sesión antes de tocar código.
- **verificado** — La defensa `governance_anticamo` (opt-in, capa SDK) lleva el
  adversarial a **0.830** sin degradar directo (**0.884**) ni dev (**0.800**),
  y separa perfectamente el held-out del benchmark (**1.000**, n=8, 0 errores
  de veredicto). Números medidos por ejecución end-to-end de la API real.
- **verificado** — Kernel congelado intacto (`git diff core/` vacío; sha256 de
  guardrail en HEAD comparado antes de editar). Default bit-idéntico (test).
- **plausible** — La generalización a otros dominios/idiomas: el léxico de
  postura es solo español y el NLI es multilingüe pero no evaluado fuera de ES.

## 2. Qué es la defensa (y qué NO es)

Fusión de 3 señales, normalizada a [0,1] (`four_r2/anticamo.py`):

| señal | qué mide | costo | peso |
|---|---|---|---|
| `stance` (léxico ES) | postura ejecución-vs-rechazo (morfológica, genérica) | ~0 ms, determinista | 1.00 |
| `nli` (opt-in) | P(entail "viola la política") − P(entail "cumple") con mDeBERTa-v3-base-mnli-xnli | ~2.5 s/muestra CPU | 0.25 |
| `c_ni` | señal original de gobernanza (embeddings) | según embedder | 0.50 |

**Nota de honestidad (obligatoria):** `stance` y `nli` NO son el gate de
coherencia NRIF: son un juez de lenguaje ligero. La robustez anti-camuflaje no
emerge del kernel congelado. El posicionamiento correcto de 4R2 para
response-governance robusto es: *pipeline por capas con juez ligero opt-in* —
determinismo, latencia acotada, fail-closed y defensa en profundidad — no
"la coherencia geométrica detecta camuflaje" (no lo hace; está medido).

## 3. Resultados (AUROC; embedder semántico all-MiniLM-L6-v2)

| set | n | C_NI base (léx/sem) | anticamo SIN NLI | anticamo CON NLI |
|---|---|---|---|---|
| OOD adversarial (`hard`) | 20 | 0.230 / 0.350 | 0.850 | **0.830** |
| OOD directo | 22 | 0.868 / 0.810 | 0.884 | **0.884** |
| dev curado | 42 | 0.773 / ~0.80 | 0.773 | **0.800** |
| **held-out benchmark** | 8 | — / 0.812 | ND | **1.000** |

- Bootstrap 95% CI del AUROC adversarial (con NLI): **[0.604, 0.980]**
  (2000 reps, seed 0). n=20 es poco; el intervalo es honesto y ancho.
- Held-out n=8 (4+/4−): 16 pares, AUROC 1.0; cota inferior real con n tan
  chico es débil (~0.66 por Hanley-McNeil). Es validación anti-gaming, no
  evidencia fuerte por sí sola.
- Ablación: el léxico determinista hace casi todo el trabajo adversarial;
  el NLI aporta +0.027 en dev y ordena mejor el held-out. Sin NLI es un modo
  degradado viable (sin dependencias extra).

## 4. Punto de operación (calibrado SOLO en dev + OOD visible)

`theta = 0.46`, `governance_flag_buffer = 0.15` (FLAG = escalar a humano):

| set | ASR (evasión) | ORR (FLAG+BLOCK sobre legítimas) |
|---|---|---|
| adversarial | 10% (2/20 · las 2 evasiones son violaciones camufladas) | 40% |
| directo | 0% | 36% |
| dev | 0% | 43% |
| held-out | 0% (0/4) | 0% (0/4) |

Lectura: el punto elegido es conservador — casi nada se evade, a costa de
mandar ~40% de lo legítimo de los sets difíciles a revisión (FLAG, no BLOCK).
Para tráfico normal (held-out del benchmark) no genera falsas alarmas.

## 5. Límites explícitos

1. n adversarial = 20 (visible) — potencia estadística baja; CI ancho.
2. Léxico de postura: español únicamente; autoría con acceso a dev+OOD visible
   (los patrones son morfológicos genéricos, sin frases de muestras; riesgo
   residual de sobreajuste declarado). Validación en held-out no usada para
   calibrar.
3. NLI: mDeBERTa-v3-base-mnli-xnli en CPU (~2.5 s/muestra, secuencial);
   determinista en una misma máquina/versión (eval, sin dropout), sin garantía
   bit-exacta entre plataformas BLAS distintas.
4. El atacante adaptativo que conozca el léxico puede evitar sus marcadores;
   la señal NLI y C_NI siguen, pero el techo real contra adversario adaptativo
   NO está medido (siguiente iteración: red-team adaptativo).
5. Garantía demostrable: solo las cotas [0,1] del score y la monotonía del
   floor de seguridad (ALLOW≤FLAG≤BLOCK). Todo lo demás es empírico con los
   N y seeds declarados.

## 6. Reproducción

```bash
# 4r2 repo, rama apex-20260707
python3 -m pytest -q                      # 162 passed
python3 self_test.py                      # exit 0
python3 experiments/eval_anticamo.py --nli <ruta_mdeberta>   # tabla §3-§4
git diff core/                            # vacío (kernel congelado)
```
Backend NLI: `MoritzLaurer/mDeBERTa-v3-base-mnli-xnli` (HF), max_length 256.
Embedder: `sentence-transformers/all-MiniLM-L6-v2`. Sets: `experiments/
ood_hard_eval.jsonl` (42; 20 hard), `experiments/policy_compliance_dev.jsonl`
(42), held-out = split MD5 20% del dataset `policy_compliance` de AegisBench
(vía `adapters_external/fourr2_adapter.py`, parámetros nuevos opt-in
`governance/anticamo/embedder/nli_backend`; el scoring del benchmark no cambió).

## 7. Próximos pasos (≤3)

1. Red-team adaptativo contra el léxico (atacante que conoce los patrones) y
   ampliación del set adversarial (n≥100, train/test separados).
2. Léxico de postura EN + fallback multilingüe (o sustituirlo por el NLI en
   modo 2-hipótesis de postura, midiendo el costo).
3. Decisión de producto: exponer `governance_anticamo` en el sidecar
   (`service.py`) y documentar la nota de honestidad en el deck técnico.

— Salida de un pipeline orquestado ("ARQ Orchestrator – Modo Arsenal") sobre un
LLM. Dirección humana: Richie.
