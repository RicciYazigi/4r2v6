# Validación independiente Fase 3 — co-arquitecto (held-out)

**Método:** reproduje la fórmula de gobernanza de Antigravity desde su spec
(C_NI = distancia angular normalizada policy↔response, arccos(cos)/π), sin leer
su código (llegaba truncado por el mount), y la probé en el split HELD-OUT del
benchmark que Antigravity NUNCA vio. Kernel verificado por hash.

## 1. Integridad del kernel congelado — OK
`core/kernel_v6.py` y `core/kernel_1240421.py`: **sha256 del working-tree =
sha256 del commit**. Antigravity no tocó la matemática congelada. Confirmado.

## 2. Reproducción del método (independiente) — coincide
| Señal | AUROC léxico | AUROC semántico |
|-------|--------------|-----------------|
| baseline c_total kernel | 0.358 | 0.281 |
| C_NI (gobernanza) DEV n=42 | 0.773 | 0.800 |

Coincide exacto con lo reportado por Antigravity. El método es correcto.

## 3. Validación anti-gaming en HELD-OUT (n=8, +4/−4) — PASA
| | DEV (n=42) | HELD-OUT (n=8) |
|---|---|---|
| Léxico AUROC | 0.773 | 0.938 |
| Semántico AUROC | 0.800 | 0.812 |
| ASR/ORR léxico (θ=0.38) | 33%/24% | 25%/25% |
| ASR/ORR semántico (θ=0.31) | 24%/29% | 25%/0% |

La discriminación **generaliza** al split no visto (no colapsa a azar ni se
invierte). Como C_NI es una fórmula FIJA (no entrenada; solo θ se calibró en dev),
esto era lo esperado y se confirma. **La mejora es real, no sobreajuste.**
*Caveat:* held-out n=8 es pequeño (IC amplio); la evidencia fuerte es dev n=42 +
consistencia en held-out.

## 4. Lectura honesta (para no sobrevender)
En `governance_mode`, el score = **C_NI puro** (w=1.0); mezclar con la señal del
kernel la degradaba. Es decir: **no es que el kernel NRIF de 4R2 ahora discrimine**
— se añadió un detector NUEVO y separado (coherencia policy↔response) junto al
kernel congelado, y ESE detector es el que funciona. La coherencia NRIF original
sigue sin discriminar esta tarea.

Implicación estratégica: el detector que funciona es una técnica estándar
(distancia de embeddings policy↔response), no la maquinaria distintiva de 4R2.
Valor: 4R2 ya TIENE un modo de gobernanza de respuestas útil y opt-in. Pero el
"win" no viene de la salsa secreta del kernel — conviene tenerlo claro para
IP/posicionamiento.

## 5. Lo que NO pude verificar desde el sandbox
El artefacto de código `four_r2/guardrail.py` de Antigravity llega truncado por
el mount; no pude ejecutarlo aquí. Verifiqué el MÉTODO y el kernel, no el archivo.
Pendiente: confirmar localmente que su `pytest` (145 verde) corre en tu máquina.

**Veredicto:** Fase 3 válida. Mejora real y generalizante, kernel intacto,
opt-in. Listo para decidir si se commitea (local) y cómo se posiciona.
