"""Guardrail — the one-import product API over the canonical 4R2 kernel.
    from four_r2 import Guardrail
    g = Guardrail()
    d = g.evaluate(policy="...", request="...", response="...",
                   verifiability=(0.9, 1.0, 0.8, 0.7))
    if d.verdict == "BLOCK": ...
Guarantees (see docs/LIMITATIONS.md for the proven-vs-empirical split):
  - Deterministic: same inputs + same embedder => bit-identical C_total.
  - Fail-closed: ANY exception anywhere in the pipeline (embedding, kernel,
    malformed input) yields verdict BLOCK with fail_closed=True. evaluate()
    never raises.
  - C_total in [0,1] by convexity of the weighted sum of bounded distances.
  - Defense in depth preserved: convex gate (theta) + Layer Breach Breaker
    (ADR-0007) + optional VER fuse (verifiability floor).
Verifiability vector F = (f_ground, f_num, f_cite, f_exec) in [0,1]^4.
If the caller does not supply F, the default is (0.5, 0.5, 0.5, 0.5): a
neutral "unverified" prior (C_IF = 0.5). Precise semantics: it contributes
w_IF*0.5 to C_total instead of silently granting perfect physical coherence
(F=1 => C_IF=0), so unverified content always scores strictly worse than
verified content — but perfectly aligned N/R/I with the neutral prior can
still ALLOW under balanced weights (C_total ~= 0.167 <= theta 0.35). Supply
real F signals in production; that is what E2/T3 measured.
"""
from __future__ import annotations
import time
import math
from dataclasses import dataclass
from typing import Optional, Sequence
import numpy as np
from ._kernel_loader import load_kernel_module
from ._version import KERNEL_MATH_VERSION, __version__
from .embedders import HashingEmbedder
DEFAULT_VERIFIABILITY = (0.5, 0.5, 0.5, 0.5)
VER_FUSE_FLOOR_DEFAULT = 0.15   # mean(F) below floor => ALLOW downgraded to FLAG
VER_GROUND_FLOOR_DEFAULT = 0.15  # F[0] (grounding) below floor => ALLOW downgraded
# to FLAG. Rationale: adversarial camouflage inflates f_num/f_exec while the
# response stays unmoored from the request (f_ground ~ 0.1); a per-component
# floor is defense in depth analogous to LBB's per-layer cap. Floor value is
# EMPIRICAL (E2 corpus: benign min f_ground 0.214 vs adversarial min 0.057);
# recalibrate alongside theta when changing embedder or F pipeline.
@dataclass(frozen=True)
class Decision:
    verdict: str                 # ALLOW | FLAG | BLOCK
    c_total: float               # [0,1]; 1.0 on fail-closed
    breakdown: dict              # C_NR, C_RI, C_IF, weights ({} on fail-closed)
    lbb_trigger: Optional[str]   # None | LBB_FLAG | LBB_BLOCK
    ver_fuse: Optional[str]      # None | VER_FUSE_FLAG
    theta: float
    latency_ms: float
    fail_closed: bool
    reason: Optional[str]
    package_version: str = __version__
    kernel_math_version: str = KERNEL_MATH_VERSION
    def to_dict(self) -> dict:
        return {
            "verdict": self.verdict,
            "c_total": self.c_total,
            "breakdown": self.breakdown,
            "lbb_trigger": self.lbb_trigger,
            "ver_fuse": self.ver_fuse,
            "theta": self.theta,
            "latency_ms": self.latency_ms,
            "fail_closed": self.fail_closed,
            "reason": self.reason,
            "package_version": self.package_version,
            "kernel_math_version": self.kernel_math_version,
        }
def _block(reason: str, theta: float, t0: float) -> Decision:
    return Decision(
        verdict="BLOCK", c_total=1.0, breakdown={}, lbb_trigger=None,
        ver_fuse=None, theta=theta, latency_ms=(time.perf_counter() - t0) * 1000.0,
        fail_closed=True, reason=reason,
    )
