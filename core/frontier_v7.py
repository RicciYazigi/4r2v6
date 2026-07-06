"""
4R2 Frontier v7.0 - Layer-decoupling defenses (opt-in, non-breaking)
====================================================================

Adds the v7.0 "Frontier" defenses on top of the FROZEN v6.1.0 kernel
(core/kernel_v6.py, core/kernel_1240421.py). Imports the frozen math and
NEVER mutates it. The v6.1.0 public API is unchanged; everything here is
additive and opt-in.

Honesty contract (project rule: rigor real por encima de rigor aparente):
  * Two guarantee categories, never mixed:
      - MATH (provable): proved in a few lines in test_frontier_v7.
      - EMPIRICAL (measured): reported only from a real seeded run; never
        generalized to universal completeness.
  * Nothing here is physics. H(x) is a *score* (a calibrated penalty
    functional), not a Hamiltonian. Shannon entropy over the layer vector is
    information theory over a finite index, NOT Von Neumann entropy.

1. H(x) - layer-breach energy score (derived replacement for heuristic LBB)
   H(x) = a*C_NR + b*C_RI + g*(1 - C_IF),  a,b,g >= 0, on the simplex => [0,1].
   MATH: convex on the simplex => bounded [0,1]; monotone non-decreasing in
   C_NR, C_RI and in (1 - C_IF). A single-layer breach raises H even when
   convex dilution keeps C_total below theta - the camouflage hole H closes.

2. Camouflage signal - JS(observed || benign reference) over a layer score.
   MATH: JS bounded [0, ln2], symmetric, finite. Reuses frozen
   kernel_v6.js_divergence (no new metric invented).

3. OOD signal - Shannon entropy over the normalized breach vector, range
   [0, ln 3]. Low entropy = breach concentrated in one layer (single-layer
   camouflage signature). Threshold set by benign percentiles, not by hand.

4. Fisher vs angular: a true Fisher-Information metric is the natural distance
   ONLY when the compared objects are parameters of a distribution family.
   Generic dense embeddings are not; fabricating a family would be aesthetic,
   not real, rigor. Decision: KEEP angular (a proven true metric). The script
   scripts/frontier_calibrate.py runs a diagonal-Fisher control on the real E2
   corpus and reports whether it moves FPR/FNR - evidence, not assertion.
"""
from __future__ import annotations
import json
import math
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional, Sequence

import numpy as np

import kernel_v6  # frozen bounded JS divergence lives here

EPS = 1e-12


# 1. H(x) - layer-breach energy score
@dataclass(frozen=True)
class HParams:
    a: float = 1.0 / 3.0
    b: float = 1.0 / 3.0
    g: float = 1.0 / 3.0
    threshold: float = 1.01   # >1 => uncalibrated default never escalates on H
    source: str = "default (uncalibrated simplex prior; H escalation disabled)"

    def simplex(self) -> "HParams":
        s = max(EPS, self.a + self.b + self.g)
        return HParams(self.a / s, self.b / s, self.g / s, self.threshold, self.source)


def h_energy(c_nr: float, c_ri: float, c_if: float, p: Optional[HParams] = None) -> float:
    p = (p or HParams()).simplex()
    c_nr = float(np.clip(c_nr, 0.0, 1.0))
    c_ri = float(np.clip(c_ri, 0.0, 1.0))
    c_if = float(np.clip(c_if, 0.0, 1.0))
    return p.a * c_nr + p.b * c_ri + p.g * (1.0 - c_if)


def fisher_linear_discriminant(benign, adversarial, shrinkage=1e-3):
    """Fisher LDA direction on rows [C_NR, C_RI, 1-C_IF]. Returns (w, thr)."""
    benign = np.atleast_2d(benign).astype(float)
    adversarial = np.atleast_2d(adversarial).astype(float)
    mu_b, mu_a = benign.mean(0), adversarial.mean(0)
    d = benign.shape[1]
    sw = np.cov(benign.T) + np.cov(adversarial.T) + shrinkage * np.eye(d)
    w = np.linalg.solve(sw, (mu_a - mu_b))
    w = w / (np.linalg.norm(w) + EPS)
    thr = float(0.5 * (benign @ w).mean() + 0.5 * (adversarial @ w).mean())
    return w, thr


