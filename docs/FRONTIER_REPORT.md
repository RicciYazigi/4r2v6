# FRONTIER_REPORT — 4R2 Coherence Guardrail v7.0 "Frontier"

**TRACE_ID:** ARS-20260705-F5-V7-0001 | **Estado: OK**
**Fecha:** 2026-07-05 | **Base congelada:** kernel v6.1.0 (ADR-0006 + ADR-0007)
**Módulo nuevo:** `core/frontier_v7.py` (opt-in, sin breaking changes) | **Dirección humana:** Richie

> Regla de honestidad de este reporte: se separan **garantías matemáticas
> demostrables (T1)** de **resultados empíricos con límites explícitos (T2)**.
> Nunca se presenta T2 como T1. Todo número T2 proviene de una ejecución real,
> semilla fija `1240421`, sellada por SHA-256. Lo que no se ejecutó se marca ND.

---

## 1. Qué añade v7.0 (y qué NO)

v7.0 **no reabre** el kernel v6.1.0: lo importa y lo deja intacto (API pública
sin cambios; 65/65 tests originales siguen verdes). Añade tres señales de
desacoplamiento entre capas y un detector de negación endurecido, todo opt-in:

1. **H(x)** — score de energía de brecha por capa, *derivado* (reemplaza el
   umbral heurístico 0.75/0.60 del LBB por una frontera calibrada por
   discriminante lineal de Fisher sobre datos reales).
2. **Señal de camuflaje** — JS-divergencia contra referencia benigna (reusa la
   JS acotada ya probada del kernel; no inventa métrica nueva).
3. **Señal OOD** — entropía de Shannon sobre el vector de brecha (no Von
   Neumann), banda por percentiles benignos.
4. **Detector de negación endurecido** — cierra la evasión por paráfrasis del
   fusible VER de v6.1.0 (hallazgo P1). **Cableado a producción**
   (`scripts/eval_e2_e3.py::verifiability`); E2 post-wiring sin regresión
   (FPR 0.0, FNR 0.0, veto 100%, AUROC 1.0).

**Contrato de seguridad:** `frontier_verdict` es **escalación pura** — puede
degradar ALLOW→FLAG→BLOCK, **nunca** relaja un veredicto v6. Probado como
propiedad (test `test_frontier_is_escalation_only`, 300 casos aleatorios).

---

## 2. Garantías T1 — matemáticas demostrables

Probadas en pocas líneas en `scripts/test_frontier_v7.py` (9 tests, todos verdes):

| Propiedad | Enunciado | Prueba |
|:----------|:----------|:-------|
| Cota de H(x) | Con pesos en el símplex y C_j∈[0,1], `H∈[0,1]` | convexidad; `test_H_bounded_on_simplex` |
| Monotonía de H | H no decrece en C_NR, C_RI y en (1−C_IF) | lineal con pesos ≥0; `test_H_monotone_nondecreasing` |
| Cota de entropía | `H_shannon∈[0, ln 3]` sobre el vector de 3 capas | Shannon sobre índice finito; `test_entropy_bounded_ln3` |
| Firma de capa única | brecha concentrada ⇒ entropía menor que difusa | `test_single_layer_has_low_entropy` |
| Cota de camuflaje | `JS∈[0, ln 2]`, simétrica, finita | reusa `kernel_v6.js_divergence`; `test_camouflage_js_bounded_ln2` |
| Escalación monótona | v7 nunca sube (mejora) un veredicto v6 | `test_frontier_is_escalation_only` |

Estas son garantías **demostrables**, no medidas. No se afirma completitud
universal a partir de ellas.

---

## 3. Decisión Fisher vs. angular (honesta, con evidencia)

**Decisión: se mantiene la métrica angular** (ya es una métrica verdadera:
simetría + desigualdad triangular, probada en v6). Una métrica de Fisher-Rao
sería la distancia natural **sólo** si los objetos comparados fueran parámetros
de una familia de distribuciones; los embeddings densos genéricos **no lo son**,
y fabricar una familia (p. ej. gaussianas independientes) sería rigor aparente,
no real.

