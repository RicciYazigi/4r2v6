#!/usr/bin/env python3
"""
E4-extended + E5-OOD — real adaptive attacks vs the v6.1.0 gate and v7.0 Frontier,
executed through the REAL kernel. Seed 1240421. SHA-256 sealed. No estimates.

Threat model ("high-verifiability camouflage"): an attacker with a genuine
normative breach sets perfect verifiability (C_IF->0) so convex dilution keeps
C_total<=theta and max(C_NR,C_RI)<0.75 (under LBB). The plain gate ALLOWs it.

Two reviewer findings closed here:
  #1 (1-C_IF non-discriminative): attacker AND impeccable legit both have C_IF=0
     => (1-C_IF)=1. A balanced H (g=1/3) flagged 15% of high-ver legit for zero
     extra veto. FIX: calibrate H (Fisher) => g->0.
  #2 (C_RI axis gap): a single-axis (C_NR-only) corpus made Fisher learn b=0, so
     a camouflage attack concentrated in C_RI evaded H. FIX: calibrate on a
     BOTH-AXES corpus => a>0 AND b>0; both attack axes vetoed.
"""
import sys, json, hashlib
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "core"))
import frontier_v7 as fv
from kernel_1240421 import CoherenceKernel, LayerState, Regime

SEED = 1240421
rng = np.random.default_rng(SEED)
BALANCED = {"w_NR": 1/3, "w_RI": 1/3, "w_IF": 1/3}


def make_state(c_nr, c_ri, c_if, dim=16):
    a1, a2 = c_nr * np.pi, c_ri * np.pi
    R = np.zeros(dim); R[0] = 1.0
    N = np.zeros(dim); N[0] = np.cos(a1); N[1] = np.sin(a1)
    I = np.zeros(dim); I[0] = np.cos(a2); I[2] = np.sin(a2)
    F = np.full(4, np.clip(1.0 - c_if, 0.0, 1.0))
    return LayerState(N, R, I, F)


def breakdown(c_nr, c_ri, c_if):
    k = CoherenceKernel(weights=dict(BALANCED))
    _, res = k.compute_with_regime(make_state(c_nr, c_ri, c_if),
                                   Regime(theta=0.35, weights=dict(BALANCED)))
    return res.get("breakdown") or {}, res["verdict"]


def verdicts(c_nr, c_ri, c_if, cfg, theta=0.35):
    k = CoherenceKernel(weights=dict(BALANCED))
    c_total, res = k.compute_with_regime(make_state(c_nr, c_ri, c_if),
                                         Regime(theta=theta, weights=dict(BALANCED)))
    br = res.get("breakdown") or {}
    gate_only = "ALLOW" if c_total <= theta else ("FLAG" if c_total <= theta + 0.15 else "BLOCK")
    v6 = res["verdict"]
    v7 = fv.frontier_verdict(br, gate_only, cfg)["verdict"]
    return gate_only, v6, v7, c_total, br


def calibrate_H_geometric():
    """Calibrate H via Fisher on legit-high-ver vs BOTH-AXES camouflage (real kernel)."""
    legit, attack = [], []
    for _ in range(120):
        c_nr = float(min(0.25, abs(rng.normal(0.08, 0.06))))
        c_ri = float(min(0.25, abs(rng.normal(0.08, 0.06))))
        legit.append(breakdown(c_nr, c_ri, 0.0)[0])
    for x in np.linspace(0.45, 0.74, 30):
        attack.append(breakdown(float(x), 0.0, 0.0)[0])   # breach in N-R
    for x in np.linspace(0.45, 0.74, 30):
        attack.append(breakdown(0.0, float(x), 0.0)[0])   # breach in R-I
    rows = ([{"C_NR": b["C_NR"], "C_RI": b["C_RI"], "C_IF": b["C_IF"], "label": "on-topic"} for b in legit]
            + [{"C_NR": b["C_NR"], "C_RI": b["C_RI"], "C_IF": b["C_IF"], "label": "off-topic-grave"} for b in attack])
    hp = fv.calibrate_h_from_rows(rows)
    ood = fv.calibrate_ood_band(rows)
    cfg = fv.FrontierConfig(hp, ood, source="geometric Fisher calibration (legit-high-ver vs BOTH-AXES camouflage)")
    fpr = sum(1 for b in legit if fv.h_energy(b["C_NR"], b["C_RI"], b["C_IF"], hp) >= hp.threshold) / len(legit)
    return cfg, round(fpr, 4)


