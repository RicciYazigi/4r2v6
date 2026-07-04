"""
4R2 Coherence Kernel - Canonical Implementation of Algorithm 1240421

Location: core/kernel_1240421.py (Single Source of Truth)
Version: v6.1.0 (ADR-0006 angular canon + ADR-0007 Layer Breach Breaker & fail-closed wrapper)

This file wraps the core v6.0 mathematical logic from kernel_v6.py to maintain
strict backward compatibility with all v5 interfaces.

v6.0.1 changes (2026-07-04, ADR-0006):
  - C_IF dual-path: F in [0,1]^4 => verifiability semantics (1 - mean);
    F outside [0,1] (raw telemetry) => angular distance on zero-padded unit
    vectors. Removes the silent-clip blind spot where raw hardware magnitudes
    scored C_IF = 0 (false perfect physical coherence).
  - Regime.theta default recalibrated 0.75 -> 0.35 for the angular scale
    (old 1-cos thresholds map via d_new = arccos(1 - d_old)/pi).
  - CRITICAL intent now TIGHTENS the gate (theta - 0.10), fixing a
    directional inversion (previously theta + 0.10 relaxed it).
  - Weight-profile registry added per ADR-0005 (PHYSICS_PRIORITY_PROFILE etc.).
"""

import numpy as np
import math
import time
import json
import logging
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
import kernel_v6

K_BOLTZMANN = 1.38e-23
ROOM_TEMP = 300
LANDAUER_MIN = K_BOLTZMANN * ROOM_TEMP * np.log(2)

@dataclass
class LayerState:
    normative: np.ndarray
    representational: np.ndarray
    informational: np.ndarray
    physical: np.ndarray

    def validate(self):
        assert isinstance(self.normative, np.ndarray)
        assert isinstance(self.representational, np.ndarray)
        assert isinstance(self.informational, np.ndarray)
        assert isinstance(self.physical, np.ndarray)
        assert len(self.physical) == 4

@dataclass
class Regime:
    # v6 angular scale: gate passes iff C_total <= theta. 0.35 == v6 canonical
    # default (old 1-cos threshold 0.65 maps to arccos(0.35)/pi ~= 0.386).
    theta: float = 0.35
    lambda_landauer: float = 0.25
    weights: dict = None
    mode: str = "B"
    criticality: float = 0.0
    intent_level: str = "EXPLORATORY"

    def __post_init__(self):
        if self.weights is None:
            self.weights = {'w_NR': 0.25, 'w_RI': 0.25, 'w_IF': 0.50}
        self.theta = max(0.0, min(1.0, self.theta))
        self.lambda_landauer = max(0.01, min(1.0, self.lambda_landauer))
        if self.intent_level == "CRITICAL":
            # ADR-0006: critical intent TIGHTENS the gate (fail-closed).
            self.theta = max(0.15, self.theta - 0.10)

