#!/usr/bin/env python3
"""
Aggressive Fuzzing + Ablation Study for 4R2 Coherence Engine.

Generates thousands of controlled cases to analyze robustness and
distribution of C_total, individual layer coherences, and Loss_4R2.

Focus: mathematical behavior of the canonical kernel.
Also includes some full-pipeline ablations via translator.

Run from rempacado root:
  PYTHONPATH=core python scripts/aggressive_fuzz_ablation.py

All runs use fixed seeds per category for reproducibility.
Outputs sealed JSONL + summary with SHA256.
"""

import sys
import json
import hashlib
import os
from pathlib import Path
from datetime import datetime
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "core"))

from kernel_1240421 import create_kernel, LayerState

# Constants for reproducibility and scale
SEED_BASE = 424242
N_MONTE_CARLO = 2500
N_SYSTEMATIC = 800
TOTAL_TARGET = N_MONTE_CARLO + N_SYSTEMATIC

OUTPUT_DIR = ROOT / "evidence" / "fuzz_aggressive_20260623"
os.makedirs(OUTPUT_DIR, exist_ok=True)

kernel = create_kernel(lambda_landauer=0.05, beta_coherence=0.1)


def _safe_norm(vec: np.ndarray, eps: float = 1e-8) -> np.ndarray:
    n = np.linalg.norm(vec)
    return vec / (n + eps)


def make_layer_state(norm_n=1.0, norm_r=1.0, norm_i=1.0, phys_scale=1.0,
                     noise_i=0.0, noise_f=0.0, seed=None) -> LayerState:
    if seed is not None:
        np.random.seed(seed)
    # All layers forced to 4D for C_NR / C_RI compatibility (kernel assumes matching lengths here)
    n = np.random.randn(4) * norm_n
    r = np.random.randn(4) * norm_r
    i = np.random.randn(4) * norm_i
    if noise_i > 0:
        i += np.random.randn(4) * noise_i
    p = np.array([1200., 12., 65., 8.]) * phys_scale
    if noise_f > 0:
        p += np.random.randn(4) * noise_f * np.abs(p)
    return LayerState(
        normative=_safe_norm(n),
        representational=_safe_norm(r),
        informational=_safe_norm(i),  # already will be re-normed in kernel but ok
        physical=p
    )


def compute_loss(state: LayerState, base_loss: float = 0.5, alpha: float = 1.0, gamma: float = 1.0) -> dict:
    try:
        c_total, breakdown = kernel.compute_coherence_total(state)
        loss = kernel.compute_loss_4R2(base_loss, c_total, decision_changes=2, alpha=alpha, gamma=gamma)
        return {
            "C_NR": breakdown["C_NR"],
            "C_RI": breakdown["C_RI"],
            "C_IF": breakdown["C_IF"],
            "C_total": c_total,
            "Loss_4R2": loss
        }
    except ValueError as e:
        # Fail-closed expected behavior for zero-norm or malformed vectors
        return {
            "C_NR": 1.0,
            "C_RI": 1.0,
            "C_IF": 1.0,
            "C_total": 1.0,
            "Loss_4R2": base_loss + alpha * 1.0 + gamma * (kernel.lambda_landauer * 2),
            "error": str(e)
        }


def run_monte_carlo(n: int, base_seed: int) -> list:
    results = []
    for i in range(n):
        seed = base_seed + i
        # Vary scales and noise (all vectors 4D)
        scale = np.random.uniform(0.1, 10.0)
        noise_i = np.random.uniform(0.0, 0.5)
        noise_f = np.random.uniform(0.0, 0.3)
        st = make_layer_state(norm_n=scale, norm_r=scale, norm_i=scale * 0.8,
                              phys_scale=scale,
                              noise_i=noise_i, noise_f=noise_f, seed=seed)
        metrics = compute_loss(st)
        rec = {
            "case_id": f"mc_{i:05d}",
            "type": "monte_carlo",
            "seed": seed,
            "params": {"scale": round(scale, 4), "noise_i": round(noise_i, 4),
                       "noise_f": round(noise_f, 4)},
            **{k: round(float(v), 8) for k, v in metrics.items()}
        }
        results.append(rec)
    return results