class Guardrail:
    """Deterministic, fail-closed coherence guardrail for LLM agents."""
    def __init__(
        self,
        theta: float = 0.35,
        weights_profile: str = "balanced",
        embedder=None,
        default_verifiability: Sequence[float] = DEFAULT_VERIFIABILITY,
        intent_level: str = "EXPLORATORY",
        ver_fuse_floor: Optional[float] = VER_FUSE_FLOOR_DEFAULT,
        ver_ground_floor: Optional[float] = VER_GROUND_FLOOR_DEFAULT,
        governance_mode: bool = False,
    ):
        self._kmod = load_kernel_module()
        kernel_cls = self._kmod.CoherenceKernel
        if weights_profile not in kernel_cls.WEIGHT_PROFILES:
            raise ValueError(
                f"unknown weights_profile {weights_profile!r}; "
                f"valid: {sorted(kernel_cls.WEIGHT_PROFILES)}"
            )
        self.theta = float(np.clip(theta, 0.0, 1.0))
        self.weights = dict(kernel_cls.WEIGHT_PROFILES[weights_profile])
        self.weights_profile = weights_profile
        self.intent_level = intent_level
        self.ver_fuse_floor = ver_fuse_floor
        self.ver_ground_floor = ver_ground_floor
        self.embedder = embedder or HashingEmbedder()
        self.governance_mode = governance_mode
        f = np.asarray(default_verifiability, dtype=np.float64)
        if f.shape != (4,) or np.any(f < 0) or np.any(f > 1):
            raise ValueError("default_verifiability must be in [0,1]^4")
        self.default_verifiability = f
    # -- internal -----------------------------------------------------------
    def _regime(self, criticality: float):
        return self._kmod.Regime(
            theta=self.theta,
            weights=dict(self.weights),
            criticality=float(np.clip(criticality, 0.0, 1.0)),
            intent_level=self.intent_level,
        )
    # -- public API ---------------------------------------------------------
    def evaluate(
        self,
        policy: str,
        request: str,
        response: str,
        verifiability: Optional[Sequence[float]] = None,
        criticality: float = 0.0,
    ) -> Decision:
        """Score one agent decision. Never raises; fail-closed => BLOCK."""
        t0 = time.perf_counter()
        try:
            f = (
                np.asarray(verifiability, dtype=np.float64)
                if verifiability is not None
                else self.default_verifiability.copy()
            )
            if f.shape != (4,) or np.any(f < 0) or np.any(f > 1) or not np.all(np.isfinite(f)):
                raise ValueError("verifiability must be finite and in [0,1]^4")
            state = self._kmod.LayerState(
                normative=self.embedder.embed(policy),
                representational=self.embedder.embed(request),
                informational=self.embedder.embed(response),
                physical=f,
            )
            regime = self._regime(criticality)
            kernel = self._kmod.CoherenceKernel(weights=dict(self.weights))
            c_total, res = kernel.compute_with_regime(state, regime)
            verdict = res["verdict"]
            ver_fuse = None
            if verdict == "ALLOW":
                if self.ver_fuse_floor is not None and float(np.mean(f)) < self.ver_fuse_floor:
                    verdict, ver_fuse = "FLAG", "VER_FUSE_FLAG"
                elif self.ver_ground_floor is not None and float(f[0]) < self.ver_ground_floor:
                    verdict, ver_fuse = "FLAG", "VER_FUSE_GROUND"

            if self.governance_mode:
                # Calculate angular distance C_NI
                norm_a = state.normative
                norm_b = state.informational
                n_a = np.linalg.norm(norm_a)
                n_b = np.linalg.norm(norm_b)
                if n_a < 1e-12 or n_b < 1e-12:
                    raise ValueError("zero-norm vector: refusing to score (fail-closed)")
                unit_a = norm_a / n_a
                unit_b = norm_b / n_b
                cos = float(np.clip(np.dot(unit_a, unit_b), -1.0, 1.0))
                c_ni = math.acos(cos) / math.pi
                
                c_total = c_ni
                
                # Verdict based on governance score C_NI and regime.theta
                if c_ni <= regime.theta:
                    verdict = "ALLOW"
                elif c_ni <= regime.theta + 0.15:
                    verdict = "FLAG"
                else:
                    verdict = "BLOCK"
                
                # Enforce safety overrides (fail-closed and LBB_BLOCK)
                if bool(res.get("fail_closed", False)):
                    verdict = "BLOCK"
                elif res.get("lbb_trigger") == "LBB_BLOCK":
                    verdict = "BLOCK"

            breakdown = dict(res.get("breakdown", {})) if isinstance(res.get("breakdown"), dict) else {}
            if self.governance_mode and breakdown:
                breakdown["C_NI"] = c_ni
                breakdown["C_total"] = c_ni

            return Decision(
                verdict=verdict,
                c_total=float(c_total),
                breakdown=breakdown,
                lbb_trigger=res.get("lbb_trigger"),
                ver_fuse=ver_fuse,
                theta=regime.theta,
                latency_ms=(time.perf_counter() - t0) * 1000.0,
                fail_closed=bool(res.get("fail_closed", False))
                or not isinstance(res.get("breakdown"), dict)
                or not res.get("breakdown"),
                reason=res.get("error"),
            )
        except Exception as e:  # noqa: BLE001 — fail-closed by design
            return _block(f"{type(e).__name__}: {e}", self.theta, t0)
    def selftest(self) -> dict:
        """Kernel invariants (perfect_c == 0.0 etc.) via the canonical kernel."""
        return self._kmod.CoherenceKernel.selftest()
