"""
4R2 Coherence Kernel - Canonical Implementation of Algorithm 1240421

Location: core/kernel_1240421.py (Single Source of Truth)

This is the official canonical version for this workspace.

Locked Design Decisions (v5.2 - reinforced from backup42final analysis):
- C_total uses weighted SUM (lower = better).
- Loss_4R2 uses C_total squared.
- C_IF uses cosine distance (consistent with C_NR/C_RI) after zero-pad + re-norm.
- Added v5.2: Regime (RCC with theta, lambda, dynamic weights F-priority), CCA class for telemetry,
  compute_with_regime for dynamic convivencia, promotion_protocol for Obsidian<->SurfSense dualism.

See docs/CANON_SPEC.md , FINAL_AUDIT_AND_ROADMAP.md , cierrecanonicoal26dejunio.md
and agenticgrokhistorial.md for full backup analysis and rationale.
"""

import numpy as np
import math
import time
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
import logging
import json
from datetime import datetime

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
    """Régimen de Coherencia Contextual (RCC) v5.2 - from backup42final.
    Supports dynamic theta, lambda, F-priority weights, mode (A/B), criticality from CCA.
    """
    theta: float = 0.75
    lambda_landauer: float = 0.25
    weights: dict = None
    mode: str = "B"  # A=static, B=convivencia
    criticality: float = 0.0
    intent_level: str = "EXPLORATORY"  # from PSC

    def __post_init__(self):
        if self.weights is None:
            self.weights = {'w_NR': 0.25, 'w_RI': 0.25, 'w_IF': 0.50}  # F priority
        self.theta = max(0.0, min(1.0, self.theta))
        self.lambda_landauer = max(0.01, min(1.0, self.lambda_landauer))
        if self.intent_level == "CRITICAL":
            self.theta = min(0.98, self.theta + 0.1)


class CoherenceKernel:
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
        self.belief_tracker = BeliefTracker()
        self.calibrator = CalibratedEvaluator()
        self.domain_kernel = DomainKernel()

    def _safe_norm(self, vec: np.ndarray, epsilon: float = 1e-8) -> np.ndarray:
        norm = np.linalg.norm(vec)
        return vec / (norm + epsilon)

    def compute_C_NR(self, normative: np.ndarray, representational: np.ndarray) -> float:
        n = self._safe_norm(normative)
        r = self._safe_norm(representational)
        return float(1.0 - np.dot(n, r))

    def compute_C_RI(self, representational: np.ndarray, informational: np.ndarray) -> float:
        r = self._safe_norm(representational)
        i = self._safe_norm(informational)
        return float(1.0 - np.dot(r, i))

    def compute_C_IF(self, informational: np.ndarray, physical: np.ndarray) -> float:
        """C_IF (Informational-Physical coherence).
        Uses same cosine distance as C_NR / C_RI for layer consistency.
        Zero-pads the shorter vector then re-normalizes (handles variable dims
        from translator, e.g. info~3 vs physical=4).
        Lower value = better alignment between layers.
        """
        i = self._safe_norm(informational)
        p = self._safe_norm(physical)
        # Align dimensions
        size = max(len(i), len(p))
        ia = np.zeros(size); ia[:len(i)] = i
        pa = np.zeros(size); pa[:len(p)] = p
        # Re-normalize after padding for fair dot product
        ia = self._safe_norm(ia)
        pa = self._safe_norm(pa)
        return float(1.0 - np.dot(ia, pa))

    def compute_coherence_total(self, state: LayerState, weights: Optional[Dict[str, float]] = None) -> Tuple[float, Dict]:
        state.validate()
        w = weights or self.weights
        c_nr = self.compute_C_NR(state.normative, state.representational)
        c_ri = self.compute_C_RI(state.representational, state.informational)
        c_if = self.compute_C_IF(state.informational, state.physical)
        c_total = w['w_NR'] * c_nr + w['w_RI'] * c_ri + w['w_IF'] * c_if
        breakdown = {'C_NR': c_nr, 'C_RI': c_ri, 'C_IF': c_if, 'C_total': c_total, 'weights': w.copy()}
        self.history.append(breakdown)
        return c_total, breakdown

    def compute_with_regime(self, state: LayerState, regime: Optional['Regime'] = None) -> Tuple[float, Dict]:
        """v5.2: Compute with dynamic RCC from CCA (reforzado desde backup).
        Applies dynamic weights, theta gate, adjusted lambda.
        """
        regime = regime or Regime()
        w = regime.weights or self.weights
        if regime.criticality > 0.5:
            w = w.copy()
            w['w_IF'] = min(0.65, w.get('w_IF', 0.5) + 0.15)
            w['w_NR'] = max(0.15, w.get('w_NR', 0.25) - 0.05)
            w['w_RI'] = max(0.15, w.get('w_RI', 0.25) - 0.05)
        c_total, breakdown = self.compute_coherence_total(state, weights=w)
        passes_gate = c_total <= regime.theta
        eff_lambda = regime.lambda_landauer
        if regime.mode == "B" and regime.criticality > 0.7:
            eff_lambda *= 0.7
        landauer = self.compute_landauer_cost(1, normalize=True) * eff_lambda
        result = {
            'C_total': c_total,
            'passes_gate': passes_gate,
            'regime': {'theta': regime.theta, 'lambda': eff_lambda, 'mode': regime.mode, 'criticality': regime.criticality},
            'breakdown': breakdown,
            'adjusted_landauer': landauer,
            'cca_influence': regime.criticality
        }
        return c_total, result

    def measure_coherence_with_keys(self, normative, representational, informational, physical, keys=None):
        """
        Compatibilidad con variante auditada (LLMsuper v5.3.1 style).
        Retorna tanto total_coherence (raw) como coherence_score (clamped [0,1]).
        Útil para Loss y uso operacional (fail-closed).
        """
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
        raw_quality = (1.0 - c_total) - (K * entropy_loss)   # raw puede ser negativo
        coherence_score = max(0.0, min(1.0, raw_quality))    # clamped operacional

        # Landauer similar al auditado
        bits = len(normative) + len(representational) + len(informational)
        kT = 4.11e-21
        ln2 = 0.693147
        landauer_cost = bits * kT * ln2 * (1 + entropy_loss)

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
        # Hardening: Prevenir errores de punto flotante extremos antes de la potenciación.
        # Si C_total es -0.0000000001 por error de precisión, max() evita valores negativos.
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
        # Perfect
        perfect = LayerState(np.ones(4), np.ones(4), np.ones(4), np.array([1000.,8.,50.,10.]))
        c, _ = kernel.compute_coherence_total(perfect)
        loss_p = kernel.compute_loss_4R2(0.5, c, 0)
        # Bad
        bad = LayerState(np.array([1.,0.,1.,0.]), np.array([0.,1.,0.,1.]), np.array([0.5]*4), np.array([1000.,8.,50.,10.]))
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
    """Context Coexistence Agent v5.2 (from backup CCA_Design + Streaming_Pulse).
    Passive observer. Produces telemetry for dynamic RCC.
    """
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

    def to_regime(self, tel: dict) -> 'Regime':
        crit = tel.get("criticality", 0.0)
        irr = 1.0 if tel.get("action_verb_detected") else 0.0
        theta = 0.95 if crit > 0.7 else 0.75
        lam = max(0.05, 0.25 - irr * 0.15)
        w = {'w_NR': 0.25, 'w_RI': 0.25, 'w_IF': 0.50}
        if crit > 0.6:
            w['w_IF'] = 0.60
            w['w_NR'] = 0.20
        return Regime(theta=theta, lambda_landauer=lam, weights=w, criticality=crit, mode="B")


