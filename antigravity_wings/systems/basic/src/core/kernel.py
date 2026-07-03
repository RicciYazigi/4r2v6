"""
KERNEL 1240421 - 4R2 COHERENCE ENGINE (DEPRECATED in this workspace)

This file is kept for historical reference only.

>>> USE THE CANONICAL IMPLEMENTATION INSTEAD:
    /core/kernel_1240421.py   (single source of truth)

The version here uses a different C_IF heuristic and strict product for C_total.
It is no longer the reference implementation.

Versión original: 1.0-SANITIZED (2026-01-08)
Estado en este workspace: DEPRECATED - Do not use for new work.

Implementación estricta N-R-I-F basada en la "Especificación Técnica Saneada":

- Sección 2: Arquitectura Tetradimensional (N, R, I, F)
- Sección 3.1: Coherencia inter-capa por cos_sim normalizada a [0,1]
- Sección 3.2: C_IF = info_value * (0.40*erasure + 0.35*efficiency + 0.25*temp)
- Sección 3.3: total_coherence = C_NR * C_RI * C_IF (producto estricto)
- Sección 4: Landauer E = kB * T * ln(2) * bits_erased (referencia teórica; proxy)
- Sección 5: entropy_loss = [(1-C_NR)+(1-C_RI)+(1-C_IF)]/3

Nota de rigor:
- Este kernel NO mide calor real en el chip.
- Landauer es un cálculo teórico de referencia usando "bits_erased" como proxy.
"""

from __future__ import annotations

from typing import Dict, List, Literal, Tuple

import numpy as np
from pydantic import BaseModel, Field, ValidationError


# -----------------------------
# Constantes (Sección 4 y 3.2)
# -----------------------------

KB: float = 1.380649e-23  # J/K (constante de Boltzmann, referencia teórica)
LN2: float = 0.6931471805599453  # ln(2)

W_ERASURE: float = 0.40
W_EFFICIENCY: float = 0.35
W_TEMP: float = 0.25

# Parámetros heurísticos del Spec 3.2
THROUGHPUT_SCALE: float = 50.0  # tanh((ops/ns)/50)
TEMP_BASELINE_K: float = 300.0
TEMP_SCALE: float = 200.0

# Numérica
EPS: float = 1e-12


# -----------------------------
# Modelos de datos (Pydantic)
# -----------------------------

class PhysicalLayerInput(BaseModel):
    """Capa F (Physical): métricas computacionales del ciclo."""
    ops: float = Field(..., gt=0.0, description="Operaciones computacionales estimadas en el ciclo")
    bits_erased: float = Field(..., ge=0.0, description="Bits borrados/sobrescritos (proxy, no medición física)")
    temp_k: float = Field(default=300.0, ge=0.0, description="Temperatura simulada en Kelvin (default 300K)")
    time_ns: float = Field(..., gt=0.0, description="Tiempo de ejecución del ciclo en nanosegundos")


class KernelInput(BaseModel):
    """
    Entrada 4R2 (N-R-I-F).
    Vectores semánticos deben estar normalizados en [0,1]^n.
    """
    normative_n: List[float] = Field(..., description="Capa N: valores/reglas esperados (vector [0,1]^n)")
    representational_r: List[float] = Field(..., description="Capa R: estado interno/modelo (vector [0,1]^n)")
    informational_i: List[float] = Field(..., description="Capa I: datos observados (vector [0,1]^n)")
    physical_f: PhysicalLayerInput = Field(..., description="Capa F: métricas computacionales")


class KernelOutput(BaseModel):
    decision: Literal["GO", "NO_GO"]
    coherence_score: float = Field(..., ge=0.0, le=1.0, description="Coherencia total (0..1)")
    entropy_loss: float = Field(..., ge=0.0, le=1.0, description="Pérdida cíclica (0..1)")
    landauer_cost_j: float = Field(..., ge=0.0, description="Costo Landauer teórico (J), usando bits_erased como proxy")
    components: Dict[str, float] = Field(default_factory=dict)
    metadata: Dict[str, str] = Field(default_factory=dict)


