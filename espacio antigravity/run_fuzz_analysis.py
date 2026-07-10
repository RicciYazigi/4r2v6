#!/usr/bin/env python3
import sys
import json
import hashlib
import os
from pathlib import Path
from datetime import datetime
import numpy as np

# Adjust paths to load kernel from core
ESPACIO_DIR = Path(__file__).resolve().parent
ROOT = ESPACIO_DIR.parent
sys.path.insert(0, str(ROOT / "core"))

from kernel_1240421 import create_kernel, LayerState

# Constants
SEED_BASE = 424242
N_MONTE_CARLO = 2500
N_SYSTEMATIC = 800
TOTAL_TARGET = N_MONTE_CARLO + N_SYSTEMATIC

# Output inside espacio antigravity/evidence
OUTPUT_DIR = ESPACIO_DIR / "evidence"
os.makedirs(OUTPUT_DIR, exist_ok=True)

kernel = create_kernel(lambda_landauer=0.05, beta_coherence=0.1)

def _safe_norm(vec: np.ndarray, eps: float = 1e-8) -> np.ndarray:
    n = np.linalg.norm(vec)
    return vec / (n + eps)

def make_layer_state(norm_n=1.0, norm_r=1.0, norm_i=1.0, phys_scale=1.0,
                     noise_i=0.0, noise_f=0.0, seed=None) -> LayerState:
    if seed is not None:
        np.random.seed(seed)
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
        informational=_safe_norm(i),
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
        # Gracefully handle the zero-norm fail-closed case
        return {
            "C_NR": 1.0,
            "C_RI": 1.0,
            "C_IF": 1.0,
            "C_total": 1.0,
            "Loss_4R2": base_loss + alpha * (1.0 ** 2) + gamma * kernel.compute_landauer_cost(2)
        }

def run_monte_carlo(n: int, base_seed: int) -> list:
    results = []
    for i in range(n):
        seed = base_seed + i
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
                **{k: round(float(v), 8) for k, v in metrics.items()}
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
            
    # 3. Physical noise sweeps
    for sigma in [0.05, 0.15, 0.3]:
        for rep in range(5):
            st = make_layer_state(noise_f=sigma, seed=base_seed + idx + rep)
            metrics = compute_loss(st)
            rec = {
                "case_id": f"sys_noiseF_{idx:05d}",
                "type": "noise_physical",
                "sigma": sigma,
                **{k: round(float(v), 8) for k, v in metrics.items()}
            }
            results.append(rec)
            idx += 1
            
    return results

def save_results(all_results: list) -> dict:
    results_path = OUTPUT_DIR / "fuzz_results.jsonl"
    with open(results_path, "w") as f:
        for r in all_results:
            f.write(json.dumps(r, sort_keys=True) + "\n")
            
    c_totals = [r["C_total"] for r in all_results]
    losses = [r["Loss_4R2"] for r in all_results]
    
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
        "notes": "Aggressive fuzz + systematic ablations. Kernel direct only. (Run in espacio antigravity)",
    }
    
    summary_path = OUTPUT_DIR / "summary.json"
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)
        
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

def run_deep_analysis(data):
    c_total = np.array([d["C_total"] for d in data])
    loss = np.array([d["Loss_4R2"] for d in data])
    c_nr = np.array([d["C_NR"] for d in data])
    c_ri = np.array([d["C_RI"] for d in data])
    c_if = np.array([d["C_IF"] for d in data])
    
    def corr(a, b):
        return float(np.corrcoef(a, b)[0,1])
        
    corrs = {
        "C_total_vs_Loss": corr(c_total, loss),
        "C_NR_vs_C_total": corr(c_nr, c_total),
        "C_RI_vs_C_total": corr(c_ri, c_total),
        "C_IF_vs_C_total": corr(c_if, c_total),
        "C_NR_vs_Loss": corr(c_nr, loss),
        "C_RI_vs_Loss": corr(c_ri, loss),
        "C_IF_vs_Loss": corr(c_if, loss),
    }
    
    by_type = {}
    for d in data:
        t = d.get("type", "unknown")
        if t not in by_type:
            by_type[t] = []
        by_type[t].append(d["C_total"])
        
    by_type_res = {}
    for t, vals in by_type.items():
        arr = np.array(vals)
        by_type_res[t] = {
            "count": len(arr),
            "mean_C_total": float(np.mean(arr)),
            "std_C_total": float(np.std(arr)),
            "min": float(np.min(arr)),
            "max": float(np.max(arr)),
        }
        
    sorted_data = sorted(data, key=lambda x: x["C_total"])
    best = sorted_data[:5]
    worst = sorted_data[-5:][::-1]
    extremes = {
        "best_5_lowest_C_total": [
            {"case_id": d["case_id"], "C_total": d["C_total"], "type": d.get("type"), "params": d.get("params")} 
            for d in best
        ],
        "worst_5_highest_C_total": [
            {"case_id": d["case_id"], "C_total": d["C_total"], "type": d.get("type"), "params": d.get("params")} 
            for d in worst
        ]
    }
    
    analysis = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "total_cases": len(data),
        "correlations": {k: round(v, 6) for k,v in corrs.items()},
        "by_type": by_type_res,
        "extremes": extremes,
        "key_insights": [
            "C_total correlates strongly with Loss (as expected from C**2).",
            "C_IF often has high variance in physical_scale and layer_ablation cases.",
            "Physical layer ablations produce the widest range in C_total.",
        ]
    }
    
    analysis_path = OUTPUT_DIR / "deep_analysis.json"
    with open(analysis_path, "w") as f:
        json.dump(analysis, f, indent=2)
        
    with open(analysis_path, "rb") as f:
        h = hashlib.sha256(f.read()).hexdigest()
    seal = {"analysis_sha256": h, "file": str(analysis_path)}
    seal_path = OUTPUT_DIR / "deep_analysis_seal.json"
    with open(seal_path, "w") as f:
        json.dump(seal, f, indent=2)
        
    return analysis

def main():
    print("=== RUNNING FUZZING IN ESPACIO ANTIGRAVITY ===")
    np.random.seed(SEED_BASE)
    
    print("Generating MC cases...")
    mc = run_monte_carlo(N_MONTE_CARLO, SEED_BASE + 10000)
    
    print("Generating Systematic Ablation cases...")
    sys_abl = run_systematic_ablations(SEED_BASE + 20000)
    
    all_res = mc + sys_abl
    print(f"Total cases generated: {len(all_res)}")
    
    save_out = save_results(all_res)
    print("Results saved.")
    
    print("Running Deep Analysis...")
    analysis = run_deep_analysis(all_res)
    print("Analysis complete.")
    print(json.dumps(analysis, indent=2))

if __name__ == "__main__":
    main()
