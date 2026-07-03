#!/usr/bin/env python3
"""
NRIF Calibration Protocol (addresses Auditoria_Brutal_V40 Gap #1)
Derives/justifies layer weights from empirical data (synthetic pilots here).
Prioritizes Physics (F via C_IF) per "F=16" doctrine for Stillness.

Run: python scripts/nrif_calibration.py
Outputs: before/after C_total, Landauer deltas, recommended weights.

Math invariant: C_total is always weighted SUM (lower=better). 
Changing w_IF upward increases C_total penalty on physical misalignment
(energy/latency high → worse reported coherence) while Landauer penalty
in loss_4R2 remains additive and orthogonal.
"""
import numpy as np
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "4R2-MASTER-DELIVERY" / "tests"))

from kernel_1240421 import CoherenceKernel, LayerState, create_kernel

def synthetic_pilot_data(n=200, seed=42):
    """Generate aligned vs misaligned states (proxy for real traces)."""
    rng = np.random.default_rng(seed)
    data = []
    for _ in range(n):
        # Normative (ethics/declared) - relatively stable
        nrm = rng.normal(0.8, 0.1, 4)
        # Representational close or drifted
        rep = nrm + rng.normal(0, 0.05 if rng.random() > 0.3 else 0.25, 4)
        # Informational (output)
        inf = rep + rng.normal(0, 0.1, 4)
        # Physical: [FLOPS_norm, mem, energy, latency] - high variance bad
        phys = np.array([
            rng.uniform(0.6, 1.0),
            rng.uniform(0.5, 0.9),
            rng.uniform(0.2, 1.3),  # energy can be bad
            rng.uniform(0.1, 1.5),  # latency bad = high cost
        ])
        is_critical = rng.random() > 0.7  # simulate project/critical PSC
        data.append({
            "state": LayerState(
                normative=np.clip(nrm, 0, 1),
                representational=np.clip(rep, 0, 1),
                informational=np.clip(inf, 0, 1),
                physical=phys
            ),
            "decision_changes": int(rng.integers(0, 4)) if is_critical else int(rng.integers(0, 2)),
            "is_critical": is_critical
        })
    return data

def evaluate_set(kernel: CoherenceKernel, data):
    c_totals = []
    landauers = []
    losses = []
    for d in data:
        c, _ = kernel.compute_coherence_total(d["state"])
        l = kernel.compute_landauer_cost(d["decision_changes"])
        # use base_loss proxy
        base = 0.2
        loss = kernel.compute_loss_4R2(base, c, d["decision_changes"])
        c_totals.append(c)
        landauers.append(l)
        losses.append(loss)
    return {
        "mean_C_total": float(np.mean(c_totals)),
        "max_C_total": float(np.max(c_totals)),
        "mean_Landauer": float(np.mean(landauers)),
        "mean_loss": float(np.mean(losses)),
        "n": len(data)
    }

def main():
    print("=" * 60)
    print("NRIF CALIBRATION PROTOCOL v1 (Brutal Gap #1 closure)")
    print("Source data: synthetic pilots (replace with real traces)")
    print("Target doctrine: Physics priority (F-layer via C_IF weight)")
    print("=" * 60)

    pilots = synthetic_pilot_data(300)

    # Baseline equal weights (current DELIVERY default)
    k_base = create_kernel(lambda_landauer=0.05, beta_coherence=0.1,
                           weights={"w_NR": 1/3, "w_RI": 1/3, "w_IF": 1/3})
    base_stats = evaluate_set(k_base, pilots)
    print("\n[BASELINE equal 1/3]")
    print(base_stats)

    # Brutal-inspired: elevate physics (C_IF) to ~0.5 effective share
    # (remaining distributed; sum must =1)
    k_phys = create_kernel(lambda_landauer=0.05, beta_coherence=0.1,
                           weights={"w_NR": 0.25, "w_RI": 0.25, "w_IF": 0.50})
    phys_stats = evaluate_set(k_phys, pilots)
    print("\n[PHYSICS PRIORITY w_IF=0.50]")
    print(phys_stats)

    delta_c = phys_stats["mean_C_total"] - base_stats["mean_C_total"]
    delta_l = phys_stats["mean_Landauer"] - base_stats["mean_Landauer"]
    print("\n[DELTAS]")
    print(f"Delta mean_C_total = {delta_c:+.6f}  (higher = more sensitive to physical misalignment)")
    print(f"Delta mean_Landauer (normalized) = {delta_l:+.6f}  (orthogonal to weights; driven by decision_changes)")
    print(f"Note: elevated w_IF raises C_total on high-energy/latency cases -> earlier Stillness trigger.")
    print("Landauer term in loss_4R2 stays gamma-driven and additive.")

    # Recommended for v5.2 PSC "Soberano" (high gravity): even stronger F
    k_sober = create_kernel(lambda_landauer=0.02, beta_coherence=0.05,
                            weights={"w_NR": 0.20, "w_RI": 0.20, "w_IF": 0.60})
    sober_stats = evaluate_set(k_sober, [d for d in pilots if d["is_critical"]])
    print("\n[SOBERANO mode (critical subset, w_IF=0.60, low lambda)]")
    print(sober_stats)

    print("\n[RECOMMENDATION]")
    print("1. Use data-driven sweep on real pilot traces to lock w_* (F >= 0.4).")
    print("2. Persist weights + justification + sha of input data as evidence.")
    print("3. Feed PSC intent_level -> dynamic weights (Scribe).")
    print("4. Never mutate kernel math; only regime/weights from upper layer.")

    # Emit minimal evidence line for traceability
    print("\nEVIDENCE_LINE:", {
        "protocol": "NRIF_CAL_V1_BRUTAL_GAP1",
        "baseline_mean_C": round(base_stats["mean_C_total"], 6),
        "phys_prior_mean_C": round(phys_stats["mean_C_total"], 6),
        "delta_C": round(delta_c, 6),
        "source": "synthetic_300"
    })

if __name__ == "__main__":
    main()