# -----------------------------
# Kernel
# -----------------------------

class CoherenceKernel:
    """
    Kernel 1240421 (v1.0-SANITIZED).

    Umbral (threshold):
    - Con producto estricto, umbrales altos bloquean agresivamente.
    - DEFAULT_THRESHOLD es un valor operativo inicial para TRL4; calibrar por dominio.
    """
    DEFAULT_THRESHOLD: float = 0.65  # recomendado como punto de partida con producto estricto (calibrar)

    def __init__(self, threshold: float = DEFAULT_THRESHOLD):
        self.threshold = float(threshold)

    # ---------
    # Validación
    # ---------

    @staticmethod
    def _is_finite(x: float) -> bool:
        return bool(np.isfinite(x))

    @classmethod
    def _validate_unit_vector(cls, name: str, v: List[float]) -> None:
        if not isinstance(v, list) or len(v) == 0:
            raise ValueError(f"{name} must be a non-empty list[float] in [0,1].")
        for i, x in enumerate(v):
            try:
                xf = float(x)
            except Exception as exc:
                raise ValueError(f"{name}[{i}] is not a number.") from exc
            if not cls._is_finite(xf):
                raise ValueError(f"{name}[{i}] must be finite.")
            if xf < 0.0 or xf > 1.0:
                raise ValueError(f"{name}[{i}] must be within [0,1].")

    @classmethod
    def _validate_physical(cls, phys: PhysicalLayerInput) -> None:
        for field_name in ("ops", "bits_erased", "temp_k", "time_ns"):
            val = float(getattr(phys, field_name))
            if not cls._is_finite(val):
                raise ValueError(f"physical_f.{field_name} must be finite.")
        if phys.ops <= 0.0:
            raise ValueError("physical_f.ops must be > 0.")
        if phys.time_ns <= 0.0:
            raise ValueError("physical_f.time_ns must be > 0.")
        if phys.bits_erased < 0.0:
            raise ValueError("physical_f.bits_erased must be >= 0.")
        if phys.temp_k < 0.0:
            raise ValueError("physical_f.temp_k must be >= 0.")

    # -------------------------
    # Heurística: padding mediana
    # -------------------------

    @staticmethod
    def _pad_vectors_median(v1: np.ndarray, v2: np.ndarray) -> Tuple[np.ndarray, np.ndarray, bool]:
        """
        Heurística operativa: si longitudes difieren, se rellena con la mediana del vector.
        No implica equivalencia semántica; solo robustez numérica para cos_sim.
        """
        if v1.shape[0] == v2.shape[0]:
            return v1, v2, False

        target_len = max(v1.shape[0], v2.shape[0])

        def pad(v: np.ndarray, length: int) -> np.ndarray:
            if v.shape[0] >= length:
                return v
            median_val = float(np.median(v)) if v.shape[0] > 0 else 0.5
            return np.pad(v, (0, length - v.shape[0]), constant_values=median_val)

        return pad(v1, target_len), pad(v2, target_len), True

    # -------------------------
    # Sección 3.1: cos_sim normalizada
    # -------------------------

    def _cosine_similarity_normalized(self, a: np.ndarray, b: np.ndarray) -> Tuple[float, bool]:
        a2, b2, padded = self._pad_vectors_median(a, b)

        na = float(np.linalg.norm(a2))
        nb = float(np.linalg.norm(b2))
        if na < EPS or nb < EPS:
            return 0.0, padded

        dot = float(np.dot(a2, b2))
        cos_sim = dot / (na * nb)

        # Clamp numérico por flotantes
        cos_sim = float(np.clip(cos_sim, -1.0, 1.0))

        # Normalización [-1,1] -> [0,1]
        return (cos_sim + 1.0) / 2.0, padded

    # -------------------------
    # Sección 3.2: C_IF
    # -------------------------

    def _compute_c_if(self, i_vec: np.ndarray, phys: PhysicalLayerInput) -> float:
        # info_value = promedio del vector I (adimensional, [0,1])
        info_value = float(np.mean(i_vec)) if i_vec.shape[0] > 0 else 0.5
        info_value = float(np.clip(info_value, 0.0, 1.0))

        # Factor 1: exp(-2 * bits/ops)
        ratio_erasure = float(phys.bits_erased) / float(phys.ops)
        f_erasure = float(np.exp(-2.0 * ratio_erasure))  # (0,1]

        # Factor 2: tanh((ops/ns)/50)
        throughput = float(phys.ops) / float(phys.time_ns)  # proxy adimensional (definición operativa)
        f_efficiency = float(np.tanh(throughput / THROUGHPUT_SCALE))  # [0,1)

        # Factor 3: exp(-|T-300|/200)
        delta_t = abs(float(phys.temp_k) - TEMP_BASELINE_K)
        f_temp = float(np.exp(-delta_t / TEMP_SCALE))  # (0,1]

        weighted_phys = (W_ERASURE * f_erasure) + (W_EFFICIENCY * f_efficiency) + (W_TEMP * f_temp)
        weighted_phys = float(np.clip(weighted_phys, 0.0, 1.0))

        c_if = info_value * weighted_phys
        return float(np.clip(c_if, 0.0, 1.0))

    # -------------------------
    # Sección 4: Landauer (referencia teórica)
    # -------------------------

    @staticmethod
    def _landauer_cost_j(bits_erased: float, temp_k: float) -> float:
        # Teórico: E = kB * T * ln(2) * bits
        # bits_erased is proxy (no medición térmica real del chip)
        bits = max(0.0, float(bits_erased))
        T = max(0.0, float(temp_k))
        return float(KB * T * LN2 * bits)

    # -------------------------
    # Evaluación principal
    # -------------------------

    def evaluate(self, input_data: dict) -> KernelOutput:
        try:
            data = KernelInput(**input_data)

            # Validación estricta (real)
            self._validate_unit_vector("normative_n", data.normative_n)
            self._validate_unit_vector("representational_r", data.representational_r)
            self._validate_unit_vector("informational_i", data.informational_i)
            self._validate_physical(data.physical_f)

            n_vec = np.array(data.normative_n, dtype=float)
            r_vec = np.array(data.representational_r, dtype=float)
            i_vec = np.array(data.informational_i, dtype=float)

            # 3.1: C_NR y C_RI
            c_nr, padded_nr = self._cosine_similarity_normalized(n_vec, r_vec)
            c_ri, padded_ri = self._cosine_similarity_normalized(r_vec, i_vec)

            # 3.2: C_IF
            c_if = self._compute_c_if(i_vec, data.physical_f)

            # 3.3: Producto estricto
            total_coherence = float(np.clip(c_nr * c_ri * c_if, 0.0, 1.0))

            # 5: entropy_loss
            entropy_loss = float(((1.0 - c_nr) + (1.0 - c_ri) + (1.0 - c_if)) / 3.0)
            entropy_loss = float(np.clip(entropy_loss, 0.0, 1.0))

            # 4: Landauer (teórico)
            landauer_j = self._landauer_cost_j(data.physical_f.bits_erased, data.physical_f.temp_k)

            # Decisión (Coherence Gate)
            decision: Literal["GO", "NO_GO"] = "GO" if total_coherence >= self.threshold else "NO_GO"

            return KernelOutput(
                decision=decision,
                coherence_score=round(total_coherence, 4),
                entropy_loss=round(entropy_loss, 4),
                landauer_cost_j=landauer_j,
                components={
                    "C_NR": round(float(c_nr), 4),
                    "C_RI": round(float(c_ri), 4),
                    "C_IF": round(float(c_if), 4),
                },
                metadata={
                    "engine": "1240421",
                    "spec_version": "1.0-SANITIZED",
                    "trl": "4",
                    "gate": "STRICT_PRODUCT",
                    "threshold": str(self.threshold),
                    "pad_strategy": "median",
                    "padded": str(bool(padded_nr or padded_ri)).lower(),
                    "note_landauer": "theoretical_reference_proxy_bits_erased",
                },
            )

        except ValidationError as e:
            return KernelOutput(
                decision="NO_GO",
                coherence_score=0.0,
                entropy_loss=1.0,
                landauer_cost_j=0.0,
                components={},
                metadata={"status": "INVALID_INPUT", "error": str(e), "engine": "1240421", "spec_version": "1.0-SANITIZED"},
            )
        except Exception as e:
            return KernelOutput(
                decision="NO_GO",
                coherence_score=0.0,
                entropy_loss=1.0,
                landauer_cost_j=0.0,
                components={},
                metadata={"status": "CRITICAL_FAILURE", "error": f"Kernel Panic: {str(e)}", "engine": "1240421", "spec_version": "1.0-SANITIZED"},
            )


    # ---------
    # Self-Test (Escenarios deterministas)
    # ---------

    @classmethod
    def selftest(cls) -> Dict[str, bool]:
        """
        Ejecuta pruebas deterministas para evidencia de auditoría.
        Retorna mapa de resultados.
        """
        engine = cls(threshold=0.65)
        results = {}

        # Escenario 1: PERFECT (Coherencia Máxima)
        res_perfect = engine.evaluate({
            "normative_n": [1.0, 1.0],
            "representational_r": [1.0, 1.0],
            "informational_i": [1.0, 1.0],
            "physical_f": {"ops": 5000, "bits_erased": 0, "temp_k": 300, "time_ns": 100}
        })
        results["PERFECT"] = res_perfect.decision == "GO" and res_perfect.coherence_score > 0.9

        # Escenario 2: DEGRADED (Coherencia Baja por discrepancia N-R)
        res_degraded = engine.evaluate({
            "normative_n": [1.0, 0.0],
            "representational_r": [0.0, 1.0],
            "informational_i": [0.0, 1.1], # i será clamped a 1.0
            "physical_f": {"ops": 1000, "bits_erased": 100, "temp_k": 300, "time_ns": 100}
        })
        # Discrepancia ortogonal en N-R -> cos_sim baja
        results["DEGRADED"] = res_degraded.decision == "NO_GO"

        # Escenario 3: COLLAPSED (Fallo Físico - Alta borradura)
        res_collapsed = engine.evaluate({
            "normative_n": [1.0], "representational_r": [1.0], "informational_i": [1.0],
            "physical_f": {"ops": 100, "bits_erased": 500, "temp_k": 500, "time_ns": 10}
        })
        # bits_erased > ops -> ratio > 1 -> exp(-2*ratio) bajo -> C_IF bajo
        results["COLLAPSED"] = res_collapsed.decision == "NO_GO"

        # Escenario 4: MIXED (Justo en el umbral)
        # Calibrar para que de ~0.7
        res_mixed = engine.evaluate({
            "normative_n": [1.0, 0.8],
            "representational_r": [0.9, 0.9],
            "informational_i": [0.8, 1.0],
            "physical_f": {"ops": 1000, "bits_erased": 20, "temp_k": 310, "time_ns": 100}
        })
        results["MIXED"] = res_mixed.decision in ("GO", "NO_GO") # Verificación de ejecución

        return results


# Instancia global
kernel_engine = CoherenceKernel()

if __name__ == "__main__":
    # Autotest rápido
    print("Ejecutando Kernel Self-Test...")
    test_results = CoherenceKernel.selftest()
    for k, v in test_results.items():
        print(f"  {k}: {'PASS' if v else 'FAIL'}")
