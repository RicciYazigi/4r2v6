"""MATH-property tests for the v7.0 Frontier module (provable guarantees only).

Empirical numbers live in scripts/frontier_calibrate.py (seeded, sealed). These
tests assert only what is mathematically provable, per the project honesty rule.
"""
import sys, math
from pathlib import Path
import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "core"))
import frontier_v7 as fv


def test_selftest_all_pass():
    assert fv.selftest()["ALL_PASS"] is True


def test_H_bounded_on_simplex():
    # MATH: convex combination of values in [0,1] stays in [0,1].
    for a in np.linspace(0, 1, 5):
        for b in np.linspace(0, 1, 5):
            for c in np.linspace(0, 1, 5):
                h = fv.h_energy(a, b, c)
                assert -1e-9 <= h <= 1 + 1e-9


def test_H_monotone_nondecreasing():
    p = fv.HParams(1/3, 1/3, 1/3)
    assert fv.h_energy(0.9, 0.2, 0.5, p) > fv.h_energy(0.1, 0.2, 0.5, p)
    assert fv.h_energy(0.2, 0.9, 0.5, p) > fv.h_energy(0.2, 0.1, 0.5, p)
    # rises as verifiability falls (1 - C_IF grows)
    assert fv.h_energy(0.2, 0.2, 0.1, p) > fv.h_energy(0.2, 0.2, 0.9, p)


def test_entropy_bounded_ln3():
    for _ in range(200):
        a, b, c = np.random.rand(3)
        e = fv.layer_entropy(a, b, c)
        assert 0.0 <= e <= math.log(3.0) + 1e-9


def test_single_layer_has_low_entropy():
    # A breach concentrated in one layer is lower-entropy than a diffuse one.
    e_single = fv.layer_entropy(0.9, 0.0, 1.0)   # only C_NR
    e_diffuse = fv.layer_entropy(0.5, 0.5, 0.5)
    assert e_single < e_diffuse


def test_camouflage_js_bounded_ln2():
    edges = np.linspace(0, 1, 9).tolist()
    ref = [1.0] * 8
    for _ in range(50):
        obs = np.random.rand(30).tolist()
        js = fv.camouflage_js(obs, ref, edges)
        assert 0.0 <= js <= math.log(2.0) + 1e-9


def test_frontier_is_escalation_only():
    # MATH/contract: v7 NEVER upgrades a v6 verdict (fail-closed monotonicity).
    order = {"ALLOW": 0, "FLAG": 1, "BLOCK": 2}
    cfg = fv.FrontierConfig(fv.HParams(0, 1, 0, 0.42), fv.OODBand(1.0, 1.1))
    for base in ("ALLOW", "FLAG", "BLOCK"):
        for _ in range(100):
            bd = {"C_NR": np.random.rand(), "C_RI": np.random.rand(), "C_IF": np.random.rand()}
            out = fv.frontier_verdict(bd, base, cfg)
            assert order[out["verdict"]] >= order[base]


def test_default_config_is_lbb_passthrough():
    # Uncalibrated default must not escalate on H or OOD (threshold>1, full band).
    cfg = fv.FrontierConfig.default()
    # a clean ALLOW with no layer breach stays ALLOW
    bd = {"C_NR": 0.1, "C_RI": 0.1, "C_IF": 0.9}
    assert fv.frontier_verdict(bd, "ALLOW", cfg)["verdict"] == "ALLOW"
    # frozen LBB floor still fires at max_layer >= 0.75
    bd2 = {"C_NR": 0.8, "C_RI": 0.1, "C_IF": 0.9}
    assert fv.frontier_verdict(bd2, "ALLOW", cfg)["verdict"] == "BLOCK"


def test_calibrate_h_handles_camouflage_gracefully():
    # Adversarial camouflaged as benign layers => Fisher can't separate =>
    # must fall back to a safe default, never crash.
    rows = [{"C_NR": 0.1, "C_RI": 0.1, "C_IF": 0.9, "label": "on-topic"} for _ in range(10)]
    rows += [{"C_NR": 0.1, "C_RI": 0.1, "C_IF": 0.9, "label": "adversarial"} for _ in range(10)]
    hp = fv.calibrate_h_from_rows(rows, positive_label="adversarial")
    assert isinstance(hp, fv.HParams)
    assert 0.0 <= fv.h_energy(0.5, 0.5, 0.5, hp) <= 1.0