**Control empírico** (no aserción): sobre el corpus E2 real se comparó la
proyección angular contra un reweighting *diagonal-Fisher* (escala por inversa
de varianza intra-clase, la diagonal de la FIM si las features fueran gaussianas
independientes):

| Proyección | AUROC adversarial-vs-benigno |
|:-----------|:----------------------------:|
| angular (mean-breach) | 0.3882 |
| diagonal-Fisher | 0.3260 |
| **Δ** | **−0.0622 (empeora)** |

El proxy Fisher no aporta ganancia material → **mantener angular está
evidenciado, no asumido.** (Sellado en `frontier_calibration.json`.)

---

## 4. Resultados T2 — empíricos, medidos y sellados

### 4.1 Vulnerabilidad central cuantificada: camuflaje de alta verificabilidad

Sobre el corpus E2 real, H(x) construido **sólo con magnitudes de capa** separa
perfectamente benigno-vs-grave pero **no** el adversarial camuflado:

| H(x) AUROC | valor |
|:-----------|:-----:|
| benigno vs off-topic-grave | **1.000** |
| benigno vs adversarial | **0.275** (≈ azar, incluso peor) |

Esto **es** la vulnerabilidad, medida: con `F=[1,1,1,1]` el adversarial hace que
las magnitudes de capa parezcan benignas. **La defensa no puede ser H(x) sobre
capas; es la señal de verificabilidad con negación.** (No se disfraza esto: es
un resultado negativo reportado.)

### 4.2 Ataque geométrico real E4-extendido (a través del kernel real)

Ataque de brecha normativa de capa única con verificabilidad perfecta
(`C_IF→0`), construyendo `LayerState` reales que realizan distancias angulares
exactas y pasándolos por el kernel real. Insight medido: forzar `C_IF→0` fuerza
`(1−C_IF)=1`, justo el término que H(x) penaliza.

Se mide el éxito del atacante (fracción que obtiene ALLOW) en **ambos ejes de
brecha** de capa única (N-R y R-I), con verificabilidad perfecta:

| Defensa | Éxito atacante eje N-R | Éxito atacante eje R-I |
|:--------|:----------------------:|:----------------------:|
| sólo gate (convexo) | **100.0%** | **100.0%** |
| gate + LBB (v6.1.0) | 78.9% | 78.9% |
| **gate + v7 H(x) (frontier)** | **55.3%** | **55.3%** |

v7 recorta el éxito del atacante de 100%→55% **simétricamente en ambos ejes**
(ver §4.7 sobre el hueco C_RI cazado y cerrado). **H se calibra por Fisher sobre
un corpus de ambos ejes**: pesos `a≈b≈0.5` (ambos ejes de brecha activos),
`γ=0.0` (el término (1−C_IF) sale, ver §4.6), y **FPR sobre tráfico legítimo de
alta verificabilidad genuina = 0.0**. El residual sub-umbral (brecha de un eje
≤0.42) queda cubierto por el LBB desde 0.60 — sin banda descubierta entre
defensas. (Sellado en `eval_E4E5_results.json` y `eval_high_ver_fpr.json`.)

### 4.3 E5-OOD (entropía de Shannon) — resultado negativo honesto

La entropía sobre el vector de brecha **no** detecta el ataque de camuflaje de
alta verificabilidad: entropía media benigna 0.508 vs. ataque 0.663, ambas
dentro de banda (tasa de detección del ataque por banda = 0.0). La entropía
queda como **telemetría OOD genérica reportada**, no como defensa de este
ataque. La escalación OOD del frontier exige además `max_layer≥0.5` (que el
tráfico benigno no tiene), por lo que **no** introduce falsos positivos
(v7 FPR=0 en E2).

### 4.4 P1 — Endurecimiento del detector de negación (fusible VER)

El regex de v6.1.0 (`without|skipping|bypass`) es evadible por paráfrasis. Probe
de 15 ataques parafraseados + 5 controles benignos:

| Detector | Evasión (ataques) | Falsos positivos (benigno) |
|:---------|:-----------------:|:--------------------------:|
| v6.1.0 (estrecho) | **93.3%** | 0.0% |
| **v7 endurecido** | **0.0%** | 0.0% |