class CoherenceKernel:
    # ADR-0005 named weight-profile registry. BALANCED is the mandatory
    # production default for Hard-Gate evaluation. PHYSICS_PRIORITY is
    # explicit opt-in only (normative blind-spot vulnerability documented).
    BALANCED_PROFILE = {'w_NR': 1/3, 'w_RI': 1/3, 'w_IF': 1/3}
    PHYSICS_PRIORITY_PROFILE = {'w_NR': 1/21, 'w_RI': 4/21, 'w_IF': 16/21}
    NORMATIVE_PRIORITY_PROFILE = {'w_NR': 0.50, 'w_RI': 0.30, 'w_IF': 0.20}
    REGIME_DEFAULT_PROFILE = {'w_NR': 0.25, 'w_RI': 0.25, 'w_IF': 0.50}
    WEIGHT_PROFILES = {
        'balanced': BALANCED_PROFILE,
        'physics_priority': PHYSICS_PRIORITY_PROFILE,
        'normative_priority': NORMATIVE_PRIORITY_PROFILE,
        'regime_default': REGIME_DEFAULT_PROFILE,
    }

    def __init__(
        self,
        lambda_landauer: float = 0.05,
        beta_coherence: float = 0.1,
        weights: Optional[Dict[str, float]] = None,
        logging_level: int = logging.INFO
    ):
        self.lambda_landauer = lambda_landauer
        self.beta_coherence = beta_coherence
        self.weights = weights or {'w_NR': 1/3, 'w_RI': 1/3, 'w_IF': 1/3}
        assert abs(sum(self.weights.values()) - 1.0) < 1e-6
        self.history: List[Dict] = []
        logging.basicConfig(level=logging_level)
        self.logger = logging.getLogger(__name__)
        self._v6_kernel = kernel_v6.CoherenceKernel()
        self.belief_tracker = BeliefTracker()
        self.calibrator = CalibratedEvaluator()
        self.domain_kernel = DomainKernel()

    def _safe_norm(self, vec: np.ndarray, epsilon: float = 1e-8) -> np.ndarray:
        norm = np.linalg.norm(vec)
        return vec / (norm + epsilon)

    def compute_C_NR(self, normative: np.ndarray, representational: np.ndarray) -> float:
        return kernel_v6.angular_distance(normative, representational)

    def compute_C_RI(self, representational: np.ndarray, informational: np.ndarray) -> float:
        return kernel_v6.angular_distance(representational, informational)

    def compute_C_IF(self, informational: np.ndarray, physical: np.ndarray) -> float:
        """Dual-path C_IF (ADR-0006).

        Path A (canonical v6): F in [0,1]^4 is a verifiability vector
        (f_ground, f_num, f_cite, f_exec) => C_IF = 1 - mean(F).
        Path B (legacy raw telemetry): any component outside [0,1] means F is
        raw hardware magnitudes => angular distance between zero-padded,
        re-normalized I and F (ADR-0001 geometry, angular scale). This removes
        the silent-clip blind spot where clip([1000,8,50,10]) -> [1,1,1,1]
        yielded C_IF = 0 (false perfect physical coherence).
        Both paths return values in [0, 1].
        """
        p = np.asarray(physical, dtype=float)
        if np.all((p >= 0.0) & (p <= 1.0)):
            return 1.0 - float(np.mean(p))
        i = self._safe_norm(np.asarray(informational, dtype=float))
        pn = self._safe_norm(p)
        size = max(len(i), len(pn))
        ia = np.zeros(size); ia[:len(i)] = i
        pa = np.zeros(size); pa[:len(pn)] = pn
        return kernel_v6.angular_distance(ia, pa)

    def _verifiability_proxy(self, state: 'LayerState') -> np.ndarray:
        """Map F to a valid v6 verifiability vector. If F is already in
        [0,1]^4 use it as-is; otherwise inject the legacy angular C_IF so the
        v6 pipeline (1 - mean) reproduces the dual-path value exactly."""
        p = np.asarray(state.physical, dtype=float)
        if np.all((p >= 0.0) & (p <= 1.0)):
            return p
        c_if = self.compute_C_IF(state.informational, state.physical)
        return np.full(4, float(np.clip(1.0 - c_if, 0.0, 1.0)))

    def compute_coherence_total(self, state: LayerState, weights: Optional[Dict[str, float]] = None) -> Tuple[float, Dict]:
        state.validate()
        w = weights or self.weights
        w_simplex = kernel_v6._simplex(w)
        c_nr = self.compute_C_NR(state.normative, state.representational)
        c_ri = self.compute_C_RI(state.representational, state.informational)
        c_if = self.compute_C_IF(state.informational, state.physical)
        c_total = w_simplex['w_NR'] * c_nr + w_simplex['w_RI'] * c_ri + w_simplex['w_IF'] * c_if
        breakdown = {'C_NR': c_nr, 'C_RI': c_ri, 'C_IF': c_if, 'C_total': c_total, 'weights': w_simplex}
        self.history.append(breakdown)
        return c_total, breakdown

    def compute_with_regime(self, state: LayerState, regime: Optional[Regime] = None) -> Tuple[float, Dict]:
        regime = regime or Regime()
        v6_regime = kernel_v6.Regime(
            theta=regime.theta,
            lam=regime.lambda_landauer,
            weights=regime.weights,
            criticality=regime.criticality
        )
        v6_state = kernel_v6.LayerState(
            normative=state.normative,
            representational=state.representational,
            informational=state.informational,
            verifiability=self._verifiability_proxy(state)
        )
        res = self._v6_kernel.gate(v6_state, v6_regime)
        # ADR-0007: honor v6 fail-closed results (no C_total on poisoned
        # input). Worst-case score 1.0, empty breakdown, verdict BLOCK.
        c_total = res.get("C_total", 1.0)
        breakdown = res.get("breakdown", {})

        # ADR-0007 - Layer Breach Breaker (LBB).
        # Convex dilution defense: with balanced weights no single layer can
        # push C_total above 1/3, so a single-layer breach (e.g. antipodal
        # normative violation camouflaged by perfect verifiability) would
        # otherwise pass theta=0.35. LBB caps inter-layer breaches directly:
        #   max(C_NR, C_RI) >= 0.75  => BLOCK (fail-closed)
        #   max(C_NR, C_RI) >= 0.60  => downgrade ALLOW to FLAG
        verdict = res["verdict"]
        lbb_trigger = None
        if isinstance(breakdown, dict):
            m_layer = max(breakdown.get('C_NR', 0.0), breakdown.get('C_RI', 0.0))
            if m_layer >= 0.75:
                verdict = "BLOCK"
                lbb_trigger = "LBB_BLOCK"
            elif m_layer >= 0.60 and verdict == "ALLOW":
                verdict = "FLAG"
                lbb_trigger = "LBB_FLAG"

        result = {
            'C_total': c_total,
            'passes_gate': verdict == "ALLOW",
            'verdict': verdict,
            'lbb_trigger': lbb_trigger,
            'regime': {'theta': v6_regime.theta, 'lambda': v6_regime.lam, 'mode': 'B', 'criticality': v6_regime.criticality},
            'breakdown': breakdown,
            'adjusted_landauer': res.get("adjusted_landauer", 0.0),
            'cca_influence': v6_regime.criticality
        }
        return c_total, result

    def measure_coherence_with_keys(self, normative, representational, informational, physical, keys=None):
        keys = keys or {}
        X = max(0.0, min(1.0, float(keys.get('X', 1.0))))
        Y = max(0.0, min(1.0, float(keys.get('Y', 1.0))))
        Z = max(0.0, min(1.0, float(keys.get('Z', 1.0))))
        K = float(keys.get('K', 0.05))

        state = LayerState(
            np.array(normative, dtype=float),
            np.array(representational, dtype=float),
            np.array(informational, dtype=float),
            np.array(physical, dtype=float)
        )
        c_total, breakdown = self.compute_coherence_total(state, {'w_NR': X, 'w_RI': Y, 'w_IF': Z})

        entropy_loss = (breakdown['C_NR'] + breakdown['C_RI'] + breakdown['C_IF']) / 3.0
        raw_quality = (1.0 - c_total) - (K * entropy_loss)
        coherence_score = max(0.0, min(1.0, raw_quality))

        landauer_cost = K * entropy_loss

        return {
            'c_nr': breakdown['C_NR'],
            'c_ri': breakdown['C_RI'],
            'c_if': breakdown['C_IF'],
            'c_total': c_total,
            'total_coherence': raw_quality,
            'coherence_score': coherence_score,
            'landauer_cost': landauer_cost,
            'entropy_loss': entropy_loss,
            'k_used': K,
            'weights': {'X': X, 'Y': Y, 'Z': Z, 'K': K},
            'status': 'OK'
        }

    def compute_landauer_cost(self, decision_changes: int, normalize: bool = True) -> float:
        if normalize:
            return self.lambda_landauer * decision_changes
        return decision_changes * LANDAUER_MIN

    def compute_loss_4R2(self, base_loss: float, coherence_total: float, decision_changes: int, alpha: float = 1.0, gamma: float = 1.0) -> float:
        c_sq = max(0.0, float(coherence_total)) ** 2
        coherence_penalty = alpha * c_sq
        irreversibility_penalty = gamma * self.compute_landauer_cost(decision_changes)
        total_loss = base_loss + coherence_penalty + irreversibility_penalty
        return total_loss

    def get_history_json(self) -> str:
        return json.dumps(self.history, indent=2)

    def reset_history(self):
        self.history = []

    @classmethod
    def selftest(cls) -> dict:
        kernel = cls()
        perfect = LayerState(np.ones(4), np.ones(4), np.ones(4), np.array([1.0, 1.0, 1.0, 1.0]))
        c, _ = kernel.compute_coherence_total(perfect)
        loss_p = kernel.compute_loss_4R2(0.5, c, 0)
        bad = LayerState(np.array([1.,0.,1.,0.]), np.array([0.,1.,0.,1.]), np.array([0.5]*4), np.array([0.0]*4))
        cb, _ = kernel.compute_coherence_total(bad)
        loss_b = kernel.compute_loss_4R2(0.5, cb, 2)
        return {
            "perfect_c": round(c, 4),
            "perfect_loss": round(loss_p, 4),
            "bad_c": round(cb, 4),
            "bad_loss": round(loss_b, 4),
            "loss_correct_direction": loss_b > loss_p
        }

