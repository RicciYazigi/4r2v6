"""
4R2 Coherence Kernel v6.0 — Canonical Single Source of Truth
Multi-layer coherence scoring & gating for LLM outputs.
Foundations: embedding geometry (angular metric) + information theory (JS divergence).
Explicitly NOT physical thermodynamics. Landauer is cited as conceptual inspiration only.

Locked design decisions v6.0:
  D1. d(a,b) = arccos(clip(cos))/π  — true metric, range [0,1], triangle inequality holds.
  D2. Weights live on the simplex; normalization is internal and mandatory.
  D3. F-layer = verifiability vector in [0,1]^4, never raw hardware magnitudes.
  D4. R_irr = λ·JS(π_t ‖ π_{t−1}) replaces physical Landauer cost.
  D5. Calibration = centered Platt: σ((raw−b)/T). Full [0,1] range.
  D6. Fail-closed: any exception in scoring ⇒ verdict BLOCK.
Supersedes: v5.2 CANON_FREEZE, v5.3.1 LLMsuper variant.
"""
from __future__ import annotations
import math, time, json
import numpy as np
from dataclasses import dataclass, field
from typing import Optional

EPS = 1e-12

# ---------- geometry ----------
def _unit(v: np.ndarray) -> np.ndarray:
    n = np.linalg.norm(v)
    if n < EPS:
        raise ValueError("zero-norm vector: refusing to score (fail-closed)")
    return v / n

def angular_distance(a: np.ndarray, b: np.ndarray) -> float:
    """True metric on the unit sphere, normalized to [0,1]."""
    if a.shape != b.shape:
        raise ValueError(f"dim mismatch {a.shape} vs {b.shape}: layers must share embedding space")
    cos = float(np.clip(np.dot(_unit(a), _unit(b)), -1.0, 1.0))
    return math.acos(cos) / math.pi

# ---------- information theory ----------
def js_divergence(p: np.ndarray, q: np.ndarray) -> float:
    """Jensen-Shannon divergence, bounded [0, ln2], symmetric, always finite."""
    p = np.clip(p, EPS, 1); p = p / p.sum()
    q = np.clip(q, EPS, 1); q = q / q.sum()
    m = 0.5 * (p + q)
    kl = lambda x, y: float(np.sum(x * np.log(x / y)))
    return 0.5 * kl(p, m) + 0.5 * kl(q, m)

# ---------- state ----------
@dataclass
class LayerState:
    normative: np.ndarray          # E(policy)           ∈ ℝ^d
    representational: np.ndarray   # E(user request)     ∈ ℝ^d
    informational: np.ndarray      # E(model output)     ∈ ℝ^d
    verifiability: np.ndarray      # (f_ground, f_num, f_cite, f_exec) ∈ [0,1]^4

    def validate(self):
        d = self.normative.shape
        assert self.representational.shape == d and self.informational.shape == d, \
            "N, R, I must share embedding dimension"
        assert self.verifiability.shape == (4,), "F must be [f_ground, f_num, f_cite, f_exec]"
        assert np.all(self.verifiability >= 0) and np.all(self.verifiability <= 1), "F ∈ [0,1]^4"

@dataclass
class Regime:
    theta: float = 0.35            # gate: pass iff C_total <= θ (v6: unbiased scale => tighter θ)
    lam: float = 0.30              # γ weight on R_irr
    weights: dict = field(default_factory=lambda: {"w_NR": 0.25, "w_RI": 0.25, "w_IF": 0.50})
    criticality: float = 0.0
    def __post_init__(self):
        self.theta = float(np.clip(self.theta, 0.0, 1.0))
        if self.criticality > 0.7:   # critical context => stricter gate
            self.theta = max(0.15, self.theta - 0.10)

def _simplex(w: dict) -> dict:
    v = np.array([max(EPS, w.get(k, 1/3)) for k in ("w_NR", "w_RI", "w_IF")])
    v = v / v.sum()
    return {"w_NR": float(v[0]), "w_RI": float(v[1]), "w_IF": float(v[2])}