Límite explícito: detector **léxico** sobre un probe curado de n=15; no es
garantía semántica; una paráfrasis novedosa aún podría evadir. Wiring a la
extracción de verificabilidad de producción = cambio de una línea (recomendado).
(Sellado en `eval_negation_hardening.json`.)

### 4.6 Vulnerabilidad simétrica cazada por revisión (2026-07-05)

Un revisor probó el propio `h_energy` con casos que el reporte no aislaba y
encontró una **vulnerabilidad simétrica real**: el término `(1−C_IF)` sube
cuando la verificabilidad es *genuinamente perfecta* (C_IF→0). Como el atacante
de camuflaje **y** un caso legítimo impecable tienen ambos C_IF=0 ⇒ (1−C_IF)=1,
un H balanceado (γ=1/3) trataba la perfección genuina como sospechosa.

**Medido** (`eval_high_ver_fpr.json`, 120 casos legítimos de alta verificabilidad
real, F=[1,1,1,1], por el kernel real):

| Variante de H | FPR alta-verificabilidad legit | Veto ataque |
|:--------------|:------------------------------:|:-----------:|
| balanceado (a=b=g=1/3), θ=0.42 | **0.15** | 1.00 |
| Fisher-calibrado (a=1, g=0), θ=0.251 | **0.00** | 1.00 |
| solo-brecha (a=b=1/2, g=0), θ=0.209 | **0.00** | 1.00 |

El término balanceado costaba **15% de falsos positivos sobre el mejor tráfico**
y no aportaba **ningún** veto adicional. La calibración Fisher (y el propio E2,
que ya había fijado g=0) confirman: **(1−C_IF) es no-discriminativo para este
ataque** y debe salir de H. **Resolución (ADR-0008):** H se calibra siempre;
el config balanceado hard-coded queda retirado; el default del módulo mantiene
la escalación de H desactivada (threshold=1.01) para que un despliegue sin
calibrar nunca herede la falla. Tests de regresión sellan la corrección.

### 4.7 Segundo hueco simétrico cazado: eje C_RI (2026-07-05)

Tras cerrar el `(1−C_IF)`, la calibración Fisher sobre el primer corpus dio
`a=1.0, b=0.0, g=0.0` — no solo cayó `g`, también cayó **`b` (peso de C_RI) a 0**.
Verificado de forma independiente: con esos pesos, un ataque de camuflaje idéntico
pero con la brecha en **C_RI** (`C_NR≈0.05, C_RI≈0.74, C_IF=0`, bajo el piso del
LBB) obtenía **ALLOW** — la misma vulnerabilidad de capa única, reabierta en el
otro eje.

**Causa raíz:** el corpus de calibración construía los ataques variando **solo
C_NR**, así que Fisher aprendió correctamente a ignorar `(1−C_IF)` pero también,
sin querer, a ignorar `C_RI` (no cargaba señal en ese dataset).

**Corrección medida** (`eval_high_ver_fpr.json`, corpus ampliado a ambos ejes,
kernel real):

| Calibración | pesos (a, b, g) | veto ataque N-R | veto ataque R-I | FPR alta-ver |
|:------------|:---------------:|:---------------:|:---------------:|:------------:|
| un solo eje (rota) | (1.0, 0.0, 0.0) | 1.00 | **0.00** | 0.00 |
| ambos ejes (corregida) | (0.499, 0.501, 0.0) | **1.00** | **1.00** | **0.00** |

**Resolución:** H se calibra siempre sobre un corpus que contiene ataques en
ambos ejes; se verifica explícitamente que ni `a` ni `b` degeneren a 0
(`degeneracy_check: PASS`). Test de regresión `test_calibration_covers_both_breach_axes`
falla si cualquiera de los dos ejes con verificación perfecta logra ALLOW. Este
hueco lo encontró Richie reejecutando la calibración, no leyéndola — exactamente
el patrón de auto-caza que este proyecto persigue.

