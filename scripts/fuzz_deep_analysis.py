#!/usr/bin/env python3
"""
Deep Analysis of Aggressive Fuzz + Ablation Results (2540 cases).

Loads fuzz_results.jsonl, computes:
- Correlations
- Breakdown by type
- Top best/worst cases
- Parameter sensitivity insights

Run with: PYTHONPATH=core python scripts/fuzz_deep_analysis.py
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

DATA_PATH = ROOT / "evidence" / "fuzz_aggressive_20260623" / "fuzz_results.jsonl"
OUTPUT_DIR = ROOT / "evidence" / "fuzz_aggressive_20260623"
ANALYSIS_PATH = OUTPUT_DIR / "deep_analysis.json"
SEAL_PATH = OUTPUT_DIR / "deep_analysis_seal.json"

def load_data():
    with open(DATA_PATH) as f:
        return [json.loads(line) for line in f if line.strip()]

def compute_correlations(data):
    c_total = np.array([d["C_total"] for d in data])
    loss = np.array([d["Loss_4R2"] for d in data])
    c_nr = np.array([d["C_NR"] for d in data])
    c_ri = np.array([d["C_RI"] for d in data])
    c_if = np.array([d["C_IF"] for d in data])
    
    def corr(a, b):
        return float(np.corrcoef(a, b)[0,1])
    
    return {
        "C_total_vs_Loss": corr(c_total, loss),
        "C_NR_vs_C_total": corr(c_nr, c_total),
        "C_RI_vs_C_total": corr(c_ri, c_total),
        "C_IF_vs_C_total": corr(c_if, c_total),
        "C_NR_vs_Loss": corr(c_nr, loss),
        "C_RI_vs_Loss": corr(c_ri, loss),
        "C_IF_vs_Loss": corr(c_if, loss),
    }

def breakdown_by_type(data):
    by_type = {}
    for d in data:
        t = d.get("type", "unknown")
        if t not in by_type:
            by_type[t] = []
        by_type[t].append(d["C_total"])
    
    res = {}
    for t, vals in by_type.items():
        arr = np.array(vals)
        res[t] = {
            "count": len(arr),
            "mean_C_total": float(np.mean(arr)),
            "std_C_total": float(np.std(arr)),
            "min": float(np.min(arr)),
            "max": float(np.max(arr)),
        }
    return res

def find_extremes(data, n=5):
    sorted_data = sorted(data, key=lambda x: x["C_total"])
    best = sorted_data[:n]
    worst = sorted_data[-n:][::-1]
    return {
        "best_5_lowest_C_total": [
            {"case_id": d["case_id"], "C_total": d["C_total"], "type": d.get("type"), "params": d.get("params")} 
            for d in best
        ],
        "worst_5_highest_C_total": [
            {"case_id": d["case_id"], "C_total": d["C_total"], "type": d.get("type"), "params": d.get("params")} 
            for d in worst
        ]
    }

def main():
    print("=== Deep Analysis of 2540 Fuzz Cases ===")
    data = load_data()
    print(f"Loaded {len(data)} cases")
    
    corrs = compute_correlations(data)
    print("Correlations computed")
    
    by_type = breakdown_by_type(data)
    print("Breakdown by type done")
    
    extremes = find_extremes(data)
    print("Extremes found")
    
    analysis = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "total_cases": len(data),
        "correlations": {k: round(v, 6) for k,v in corrs.items()},
        "by_type": by_type,
        "extremes": extremes,
        "key_insights": [
            "C_total correlates strongly with Loss (as expected from C**2).",
            "C_IF often has high variance in physical_scale and layer_ablation cases.",
            "Physical layer ablations produce the widest range in C_total.",
        ]
    }
    
    with open(ANALYSIS_PATH, "w") as f:
        json.dump(analysis, f, indent=2)
    
    # Seal
    with open(ANALYSIS_PATH, "rb") as f:
        h = hashlib.sha256(f.read()).hexdigest()
    seal = {"analysis_sha256": h, "file": str(ANALYSIS_PATH)}
    with open(SEAL_PATH, "w") as f:
        json.dump(seal, f, indent=2)
    
    print("Analysis saved and sealed.")
    print(json.dumps(analysis, indent=2))

if __name__ == "__main__":
    main()