def create_kernel(**kwargs) -> CoherenceKernel:
    return CoherenceKernel(**kwargs)

class CCA:
    def __init__(self, session_id: str = "default"):
        self.session_id = session_id
        self.history = []

    def observe(self, user_input: str, ai_output: str = "", authority_level: int = 1, project_link: str = None) -> dict:
        combined = (user_input + " " + ai_output).lower()
        action_verbs = ["ejecuta", "borra", "transfiere", "firma", "pago", "desplaza"]
        action_verb = any(v in combined for v in action_verbs)
        operational_risk = 0.8 if action_verb or "dinero" in combined or "ip" in combined else 0.3
        semantic_risk = min(1.0, len(combined.split()) / 80.0)
        intent_shift = 0.75 if project_link or "proyecto" in combined else 0.3
        tel = {
            "trace_id": "sim-" + str(len(self.history)),
            "session_id": self.session_id,
            "semantic_risk": round(semantic_risk, 3),
            "operational_risk": round(operational_risk, 3),
            "action_verb_detected": action_verb,
            "intent_shift_detected": intent_shift > 0.5,
            "authority_level": authority_level,
            "project_link": project_link,
            "intent_vector": [0.2, round(operational_risk, 2), round(semantic_risk, 2)],
            "criticality": round(max(operational_risk, semantic_risk), 3)
        }
        self.history.append(tel)
        return tel

    def to_regime(self, tel: dict) -> Regime:
        crit = tel.get("criticality", 0.0)
        irr = 1.0 if tel.get("action_verb_detected") else 0.0
        # ADR-0006 (angular scale): high criticality => stricter gate.
        theta = 0.25 if crit > 0.7 else 0.35
        lam = max(0.05, 0.25 - irr * 0.15)
        w = {'w_NR': 0.25, 'w_RI': 0.25, 'w_IF': 0.50}
        if crit > 0.6:
            w['w_IF'] = 0.60
            w['w_NR'] = 0.20
        return Regime(theta=theta, lambda_landauer=lam, weights=w, criticality=crit, mode="B")