def calibrate_h_from_rows(rows, shrinkage=1e-3, positive_label="off-topic-grave"):
    """Calibrate H(x) weights + threshold on real rows (benign vs positive_label).

    H(x) is a function of LAYER MAGNITUDES only: the derived generalization of
    the heuristic LBB. It is calibrated against benign vs off-topic-grave, where
    layers genuinely separate. It is DELIBERATELY not calibrated against
    adversarial, because camouflaged adversarial (F=[1,1,1,1]) makes the layer
    magnitudes look benign - no threshold on H alone can catch it. That defense
    is the negation-aware verifiability cue (VER fuse). See frontier_calibrate.py
    for the measured AUROC proving this separation is impossible on H alone.
    """
    benign, pos = [], []
    for r in rows:
        f = [r["C_NR"], r["C_RI"], 1.0 - r["C_IF"]]
        if r["label"] in ("on-topic", "off-topic-leve"):
            benign.append(f)
        elif r["label"] == positive_label:
            pos.append(f)
    benign, pos = np.array(benign), np.array(pos)
    if len(benign) < 2 or len(pos) < 2:
        return HParams(source="default (insufficient data to calibrate)")
    w, _ = fisher_linear_discriminant(benign, pos, shrinkage)
    w_pos = np.clip(w, 0.0, None)
    if w_pos.sum() < EPS:
        return HParams(source="default (degenerate Fisher direction)")
    w_pos = w_pos / w_pos.sum()
    a, b, g = (float(x) for x in w_pos)
    hp = HParams(a, b, g, 0.0, "").simplex()
    hb, ha = [], []
    for r in rows:
        h = h_energy(r["C_NR"], r["C_RI"], r["C_IF"], hp)
        if r["label"] in ("on-topic", "off-topic-leve"):
            hb.append(h)
        elif r["label"] == positive_label:
            ha.append(h)
    hb, ha = np.array(hb), np.array(ha)
    grid = np.linspace(0.0, 1.0, 1001)
    j = [(ha >= t).mean() + (hb < t).mean() - 1.0 for t in grid]
    thr = float(grid[int(np.argmax(j))])
    src = "Fisher-LDA benign-vs-" + positive_label + " n=" + str(len(benign) + len(pos))
    return HParams(a, b, g, thr, src)


# 2. Camouflage signal - JS divergence vs benign reference histogram
@dataclass(frozen=True)
class BenignReference:
    edges: list
    hist_c_nr: list
    hist_c_ri: list
    hist_c_if: list
    n: int
    source: str = ""

    def as_dict(self):
        return asdict(self)


def build_benign_reference(rows, bins=16):
    edges = np.linspace(0.0, 1.0, bins + 1)
    benign = [r for r in rows if r["label"] in ("on-topic", "off-topic-leve")]

    def hist(key, transform):
        vals = [transform(r[key]) for r in benign]
        h, _ = np.histogram(vals, bins=edges)
        return (h + 1.0).tolist()

    ident = lambda v: v
    inv = lambda v: 1.0 - v
    return BenignReference(edges.tolist(), hist("C_NR", ident), hist("C_RI", ident),
                           hist("C_IF", inv), len(benign),
                           "benign reference n=" + str(len(benign)))


def camouflage_js(observed_scores, reference_hist, edges):
    """JS(observed || benign reference) over one layer score. Bounded [0, ln2]."""
    obs, _ = np.histogram(np.asarray(observed_scores, dtype=float),
                          bins=np.asarray(edges, dtype=float))
    obs = obs + 1.0
    return kernel_v6.js_divergence(np.asarray(obs, dtype=float),
                                   np.asarray(reference_hist, dtype=float))


# 3. OOD signal - Shannon entropy over the layer vector
def layer_entropy(c_nr, c_ri, c_if):
    """Shannon entropy of normalized (C_NR, C_RI, 1-C_IF). Range [0, ln 3]."""
    v = np.array([max(0.0, c_nr), max(0.0, c_ri), max(0.0, 1.0 - c_if)], dtype=float)
    s = v.sum()
    if s < EPS:
        return math.log(3.0)
    p = np.clip(v / s, EPS, 1.0)
    return float(-np.sum(p * np.log(p)))