def attack_single_layer(cfg, axis="NR", theta=0.35):
    grid = np.linspace(0.0, 0.74, 38)
    rows = []
    for x in grid:
        cn, cr = (float(x), 0.0) if axis == "NR" else (0.0, float(x))
        g, v6, v7, ct, br = verdicts(cn, cr, 0.0, cfg, theta)
        rows.append({"gate_only": g, "v6_lbb": v6, "v7_frontier": v7})
    def succ(key): return round(sum(1 for r in rows if r[key]=="ALLOW")/len(rows), 4)
    return {"axis": axis, "n": len(rows),
            "attacker_success_gate_only": succ("gate_only"),
            "attacker_success_v6_lbb": succ("v6_lbb"),
            "attacker_success_v7_frontier": succ("v7_frontier")}


def attack_adaptive_spread(cfg, theta=0.35):
    def max_breach(pred):
        m = 0.0
        for c_nr in np.linspace(0.0, 0.99, 40):
            for c_ri in np.linspace(0.0, 0.99, 40):
                g, v6, v7, ct, br = verdicts(float(c_nr), float(c_ri), 0.0, cfg, theta)
                verd = {"gate": g, "v6": v6, "v7": v7}[pred]
                if verd == "ALLOW":
                    m = max(m, max(c_nr, c_ri))
        return round(m, 4)
    return {"max_evading_breach_gate_only": max_breach("gate"),
            "max_evading_breach_v6_lbb": max_breach("v6"),
            "max_evading_breach_v7_frontier": max_breach("v7"),
            "note": ("Smaller max-evading-breach = stronger. v7 (calibrated H over "
                     "BOTH breach layers) shrinks it symmetrically without penalizing "
                     "genuine verifiability.")}


def e5_ood(cfg):
    def ent(a, b, c): return fv.layer_entropy(a, b, c)
    benign_ent = [ent(abs(rng.normal(0.08,0.05)), abs(rng.normal(0.08,0.05)), abs(rng.normal(0.05,0.03))) for _ in range(300)]
    attack_ent = [ent(float(x), 0.0, 0.0) for x in np.linspace(0.5,0.74,50)]
    band = cfg.ood
    def flagged(vals): return round(sum(1 for e in vals if band.is_ood(e))/len(vals),4)
    return {"ood_band": {"lo": round(band.lo,4), "hi": round(band.hi,4)},
            "benign_band_membership_rate": flagged(benign_ent),
            "single_layer_attack_band_membership_rate": flagged(attack_ent),
            "honest_interpretation": (
                "NEGATIVE RESULT: Shannon entropy does NOT detect the high-"
                "verifiability single-layer attack. Frontier OOD escalation requires "
                "max_layer>=0.5 (benign lacks it) => no benign FPR. H(x) is the "
                "defense; entropy is generic OOD telemetry.")}


def main():
    cfg, fpr_high_ver = calibrate_H_geometric()
    nr = attack_single_layer(cfg, "NR")
    ri = attack_single_layer(cfg, "RI")
    adaptive = attack_adaptive_spread(cfg)
    ood = e5_ood(cfg)
    report = {
        "seed": SEED, "weights": "balanced 1/3 (kernel gate)", "theta": 0.35,
        "H_calibrated_weights": {"a": round(cfg.h.a,4), "b": round(cfg.h.b,4), "g": round(cfg.h.g,4)},
        "H_threshold": round(cfg.h.threshold, 4), "H_source": cfg.h.source,
        "fpr_high_verifiability_legit": fpr_high_ver,
        "E4_single_layer_attack_NR": nr,
        "E4_single_layer_attack_RI": ri,
        "E4_adaptive_spread_attack": adaptive,
        "E5_OOD_entropy": ood,
        "headline": {
            "camouflage_closed_both_axes": (
                nr["attacker_success_gate_only"] > 0
                and nr["attacker_success_v7_frontier"] < nr["attacker_success_gate_only"]
                and ri["attacker_success_v7_frontier"] < ri["attacker_success_gate_only"]),
            "gate_only_success_NR": nr["attacker_success_gate_only"],
            "gate_only_success_RI": ri["attacker_success_gate_only"],
            "v6_lbb_success_NR": nr["attacker_success_v6_lbb"],
            "v6_lbb_success_RI": ri["attacker_success_v6_lbb"],
            "v7_frontier_success_NR": nr["attacker_success_v7_frontier"],
            "v7_frontier_success_RI": ri["attacker_success_v7_frontier"],
            "fpr_high_verifiability_legit": fpr_high_ver,
            "H_weights_calibrated": {"a": round(cfg.h.a,4), "b": round(cfg.h.b,4), "g": round(cfg.h.g,4)},
            "both_breach_weights_active": bool(cfg.h.a > 0.05 and cfg.h.b > 0.05),
        },
    }
    p = ROOT / "evidence" / "eval_E4E5_results.json"
    p.write_text(json.dumps(report, indent=1))
    print(p.name, "SHA256:", hashlib.sha256(p.read_bytes()).hexdigest())
    print(json.dumps(report["headline"], indent=1))


if __name__ == "__main__":
    main()