# ---------- kernel ----------
class CoherenceKernel:
    def __init__(self, alpha: float = 1.0, gamma: float = 0.3, delta: float = 0.5):
        self.alpha, self.gamma, self.delta = alpha, gamma, delta
        self.history: list[dict] = []
        self._prev_policy: Optional[np.ndarray] = None   # π_{t−1} over {ALLOW,FLAG,BLOCK}

    def coherence(self, s: LayerState, weights: Optional[dict] = None) -> dict:
        s.validate()
        w = _simplex(weights or {})
        c_nr = angular_distance(s.normative, s.representational)
        c_ri = angular_distance(s.representational, s.informational)
        c_if = 1.0 - float(np.mean(s.verifiability))
        c_total = w["w_NR"]*c_nr + w["w_RI"]*c_ri + w["w_IF"]*c_if   # ∈ [0,1] by convexity
        out = {"C_NR": c_nr, "C_RI": c_ri, "C_IF": c_if, "C_total": c_total, "weights": w}
        self.history.append(out)
        return out

    def irreversibility(self, policy_t: np.ndarray) -> float:
        """R_irr for this step. policy_t = distribution over {ALLOW, FLAG, BLOCK}."""
        if self._prev_policy is None:
            self._prev_policy = policy_t
            return 0.0
        r = js_divergence(policy_t, self._prev_policy)
        self._prev_policy = policy_t
        return r

    def loss(self, base: float, c_total: float, r_irr: float, k_contra: float = 0.0) -> float:
        return base + self.alpha * max(0.0, c_total)**2 + self.gamma * r_irr + self.delta * k_contra

    def gate(self, s: LayerState, regime: Optional[Regime] = None,
             policy_t: Optional[np.ndarray] = None, k_contra: float = 0.0) -> dict:
        """End-to-end verdict. Fail-closed: any exception => BLOCK."""
        regime = regime or Regime()
        try:
            br = self.coherence(s, regime.weights)
            r_irr = self.irreversibility(policy_t if policy_t is not None
                                         else np.array([1.0, 0.0, 0.0]))
            L = self.loss(0.0, br["C_total"], r_irr, k_contra)
            passes = br["C_total"] <= regime.theta
            verdict = "ALLOW" if passes else ("FLAG" if br["C_total"] <= regime.theta + 0.15 else "BLOCK")
            return {"verdict": verdict, "C_total": br["C_total"], "L_4R2": L,
                    "R_irr": r_irr, "breakdown": br,
                    "regime": {"theta": regime.theta, "criticality": regime.criticality},
                    "fail_closed": False}
        except Exception as e:
            return {"verdict": "BLOCK", "error": str(e), "fail_closed": True}

# ---------- calibration (fixes F4) ----------
class CalibratedEvaluator:
    DEFAULTS = {f"c{i}": {"b": 0.5, "T": 0.15} for i in range(1, 8)}
    def __init__(self, params: Optional[dict] = None):
        self.params = params or dict(self.DEFAULTS)
    def calibrate(self, c_id: str, raw: float) -> float:
        p = self.params.get(c_id, {"b": 0.5, "T": 0.15})
        return float(np.clip(1.0 / (1.0 + math.exp(-(raw - p["b"]) / p["T"])), 0.0, 1.0))

# ---------- belief tracking (fixes F7) ----------
class BeliefTracker:
    """Log-odds opinion pooling with Ebbinghaus decay on episodic facts."""
    def __init__(self, tau_episodic_min: float = 20.0, threshold: float = 0.1):
        self._facts: dict[str, dict] = {}
        self._tau, self._thr = tau_episodic_min, threshold
    @staticmethod
    def _logit(p): p = min(max(p, EPS), 1 - EPS); return math.log(p / (1 - p))
    def update(self, content: str, p_obs: float, tag: str = "episodic", source: str = "untrusted"):
        kappa = 0.7 if source == "trusted" else 0.3
        key = content.lower().strip()
        prev = self._facts.get(key, {"l": 0.0})
        self._facts[key] = {"l": prev["l"] + kappa * self._logit(p_obs),
                            "t": time.time(), "tag": tag, "source": source, "content": content}
    def query(self, content: str) -> float:
        f = self._facts.get(content.lower().strip())
        if f is None: return 0.0
        p = 1.0 / (1.0 + math.exp(-f["l"]))
        if f["tag"] == "episodic":
            p *= math.exp(-((time.time() - f["t"]) / 60.0) / self._tau)
        return p
    def contradiction_cost(self, claims: list[str]) -> float:
        ps = [self.query(c) for c in claims]
        cost = 0.0
        for i in range(len(ps)):
            for j in range(i + 1, len(ps)):
                if min(ps[i], ps[j]) < self._thr: continue
                if (ps[i] - 0.5) * (ps[j] - 0.5) < 0:
                    cost += 0.5 * abs(ps[i] - ps[j])
        return cost

# ---------- self-test ----------
def selftest() -> dict:
    k = CoherenceKernel()
    v = np.array([0.3, -0.8, 0.5, 0.1])
    perfect = LayerState(v, v, v, np.ones(4))
    bad = LayerState(np.array([1., 0, 0, 0]), np.array([0., 1, 0, 0]),
                     np.array([0., 0, 1, 0]), np.array([0.2, 0.1, 0.0, 0.3]))
    gp, gb = k.gate(perfect), CoherenceKernel().gate(bad)
    ce = CalibratedEvaluator()
    checks = {
        "perfect_C_total_is_zero": abs(gp["C_total"]) < 1e-9,       # fixes F1 bias (was 0.1556)
        "perfect_verdict_ALLOW": gp["verdict"] == "ALLOW",
        "bad_verdict_BLOCK": gb["verdict"] == "BLOCK",
        "C_total_bounded": 0.0 <= gb["C_total"] <= 1.0,
        "calib_full_range": ce.calibrate("c1", 0.0) < 0.05 and ce.calibrate("c1", 1.0) > 0.95,
        "fail_closed_on_zero_vec": CoherenceKernel().gate(
            LayerState(np.zeros(4), v, v, np.ones(4)))["verdict"] == "BLOCK",
        "js_bounded": 0 <= js_divergence(np.array([.9,.05,.05]), np.array([.1,.1,.8])) <= math.log(2),
    }
    checks["ALL_PASS"] = all(checks.values())
    return checks

if __name__ == "__main__":
    print(json.dumps(selftest(), indent=2))