@dataclass(frozen=True)
class OODBand:
    lo: float
    hi: float
    source: str = ""

    def is_ood(self, entropy):
        return entropy < self.lo or entropy > self.hi


def calibrate_ood_band(rows, lo_pct=5.0, hi_pct=95.0):
    ent = []
    for r in rows:
        if r["label"] in ("on-topic", "off-topic-leve"):
            ent.append(layer_entropy(r["C_NR"], r["C_RI"], r["C_IF"]))
    ent = np.array(ent)
    if len(ent) < 2:
        return OODBand(0.0, math.log(3.0), "default (insufficient data)")
    src = "percentiles p" + str(int(lo_pct)) + "/p" + str(int(hi_pct)) + " on benign n=" + str(len(ent))
    return OODBand(float(np.percentile(ent, lo_pct)), float(np.percentile(ent, hi_pct)), src)


# 4. Frontier verdict - composes v6.1.0 gate + H(x) + OOD (opt-in wrapper)
@dataclass(frozen=True)
class FrontierConfig:
    h: HParams
    ood: OODBand
    lbb_block: float = 0.75   # frozen v6.1.0 safety floor
    lbb_flag: float = 0.60
    source: str = ""

    @staticmethod
    def default():
        return FrontierConfig(HParams(), OODBand(0.0, math.log(3.0)),
                              source="uncalibrated default")

    def as_dict(self):
        return {"h": asdict(self.h), "ood": asdict(self.ood),
                "lbb_block": self.lbb_block, "lbb_flag": self.lbb_flag,
                "source": self.source}

    @staticmethod
    def load(path):
        d = json.loads(Path(path).read_text())
        return FrontierConfig(HParams(**d["h"]), OODBand(**d["ood"]),
                              d.get("lbb_block", 0.75), d.get("lbb_flag", 0.60),
                              d.get("source", "loaded"))


def frontier_verdict(breakdown, base_verdict, cfg=None):
    """Combine v6.1.0 gate verdict with v7 signals. Escalation-only (fail-closed):
    v7 can DOWNGRADE (ALLOW->FLAG->BLOCK) but NEVER upgrade a v6 verdict."""
    cfg = cfg or FrontierConfig.default()
    c_nr = float(breakdown.get("C_NR", 1.0))
    c_ri = float(breakdown.get("C_RI", 1.0))
    c_if = float(breakdown.get("C_IF", 1.0))
    H = h_energy(c_nr, c_ri, c_if, cfg.h)
    ent = layer_entropy(c_nr, c_ri, c_if)
    ood = cfg.ood.is_ood(ent)
    m_layer = max(c_nr, c_ri)
    order = {"ALLOW": 0, "FLAG": 1, "BLOCK": 2}
    rank = order.get(base_verdict, 2)
    reasons = []
    if m_layer >= cfg.lbb_block:
        rank = max(rank, 2); reasons.append("LBB_BLOCK")
    elif m_layer >= cfg.lbb_flag:
        rank = max(rank, 1); reasons.append("LBB_FLAG")
    # H(x): single Youden-optimal boundary (calibrated on benign-vs-grave).
    # H is a function of layer magnitudes only, so it escalates to FLAG (review),
    # never hard-BLOCK on its own - the v6 gate + LBB own the BLOCK decision.
    if H >= cfg.h.threshold:
        rank = max(rank, 1); reasons.append("H_FLAG")
    # OOD low-entropy escalation only when it COINCIDES with a real layer breach
    # (single-layer camouflage signature: one layer breached => low entropy).
    # Benign traffic has low max_layer, so this does not raise benign FPR.
    if ood and ent < cfg.ood.lo and m_layer >= 0.5:
        rank = max(rank, 1); reasons.append("OOD_FLAG_single_layer_concentration")
    verdict = ["ALLOW", "FLAG", "BLOCK"][rank]
    return {"verdict": verdict, "base_verdict": base_verdict,
            "H": round(H, 6), "layer_entropy": round(ent, 6),
            "ood": ood, "max_layer": round(m_layer, 6), "escalations": reasons}


