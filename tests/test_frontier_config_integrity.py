"""Integrity tests for the SEALED frontier config (audit fix 2026-07-06).

Unlike test_calibration_covers_both_breach_axes (which uses a hand-built
synthetic corpus), these tests run the REAL frontier_calibrate.py pipeline
that produces evidence/frontier_v7_config.json, and also inspect the sealed
artifact on disk — so the shipped config cannot silently degenerate again
(the a=0 / b=0 single-axis blindness we closed on both axes).
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "core"))
sys.path.insert(0, str(ROOT / "scripts"))


def test_real_pipeline_config_has_both_breach_weights():
    # Runs the SAME pipeline that writes the sealed config (embedder + calibration).
    import frontier_calibrate as fc
    rows, _ = fc.build_rows()
    cfg, degeneracy = fc.build_calibration_config(rows)
    assert cfg.h.a > 0.05, f"N-R weight degenerated: a={cfg.h.a}"
    assert cfg.h.b > 0.05, f"R-I weight degenerated: b={cfg.h.b}"
    assert cfg.h.g < 0.05, f"(1-C_IF) weight should be ~0, got g={cfg.h.g}"
    assert degeneracy["verdict"].startswith("PASS")


def test_sealed_config_artifact_not_degenerate():
    # Ties the shipped artifact: whatever is committed must not be single-axis.
    p = ROOT / "evidence" / "frontier_v7_config.json"
    d = json.loads(p.read_text())
    h = d["h"]
    assert h["a"] > 0.05 and h["b"] > 0.05, f"sealed config is single-axis: {h}"
    assert h["g"] < 0.05, f"sealed config re-introduced (1-C_IF): g={h['g']}"


def test_real_pipeline_config_keeps_e2_zero_fpr():
    # The both-axes weights + E2 threshold must not regress E2 metrics.
    import frontier_calibrate as fc
    rows, _ = fc.build_rows()
    cfg, _ = fc.build_calibration_config(rows)
    m = fc.h_metrics(rows, cfg, use_ver_fuse=True)
    assert m["fpr_on_topic"] == 0.0 and m["fnr_grave"] == 0.0 and m["adversarial_veto"] == 1.0, m