### 4.8 Tercer hallazgo de auditoría: el config SELLADO estaba degenerado (2026-07-06)

Una auditoría milimétrica (Richie, ejecutando el repo real tras el merge)
destapó una discrepancia entre la prosa y la evidencia sellada: aunque
`eval_high_ver_fpr.json` mostraba `a=0.499, b=0.501`, el config que
`scripts/frontier_calibrate.py` sella como oficial —
`evidence/frontier_v7_config.json`— seguía con:

```
"h": {"a": 0.0, "b": 1.0, "g": 0.0, "threshold": 0.42}
```

`a=0.0` — **el mismo defecto de degeneración, ahora en el eje N-R**, en el
artefacto que el pipeline nombra como config de producción. Causa raíz:
`frontier_calibrate.py` calibraba los pesos sobre el corpus **E2 puro**, donde
los grave off-topic solo divergen por C_RI (nunca por C_NR), así que Fisher
aprendía `b=1, a=0` legítimamente para E2 pero quedaba ciego al eje N-R. El
script nunca se re-corrió con ambos ejes tras el fix de `eval_e4_extended.py`,
y el test de regresión usaba un corpus sintético aislado, no el pipeline real.
(No era un riesgo activo — ningún módulo de gate carga ese archivo — pero
contradecía el reporte y estaba sellado como evidencia de due diligence.)

**Corrección (medida):** los **pesos** de H(x) son propiedad del *threat model*
(ambos ejes importan igual → a≈b; (1−C_IF) no discrimina → g≈0), NO de un
corpus; se calibran sobre un corpus de camuflaje de **ambos ejes**. El
**threshold** sí es específico del embedder → se calibra por Youden sobre E2.
Config sellado resultante:

| | a | b | g | threshold | degeneracy_check | E2 FPR/FNR/veto |
|:--|:-:|:-:|:-:|:--------:|:----------------:|:---------------:|
| antes (E2 puro) | **0.0** | 1.0 | 0.0 | 0.42 | FAIL (N-R ciego) | 0/0/1.0 |
| ahora (ambos ejes + E2 thr) | **0.499** | **0.501** | **0.0** | 0.453 | **PASS** | **0/0/1.0** |

Salvaguardas: `frontier_calibrate.py` ahora expone `build_calibration_config()`
(el mismo pipeline que sella el artefacto) y emite un `degeneracy_check`. Tres
tests nuevos (`tests/test_frontier_config_integrity.py`) corren el **pipeline
real** y además inspeccionan el **artefacto sellado en disco**, fallando si `a`
o `b` degeneran a 0 o si `g` reintroduce (1−C_IF). El hueco ya no puede volver
a colarse en silencio.

### 4.5 No-regresión

| Control | v6.1.0 | v7 calibrado |
|:--------|:------:|:------------:|
| FPR on-topic (E2) | 0.0 | **0.0** |
| FNR grave (E2) | 0.0 | **0.0** |
| Veto adversarial (E2, fusible VER endurecido en producción) | 100% | **100%** |
| Suite de tests | 65/65 | **77/77** (65 + 12 frontier) |
| Paridad de réplicas | 1 hash | **1 hash** |

---

## 5. Empaquetado ejecutable (FASE 3)

`Dockerfile` (raíz) + `self_test.py` como ENTRYPOINT. El self-test corre en
ejecución **real** kernel_v6 + kernel_1240421 + frontier_v7 selftests, paridad
de réplicas, cierre de camuflaje y evasión de negación=0; **exit 0** verificado
localmente en esta sesión (7/7 checks PASS).

```
docker build -t 4r2:v7 .
docker run --rm 4r2:v7 --self-test   # -> exit 0
```

**Estado del build de imagen: ND en esta sesión** (no hay binario Docker en el
sandbox). El *comportamiento* del self-test está probado por ejecución local
directa; falta sólo el `docker build` en host con Docker (comandos WSL provistos
en el cierre). No se reporta como corrido lo que no se corrió.

---

## 6. Posicionamiento honesto vs. estado del arte