def test_balanced_H_penalizes_perfect_verifiability_REGRESSION():
    # Reviewer finding (2026-07-05): with g>0, perfect verifiability (C_IF=0)
    # inflates H. This documents WHY the balanced config is retired: an
    # impeccable legit case scores as high as a mild attacker.
    hp_bal = fv.HParams(1/3, 1/3, 1/3)
    h_impeccable = fv.h_energy(0.0, 0.0, 0.0, hp_bal)   # no breach, perfect ver
    h_mediocre_ver = fv.h_energy(0.0, 0.0, 0.5, hp_bal)  # no breach, mediocre ver
    assert h_impeccable > h_mediocre_ver  # the symmetric-vulnerability signature


def test_calibration_drives_gamma_to_zero_on_camouflage():
    # FIX: calibrating H on (high-ver legit vs camouflage attack) must drive the
    # weight on (1-C_IF) to ~0, because it is non-discriminative for this attack.
    rng = np.random.default_rng(1240421)
    legit = [{"C_NR": float(min(0.25, abs(rng.normal(0.08,0.06)))),
              "C_RI": float(min(0.25, abs(rng.normal(0.08,0.06)))),
              "C_IF": 0.0, "label": "on-topic"} for _ in range(120)]
    attack = [{"C_NR": float(x), "C_RI": 0.0, "C_IF": 0.0, "label": "off-topic-grave"}
              for x in np.linspace(0.45, 0.74, 60)]
    hp = fv.calibrate_h_from_rows(legit + attack)
    assert hp.g < 0.05, f"gamma should calibrate ~0, got {hp.g}"
    # and FPR on the high-ver legit set must be 0 with the calibrated H
    fpr = sum(1 for r in legit
              if fv.h_energy(r["C_NR"], r["C_RI"], r["C_IF"], hp) >= hp.threshold) / len(legit)
    assert fpr == 0.0, f"calibrated H must not flag high-ver legit, FPR={fpr}"


def test_calibration_covers_both_breach_axes():
    # Reviewer finding #2 (2026-07-05): a single-axis (C_NR-only) corpus made
    # Fisher learn b=0, so a camouflage attack in C_RI evaded H. FIX: calibrate
    # on BOTH axes. This test FAILS if either N-R or R-I high-ver camouflage
    # attack (breach in [0.45,0.74], under LBB, perfect verifiability) gets ALLOW.
    rng = np.random.default_rng(1240421)
    legit = [{"C_NR": float(min(0.25, abs(rng.normal(0.08,0.06)))),
              "C_RI": float(min(0.25, abs(rng.normal(0.08,0.06)))),
              "C_IF": 0.0, "label": "on-topic"} for _ in range(120)]
    atk = []
    for x in np.linspace(0.45, 0.74, 30):
        atk.append({"C_NR": float(x), "C_RI": 0.0, "C_IF": 0.0, "label": "off-topic-grave"})
        atk.append({"C_NR": 0.0, "C_RI": float(x), "C_IF": 0.0, "label": "off-topic-grave"})
    hp = fv.calibrate_h_from_rows(legit + atk)
    # neither breach weight may degenerate to 0
    assert hp.a > 0.05 and hp.b > 0.05, f"breach weight degenerated: a={hp.a}, b={hp.b}"
    cfg = fv.FrontierConfig(hp, fv.calibrate_ood_band(legit + atk))
    # both-axis camouflage attacks must NOT be ALLOWed through the full pipeline
    for x in np.linspace(0.45, 0.74, 15):
        for cn, cr in ((float(x), 0.0), (0.0, float(x))):
            bd = {"C_NR": cn, "C_RI": cr, "C_IF": 0.0}
            ct = (cn + cr + 0.0) / 3.0
            base = "ALLOW" if ct <= 0.35 else ("FLAG" if ct <= 0.50 else "BLOCK")
            v = fv.frontier_verdict(bd, base, cfg)["verdict"]
            assert v != "ALLOW", f"camouflage axis breach {cn,cr} evaded: {v}"