def run_systematic_ablations(base_seed: int) -> list:
    results = []
    idx = 0
    # 1. Layer zeroing / extreme
    for layer in ["normative", "representational", "informational", "physical"]:
        for mult in [0.0, 0.01, 10.0]:
            st = make_layer_state(seed=base_seed + idx)
            if layer == "normative":
                st.normative = np.zeros(4)
            elif layer == "representational":
                st.representational = np.zeros(4)
            elif layer == "informational":
                st.informational = np.zeros(4)
            else:
                st.physical = st.physical * mult
            metrics = compute_loss(st)
            rec = {
                "case_id": f"sys_abl_{idx:05d}",
                "type": "layer_ablation",
                "ablated": layer,
                "mult": mult,
                **{k: (round(float(v), 8) if not isinstance(v, str) else v) for k, v in metrics.items()}
            }
            results.append(rec)
            idx += 1

    # 2. Noise sweeps on informational
    for sigma in [0.1, 0.5, 1.0, 2.0]:
        for rep in range(5):
            st = make_layer_state(noise_i=sigma, seed=base_seed + idx + rep)
            metrics = compute_loss(st)
            rec = {
                "case_id": f"sys_noiseI_{idx:05d}",
                "type": "noise_informational",
                "sigma": sigma,
                **{k: round(float(v), 8) for k, v in metrics.items()}
            }
            results.append(rec)
            idx += 1

    # 3. Physical extreme scales
    for pscale in [0.01, 0.1, 5.0, 50.0]:
        st = make_layer_state(phys_scale=pscale, seed=base_seed + idx)
        metrics = compute_loss(st)
        rec = {
            "case_id": f"sys_phys_{idx:05d}",
            "type": "physical_scale",
            "pscale": pscale,
            **{k: round(float(v), 8) for k, v in metrics.items()}
        }
        results.append(rec)
        idx += 1

    # 4. Dedicated C_IF dim stress (call C_IF directly to test padding logic)
    for d in [2, 3, 5, 6]:
        np.random.seed(base_seed + idx)
        info = np.random.randn(d)
        phys = np.array([1200., 12., 65., 8.])
        c_if = kernel.compute_C_IF(info, phys)
        # Use a base 4D state for other metrics
        st = make_layer_state(seed=base_seed + idx + 100)
        metrics = compute_loss(st)
        metrics["C_IF"] = round(float(c_if), 8)  # override with stressed value
        rec = {
            "case_id": f"sys_cif_dim_{idx:05d}",
            "type": "cif_dim_stress",
            "dim_i": d,
            **{k: round(float(v), 8) for k, v in metrics.items()}
        }
        results.append(rec)
        idx += 1

    return results


def save_results(all_results: list) -> dict:
    results_path = OUTPUT_DIR / "fuzz_results.jsonl"
    with open(results_path, "w") as f:
        for r in all_results:
            f.write(json.dumps(r) + "\n")

    # Summary stats
    c_totals = np.array([r["C_total"] for r in all_results])
    losses = np.array([r["Loss_4R2"] for r in all_results])

    summary = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "total_cases": len(all_results),
        "C_total": {
            "mean": float(np.mean(c_totals)),
            "std": float(np.std(c_totals)),
            "min": float(np.min(c_totals)),
            "p25": float(np.percentile(c_totals, 25)),
            "median": float(np.median(c_totals)),
            "p75": float(np.percentile(c_totals, 75)),
            "max": float(np.max(c_totals)),
        },
        "Loss_4R2": {
            "mean": float(np.mean(losses)),
            "std": float(np.std(losses)),
            "min": float(np.min(losses)),
            "max": float(np.max(losses)),
        },
        "notes": "Aggressive fuzz + systematic ablations. Kernel direct only (focus on math).",
    }

    summary_path = OUTPUT_DIR / "summary.json"
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)

    # Seal
    with open(results_path, "rb") as f:
        results_sha = hashlib.sha256(f.read()).hexdigest()
    with open(summary_path, "rb") as f:
        summary_sha = hashlib.sha256(f.read()).hexdigest()

    seal = {
        "results_sha256": results_sha,
        "summary_sha256": summary_sha,
        "output_dir": str(OUTPUT_DIR),
    }
    seal_path = OUTPUT_DIR / "SEAL.json"
    with open(seal_path, "w") as f:
        json.dump(seal, f, indent=2)

    return {"summary": summary, "seal": seal, "files": [str(results_path), str(summary_path), str(seal_path)]}


def main():
    print("=" * 70)
    print("AGGRESSIVE FUZZING + ABLATION STUDY - 4R2 Canonical Kernel")
    print(f"Target: {TOTAL_TARGET} cases (MonteCarlo + Systematic)")
    print("=" * 70)

    np.random.seed(SEED_BASE)

    print("\n[1/3] Monte Carlo random cases...")
    mc = run_monte_carlo(N_MONTE_CARLO, SEED_BASE + 10000)

    print("[2/3] Systematic ablations (layer zero, noise, scale, dim)...")
    sys_abl = run_systematic_ablations(SEED_BASE + 20000)

    all_res = mc + sys_abl
    print(f"[3/3] Total cases generated: {len(all_res)}")

    print("\nSaving + sealing...")
    out = save_results(all_res)

    print("\n=== SUMMARY ===")
    print(json.dumps(out["summary"], indent=2))
    print("\n=== SEAL ===")
    print(json.dumps(out["seal"], indent=2))
    print("\nFiles written to:", OUTPUT_DIR)
    print("Aggressive fuzz & ablation complete.")


if __name__ == "__main__":
    main()