def promotion_protocol(idea: str, kernel: CoherenceKernel, cca: CCA) -> dict:
    """Obsidian (free thinking) -> audit with CCA+Kernel -> promote to SurfSense (canon) only if passes gate.
    From backup dualism analysis.
    """
    tel = cca.observe(idea)
    regime = cca.to_regime(tel)
    # Simple aligned state for demo; real would come from embeddings
    st = LayerState(
        normative=np.array([0.9, 0.8, 0.7, 0.6]),
        representational=np.array([0.85, 0.75, 0.65, 0.55]),
        informational=np.array([0.8, 0.7, 0.6, 0.5]),
        physical=np.array([1000., 8., 50., 10.])
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
    """Hecho para Belief Tracker (MVBS v2.0)."""
    content: str
    probability: float
    timestamp: float
    tag: str  # "episodic" | "semantic"
    source: str = "unknown"


class BeliefTracker:
    """Tracker de hechos con decay Ebbinghaus y actualización bayesiana."""
    
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
        """Actualiza hechos con formato (content, probability, tag, source)."""
        for content, prob, tag, source in facts:
            prob = max(0.0, min(1.0, prob))
            existing = self._find_fact(content)
            
            if existing is not None:
                confidence = 0.7 if source == "trusted" else 0.4
                existing.probability = confidence * prob + (1 - confidence) * existing.probability
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
        """Consulta probabilidad de un hecho."""
        found = self._find_fact(fact)
        if found is None:
            return 0.0, "unknown", 0.0
        
        decayed_prob = self._apply_decay(found)
        return decayed_prob, found.tag, found.timestamp
    
    def _apply_decay(self, fact: Fact) -> float:
        """Decay exponencial Ebbinghaus."""
        if fact.tag == "semantic":
            return fact.probability
        
        elapsed = (time.time() - fact.timestamp) / 60.0
        decay = math.exp(-elapsed / self._decay_episodic)
        return fact.probability * decay
    
    def get_contradiction_cost(self, facts: list[str]) -> float:
        """Costo de contradicción entre hechos."""
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
        """Retorna todos los hechos como dicts."""
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
    """Evaluador con calibración probabilística para chequeos."""
    
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
    
    def calibrate(self, c_id: str, raw_score: float) -> float:
        """Temperature scaling + sigmoid."""
        T = self._temperatures.get(c_id, 1.0)
        calibrated = 1 / (1 + math.exp(-raw_score / T))
        return max(0.0, min(1.0, calibrated))
    
    def get_severity(self, fact: str) -> float:
        """Severidad basada en keywords."""
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
    """Kernel adaptado por dominio (pesos para C_IF por domain)."""
    
    DEFAULT_PHYSICAL_WEIGHTS = {
        "default": {'w_NR': 0.25, 'w_RI': 0.25, 'w_IF': 0.50},
        "medical": {'w_NR': 0.20, 'w_RI': 0.20, 'w_IF': 0.60},
        "legal": {'w_NR': 0.30, 'w_RI': 0.30, 'w_IF': 0.40},
        "technical": {'w_NR': 0.15, 'w_RI': 0.15, 'w_IF': 0.70},
        "creative": {'w_NR': 0.40, 'w_RI': 0.40, 'w_IF': 0.20},
    }
    
    def __init__(self, domain_weights: dict[str, dict] | None = None):
        self._weights = domain_weights or self.DEFAULT_PHYSICAL_WEIGHTS.copy()
    
    def get_weights(self, domain: str = "default") -> dict[str, float]:
        return self._weights.get(domain, self._weights["default"])
    
    def detect_domain(self, text: str) -> str:
        """Detecta dominio desde texto."""
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

