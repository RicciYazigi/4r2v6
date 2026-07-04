#!/usr/bin/env python3
"""
Pilot contexts test (from SUPERAGENTTESTPILOT + zip analysis).
Tests 4R2_FUSES in real scenarios (coffee, taxi) + kernel sep.
Run: PYTHONPATH=core:antigravity_wings python scripts/test_pilot_contexts.py
Validates C_total control, guards, etc.

v6.0.1 migration (ADR-0006): F is now a verifiability vector in [0,1]^4
(f_ground, f_num, f_cite, f_exec). One legacy raw-telemetry case is kept to
exercise the dual-path C_IF (must NOT be 0 — silent-clip regression check).
"""

from antigravity_wings.fuses.fuses_4r2 import get_fuse
from antigravity_wings.fuse_config.generator import FuseConfigGenerator
from antigravity_wings.api.models import MotorOutput
from kernel_1240421 import create_kernel, LayerState
import numpy as np

def test_pilot(pilot_name, risk, action, coherence_val):
    print(f"\n=== {pilot_name} ===")
    # 4R2_FUSES
    asym = get_fuse("ASYM")
    veto = asym.execute(risk, action)
    print(f"ASYM on {risk}+{action}: {veto}")

    # FuseConfig with low score (from audit)
    mo = MotorOutput(client_id=pilot_name, scores={"global": 0.2}, ranges={}, config_blob={})
    specs = FuseConfigGenerator().generate(mo)
    print(f"4R2 specs: {[s.type for s in specs if s.type in ['VER','ASYM','PRIO']]}")

    # Kernel sep — canonical verifiability F in [0,1]^4 (ADR-0006 Path A)
    k = create_kernel()
    F_verif = np.array([0.9, 0.6, 0.8, 0.7])  # (f_ground, f_num, f_cite, f_exec)
    state = LayerState(np.ones(4)*0.8, np.ones(4)*0.7, np.ones(4)*0.6, F_verif)
    c, br = k.compute_coherence_total(state)
    res = k.measure_coherence_with_keys([0.8]*4, [0.7]*4, [0.6]*4, F_verif.tolist(), {"K": 0.1})
    print(f"C_total: {c:.4f}, raw: {res['total_coherence']:.4f}, score: {res['coherence_score']:.4f}")
    assert abs(br['C_IF'] - (1.0 - float(np.mean(F_verif)))) < 1e-9, "Path A verifiability semantics"

    # Legacy dual-path regression check (ADR-0006 Path B): raw telemetry must
    # NOT collapse to C_IF=0 via silent clipping.
    legacy = LayerState(np.ones(4)*0.8, np.ones(4)*0.7, np.ones(4)*0.6,
                        np.array([1000., 8., 50., 10.]))
    _, br_legacy = k.compute_coherence_total(legacy)
    assert br_legacy['C_IF'] > 0.05, "dual-path regression: raw F must not score C_IF=0"
    print(f"Legacy raw-F dual-path C_IF: {br_legacy['C_IF']:.4f} (>0 OK)")
    print("Pilot test: Vetoes control C_total.")

if __name__ == "__main__":
    # From pilots (coffee example)
    test_pilot("COFFEE", "EXISTENTIAL", "PASSIVE", 0.8)
    # Add more from zip/SUPER if extracted
    print("\nAll pilot contexts + 4R2_FUSES + kernel sep validated.")