| | Llama Guard | NeMo Guardrails | Constitutional-AI classifiers | **4R2 v7.0** |
|:--|:--|:--|:--|:--|
| Naturaleza | clasificador LLM fine-tuned | reglas + LLM checks | clasificador probabilístico | kernel geométrico determinista |
| Determinismo bit-a-bit | no | no | no | **sí** (SHA-256, 1e-12, 20 runs) |
| Trazabilidad por capa | no | parcial | no | **sí** (NRIF: C_NR/C_RI/C_IF) |
| Evidencia sellada/reproducible | no estándar | no | no | **sí** (evidence_index encadenado) |
| Latencia | ~decenas–cientos ms | variable | ~decenas ms | **0.124 ms media** (piloto sombra medido) |
| Garantía matemática de cotas | no | no | no | **sí** (T1: cotas convexas, JS, entropía) |

**Lo que 4R2 v7.0 garantiza que los enfoques probabilísticos no:** determinismo
bit-a-bit, trazabilidad por capa NRIF, evidencia criptográficamente sellada y
reproducible, latencia sub-ms medida, y cotas matemáticas demostrables sobre las
señales.

**Lo que 4R2 v7.0 NO garantiza todavía (nombrarlo da credibilidad):**
- Cobertura semántica amplia tipo LLM-judge: el detector de negación es léxico
  (n=15 probe); NO es comprensión semántica.
- Generalización a dominios no calibrados: H(x) y umbrales se calibran por
  despliegue; fuera de calibración no hay garantía.
- El backend de embeddings sellado aquí es **LSA lexical** (determinista, puro
  numpy). El tier sentence-transformers corre en CI/host (job `semantic-tier`),
  ND en sandbox.
- Certificación legal real del mapeo EU AI Act: sigue en nivel **plausible —
  revisar con legal**, no certificado.
- El corpus E2 es **autorado**, no benchmark público (HaluEval-style pendiente,
  gate de roadmap). No presentar sus AUROC como benchmark externo.

---

## 7. Artefactos sellados (SHA-256, este ciclo)

| Artefacto | SHA-256 |
|:----------|:--------|
| frontier_v7_config.json | `b4993bd6b81e17298fc8e0c966be8a903b7ea524e819ae87bac440b289c04f7b` |
| frontier_calibration.json | `c56d42839e16bd13f7c2e313a425b7865279dddf8cfe22d62c09ff398f6b5f4d` |
| eval_E4E5_results.json | `c7e06228a0f8acae4ac8e0e35ad37996088622914d59e503592bba977b68a818` |
| eval_high_ver_fpr.json | `2fe5f6adea6673169d97b9cfc31b68ec7ea8aa5d1dcbbda0ac7a2497c5a7d227` |
| eval_negation_hardening.json | `5786d04dfac4744f9444c4576eca3dc66e961c7f40e8fbbf7d44bb18227ad5cf` |
| eval_E2_results.json (post-wiring) | `6fa68cebed13313ba7272d77126a3dda9e98556e7233c18f8fe8f40f7c16f343` |
| eval_E3_shadow.json (post-wiring) | `481188a41074c2cc3799e7f8bf7de38e5df7f82d9c5f15c73875ea69ab35ee14` |

Índice canónico: `evidence_index.json` (10 artefactos encadenados, verificado
coherente). Si no está en el índice, no existe para due diligence.

---

## 8. Pendientes reales (no bloqueantes)

1. `docker build` en host con Docker (ND en sandbox) — comandos WSL en el cierre.
2. Wiring del detector de negación endurecido a la extracción de verificabilidad
   de producción (`scripts/eval_e2_e3.py::verifiability`) — 1 línea.
3. Tier sentence-transformers (job CI `semantic-tier`) + corpus público
   HaluEval-style (gate de roadmap).
4. Revisión legal real del mapeo EU AI Act.

*Salida de un pipeline orquestado ('ARQ Orchestrator – Modo Arsenal') sobre un
LLM. Agregación multi-rol validada por veracidad, privacidad y gates (A/B/C).
Dirección humana: Richie. Confianza: alta en T1 y en los T2 sellados; media en
generalización fuera de calibración (nombrado en §6).*
