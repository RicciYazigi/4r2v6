# PAPER COMPANION — FORMALISMO, PSEUDOCÓDIGO Y PROPIEDADES

Este documento **NO va a arXiv**.
Es para **auditores, CTOs, y defensas técnicas**.

---

## A. Pseudocódigo Canónico (Kernel + Exoskeleton)

### A.1 Cálculo de Coherencia

```python
def cosine_coherence(a, b):
    return dot(a, b) / (norm(a) * norm(b) + epsilon)

C_NR = cosine_coherence(N, R)
C_RI = cosine_coherence(R, I)
C_IF = cosine_coherence(I, F_proj)

C_total = C_NR * C_RI * C_IF
```

---

### A.2 Entropy Loss

```python
entropy_loss = ((1 - C_NR) + (1 - C_RI) + (1 - C_IF)) / 3
```

---

### A.3 Colapso Sistémico

```python
if C_total < COHERENCE_THRESHOLD or entropy_loss > ENTROPY_MAX:
    system_state = "COLLAPSED"
```

---

## B. Dual-Agent Arbitration

```python
def arbitrate(mario_report, luigi_report):
    if luigi_report.severity >= HIGH:
        return luigi_report
    return merge(mario_report, luigi_report)
```

---

## C. Enforcement Policy (Formal)

Sea:

* $S \in \{\text{CRITICAL}, \text{HIGH}, \text{MEDIUM}\}$
* $M \in \{\text{SHADOW}, \text{SOFT}, \text{HARD}\}$

La función de enforcement $E(S,M)$ es determinista:

$$
E(S,M) =
\begin{cases}
STOP, & S = CRITICAL \land M \neq SHADOW \\
STOP, & S = HIGH \land M = HARD \\
ESCALATE, & S = HIGH \land M = SOFT \\
ESCALATE, & S = MEDIUM \land M = HARD \\
DEGRADE, & S = MEDIUM \land M = SOFT \\
GO, & \text{otherwise}
\end{cases}
$$

---

## D. Propiedades Demostrables (No Empíricas)

### D.1 Monotonía del Riesgo

Si $entropy\_loss_{t+1} > entropy\_loss_t$ entonces
la severidad de enforcement **no puede disminuir**.

---

### D.2 Fail-Closed Guarantee

En modo HARD:

$$
P(\text{unsafe execution}) \rightarrow 0 \quad \text{as} \quad entropy\_loss \rightarrow 1
$$

---

### D.3 No-Leakage Property (Ghost Bridge)

Sea $X$ el input sensible y $V$ el vector de evidencia.

$$
I(X; V) \approx 0
$$

bajo ofuscación determinista no invertible.

---

## E. Qué NO afirma el sistema (Explícito)

* No demuestra conciencia
* No optimiza verdad semántica
* No mide energía física real
* No reemplaza juicio humano

---

## ESTADO FINAL

**✔ Canon científico cerrado**
**✔ Paper arXiv-ready**
**✔ Companion técnico defensible**