import re

# --------------------------------------------------------------------------
# 5. Hardened verifiability-negation detector (P1 fix: paraphrase-robust)
# --------------------------------------------------------------------------
# v6.1.0 used a narrow regex (without|skipping|bypass) that a paraphrasing
# attacker evades ("omitting the sign-off", "in place of two-factor",
# "prior to any verification"). This detector widens the bypass-verb and
# control-noun vocabularies and adds "no/lacking X" and "X was not performed"
# forms. It is a lexical cue (declared limitation: not semantic), but a much
# larger evasion surface. EMPIRICAL coverage is measured in
# scripts/eval_negation_hardening.py (old vs new evasion rate), not asserted.
_BYPASS = (r"without|skipp\w*|bypass\w*|omitt?\w*|forgo\w*|foregoing|"
           r"waiv\w*|circumvent\w*|ignor\w*|disregard\w*|neglect\w*|"
           r"in\s+place\s+of|instead\s+of|in\s+lieu\s+of|rather\s+than|"
           r"prior\s+to|ahead\s+of|absent|lacking|no\s+need\s+for|"
           r"did\s+not\s+\w+|didn't\s+\w+|not\s+perform\w*|not\s+requir\w*|"
           r"un-?verified|un-?approved|un-?checked")
_CONTROL = (r"verification|verify\w*|two-?factor|2fa|sign-?off|signoff|"
            r"screening|screen\w*|complianc\w*|hold|approv\w*|authoriz\w*|"
            r"rollback|roll-?back|test\w*|ci|change-?board|physician|"
            r"attending|identity|fraud|document\w*|audit\w*|review\w*|checks?")
_NEG_HARD = re.compile(
    r"(?:" + _BYPASS + r")[^.]{0,70}?(?:" + _CONTROL + r")"
    r"|(?:" + _CONTROL + r")[^.]{0,40}?(?:was|were|is|are)?\s*"
    r"(?:not|never)\s+(?:perform\w*|obtain\w*|done|complet\w*|requir\w*|appl\w*)"
    r"|failing\s+tests|no\s+rollback|skipp\w*\s+the",
    re.IGNORECASE)


def verifiability_negation(text: str) -> bool:
    """Return True if the text asserts a control-bypass (hardened, lexical)."""
    return bool(_NEG_HARD.search(text or ""))


def selftest():
    checks = {}
    hs = [h_energy(a, b, c) for a in (0, .5, 1) for b in (0, .5, 1) for c in (0, .5, 1)]
    checks["H_bounded_0_1"] = all(-1e-9 <= h <= 1 + 1e-9 for h in hs)
    checks["H_monotone_C_NR"] = h_energy(0.9, 0.2, 0.5) > h_energy(0.1, 0.2, 0.5)
    checks["H_rises_low_verifiability"] = h_energy(0.2, 0.2, 0.1) > h_energy(0.2, 0.2, 0.9)
    e_single = layer_entropy(0.9, 0.0, 1.0)
    e_diffuse = layer_entropy(0.5, 0.5, 0.5)
    checks["entropy_bounded"] = 0 <= e_single <= math.log(3) + 1e-9
    checks["single_layer_low_entropy"] = e_single < e_diffuse
    js = camouflage_js([0.9] * 20, [1.0] * 8, np.linspace(0, 1, 9).tolist())
    checks["camouflage_js_bounded"] = 0 <= js <= math.log(2) + 1e-9
    fv = frontier_verdict({"C_NR": 0.0, "C_RI": 0.0, "C_IF": 1.0}, "BLOCK")
    checks["frontier_never_upgrades"] = fv["verdict"] == "BLOCK"
    checks["neg_detects_paraphrase"] = (verifiability_negation("I approved it omitting the required sign-off") and not verifiability_negation("I approved it after full verification and sign-off"))
    checks["ALL_PASS"] = all(checks.values())
    return checks


if __name__ == "__main__":
    print(json.dumps(selftest(), indent=2))