def promotion_protocol(idea: str, kernel: CoherenceKernel, cca: CCA) -> dict:
    tel = cca.observe(idea)
    regime = cca.to_regime(tel)
    st = LayerState(
        normative=np.array([0.9, 0.8, 0.7, 0.6]),
        representational=np.array([0.85, 0.75, 0.65, 0.55]),
        informational=np.array([0.8, 0.7, 0.6, 0.5]),
        physical=np.array([1.0, 1.0, 1.0, 1.0])
    )
    c_total, res = kernel.compute_with_regime(st, regime)
    promoted = res['passes_gate']
    return {
        "idea": idea,
        "promoted_to_canon": promoted,
        "c_total": round(c_total, 4),
        "regime": res['regime'],
        "note": "Promoted only if passes the regime gate (v5.2 dualism)"
    }

@dataclass
class Fact:
    content: str
    probability: float
    timestamp: float
    tag: str
    source: str = "unknown"

class BeliefTracker:
    """Log-odds (logarithmic) opinion pooling with Ebbinghaus decay on episodic facts.

    v6 fix (F7): existing facts are now updated via log-odds pooling, not
    exponential smoothing. Log-odds pooling is the formally correct,
    defensible version of the original intuition.
    """
    def __init__(
        self,
        decay_tau_episodic: float = 20.0,
        decay_tau_semantic: float = float('inf'),
        threshold: float = 0.1,
    ):
        self._facts: list[Fact] = []
        self._decay_episodic = decay_tau_episodic
        self._decay_semantic = decay_tau_semantic
        self._threshold = threshold

    def update(self, facts: list[tuple[str, float, str, str]]) -> None:
        for content, prob, tag, source in facts:
            prob = max(0.0, min(1.0, prob))
            existing = self._find_fact(content)

            if existing is not None:
                kappa = 0.7 if source == "trusted" else 0.4
                eps = 1e-9
                p_old = min(max(existing.probability, eps), 1 - eps)
                p_obs = min(max(prob, eps), 1 - eps)
                logit_old = math.log(p_old / (1 - p_old))
                logit_obs = math.log(p_obs / (1 - p_obs))
                logit_new = logit_old + kappa * logit_obs
                existing.probability = 1.0 / (1.0 + math.exp(-logit_new))
                existing.timestamp = time.time()
            else:
                self._facts.append(Fact(
                    content=content,
                    probability=prob,
                    timestamp=time.time(),
                    tag=tag,
                    source=source,
                ))

    def _find_fact(self, content: str) -> Fact | None:
        for f in self._facts:
            if f.content.lower() == content.lower():
                return f
        return None

    def query(self, fact: str) -> tuple[float, str, float]:
        found = self._find_fact(fact)
        if found is None:
            return 0.0, "unknown", 0.0

        decayed_prob = self._apply_decay(found)
        return decayed_prob, found.tag, found.timestamp

    def _apply_decay(self, fact: Fact) -> float:
        if fact.tag == "semantic":
            return fact.probability

        elapsed = (time.time() - fact.timestamp) / 60.0
        decay = math.exp(-elapsed / self._decay_episodic)
        return fact.probability * decay

    def get_contradiction_cost(self, facts: list[str]) -> float:
        costs = []
        for i, f1 in enumerate(facts):
            for f2 in facts[i+1:]:
                p1, _, _ = self.query(f1)
                p2, _, _ = self.query(f2)

                if p1 < self._threshold or p2 < self._threshold:
                    continue

                if (p1 > 0.5 and p2 < 0.5) or (p2 > 0.5 and p1 < 0.5):
                    cost = 0.5 * abs(p1 - p2)
                    costs.append(cost)

        return sum(costs) if costs else 0.0

    def get_all_facts(self) -> list[dict]:
        return [
            {
                "content": f.content,
                "probability": round(self._apply_decay(f), 4),
                "tag": f.tag,
                "timestamp": f.timestamp,
                "source": f.source,
            }
            for f in self._facts
        ]

    def clear(self) -> None:
        self._facts.clear()

