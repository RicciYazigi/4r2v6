"""Data-driven theta calibration (the E2 percentile procedure, productized).
theta is EMBEDDER-SPECIFIC. The canonical default (0.35) was calibrated for
the angular scale; when you switch embedders or domains you must recalibrate:
    theta* = ( p95(C_total | benign) + p5(C_total | grave) ) / 2
Honesty rule: if the distributions overlap (p95_benign >= p5_grave) there is
NO clean threshold for this embedder/corpus. We then report status="OVERLAP",
keep theta at the fail-safe default, and rely on LBB + VER fuse — we do NOT
invent a midpoint that pretends separation exists.
Cases are dicts: {"policy": str, "request": str, "response": str,
                  "verifiability": [4 floats] (optional), "label": "benign"|"grave"}
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable, Optional
import numpy as np
@dataclass(frozen=True)
class CalibrationReport:
    status: str            # "OK" | "OVERLAP" | "INSUFFICIENT_DATA"
    theta_star: float      # recommended theta (default kept on OVERLAP)
    p95_benign: Optional[float]
    p5_grave: Optional[float]
    separation: Optional[float]   # p5_grave - p95_benign (positive = clean split)
    n_benign: int
    n_grave: int
    notes: str
    def to_dict(self) -> dict:
        return self.__dict__.copy()
def _scores(guardrail, cases: Iterable[dict]) -> list[float]:
    out = []
    for c in cases:
        d = guardrail.evaluate(
            c["policy"], c["request"], c["response"], c.get("verifiability")
        )
        # fail-closed cases score 1.0 by contract; include them (worst case)
        out.append(d.c_total)
    return out
def calibrate_theta(
    guardrail,
    benign_cases: list[dict],
    grave_cases: list[dict],
    min_per_class: int = 20,
    fallback_theta: float = 0.35,
) -> CalibrationReport:
    if len(benign_cases) < min_per_class or len(grave_cases) < min_per_class:
        return CalibrationReport(
            status="INSUFFICIENT_DATA", theta_star=fallback_theta,
            p95_benign=None, p5_grave=None, separation=None,
            n_benign=len(benign_cases), n_grave=len(grave_cases),
            notes=f"need >= {min_per_class} cases per class; keeping theta={fallback_theta}",
        )
    b = np.asarray(_scores(guardrail, benign_cases))
    g = np.asarray(_scores(guardrail, grave_cases))
    p95b = float(np.percentile(b, 95))
    p5g = float(np.percentile(g, 5))
    sep = p5g - p95b
    if sep <= 0:
        return CalibrationReport(
            status="OVERLAP", theta_star=fallback_theta,
            p95_benign=round(p95b, 4), p5_grave=round(p5g, 4),
            separation=round(sep, 4),
            n_benign=len(b), n_grave=len(g),
            notes=("benign/grave C_total distributions overlap for this embedder; "
                   "no clean theta exists — keeping fail-safe default and relying "
                   "on LBB + VER fuse. Consider a stronger embedder or better F signals."),
        )
    theta_star = round((p95b + p5g) / 2.0, 4)
    return CalibrationReport(
        status="OK", theta_star=theta_star,
        p95_benign=round(p95b, 4), p5_grave=round(p5g, 4),
        separation=round(sep, 4), n_benign=len(b), n_grave=len(g),
        notes="theta* = midpoint(p95 benign, p5 grave); re-run on domain drift.",
    )