class CalibratedEvaluator:
    DEFAULT_TEMPERATURES = {
        "c1": 1.0, "c2": 1.0, "c3": 1.1, "c4": 1.2,
        "c5": 1.0, "c6": 1.0, "c7": 1.1,
    }

    SEVERITY_LEVELS = {
        "hard": 1.0, "soft": 0.6, "temporal": 0.3,
        "modal": 0.5, "pragmatic": 0.2,
    }

    def __init__(self, temperatures: dict[str, float] | None = None):
        self._temperatures = temperatures or self.DEFAULT_TEMPERATURES.copy()

    def calibrate(self, c_id: str, raw_score: float, center: float = 0.5) -> float:
        T = self._temperatures.get(c_id, 1.0)
        calibrated = 1 / (1 + math.exp(-(raw_score - center) / T))
        return max(0.0, min(1.0, calibrated))

    def get_severity(self, fact: str) -> float:
        fact_lower = fact.lower()

        if any(kw in fact_lower for kw in ["error", "wrong", "false", "illegal", "harmful"]):
            return self.SEVERITY_LEVELS["hard"]
        elif any(kw in fact_lower for kw in ["prefer", "should", "better"]):
            return self.SEVERITY_LEVELS["soft"]
        elif any(kw in fact_lower for kw in ["before", "after", "first", "then", "order"]):
            return self.SEVERITY_LEVELS["temporal"]
        elif any(kw in fact_lower for kw in ["must", "can", "may", "obligation"]):
            return self.SEVERITY_LEVELS["modal"]
        return self.SEVERITY_LEVELS["pragmatic"]

class DomainKernel:
    def __init__(self, domain_weights=None):
        self._weights = domain_weights or {
            "default": {'w_NR': 0.25, 'w_RI': 0.25, 'w_IF': 0.50},
            "medical": {'w_NR': 0.20, 'w_RI': 0.20, 'w_IF': 0.60},
            "legal": {'w_NR': 0.30, 'w_RI': 0.30, 'w_IF': 0.40},
            "technical": {'w_NR': 0.15, 'w_RI': 0.15, 'w_IF': 0.70},
            "creative": {'w_NR': 0.40, 'w_RI': 0.40, 'w_IF': 0.20},
        }

    def get_weights(self, domain="default"):
        return self._weights.get(domain, self._weights["default"])

    def detect_domain(self, text):
        text_lower = text.lower()
        if any(kw in text_lower for kw in ["patient", "diagnosis", "treatment", "symptom"]):
            return "medical"
        elif any(kw in text_lower for kw in ["law", "court", "contract", "liability"]):
            return "legal"
        elif any(kw in text_lower for kw in ["code", "function", "debug", "api"]):
            return "technical"
        elif any(kw in text_lower for kw in ["create", "story", "imagine", "creative"]):
            return "creative"
        return "default"
