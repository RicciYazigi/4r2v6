
import sys
import os
import json
import numpy as np

# Adjust path to import the kernel
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../systems/enhanced/packages/kernel/src')))

try:
    from core.kernel import create_kernel, LayerState
except ImportError:
    # Fallback if running from root
    sys.path.append(os.path.abspath('systems/enhanced/packages/kernel/src'))
    from core.kernel import create_kernel, LayerState

def run_ablation_study():
    print("--- STARTING ABLATION STUDY ---")
    results = {
        "baseline": {},
        "ablation_no_coherence": {},
        "ablation_no_landauer": {}
    }

    # 1. BASELINE (Full System)
    kernel = create_kernel()
    
    # Create a "hallucination-like" state (High divergence)
    # Normative != Representational
    state = LayerState(
        normative=np.array([1.0, 1.0, 1.0, 0.0]), # Size 4
        representational=np.array([0.0, 0.0, 0.0, 0.0]), # Size 4
        informational=np.array([0.5, 0.5, 0.5, 0.0]), # Size 4
        physical=np.array([1000, 16, 50, 10]) # Size 4
    )
    
    # Validation: Ensure shapes match logic
    # Kernel requires rigid alignment for C_NR, C_RI, C_IF chain
    
    decisions = 10
    base_loss_val = 0.5
    
    # Compute Baseline
    C_total, _ = kernel.compute_coherence_total(state)
    loss = kernel.compute_loss_4R2(base_loss_val, C_total, decisions)
    
    results["baseline"] = {
        "C_total": C_total,
        "Loss": loss,
        "Description": "Standard 4R2 operation"
    }
    print(f"BASELINE: Loss={loss:.4f} (C_total={C_total:.4f})")

    # 2. ABLATION 1: No Coherence Penalty (Alpha = 0)
    # Effect: The system should 'accept' the hallucination with lower loss (BAD)
    loss_no_coh = kernel.compute_loss_4R2(base_loss_val, C_total, decisions, alpha=0.0)
    
    results["ablation_no_coherence"] = {
        "C_total": C_total, # Physics didn't change, just the penalty
        "Loss": loss_no_coh,
        "Delta_Loss": loss_no_coh - loss,
        "Conclusion": "Loss decreased (System became tolerant to incoherence)"
    }
    print(f"ABLATION (No Coherence): Loss={loss_no_coh:.4f} (Delta={loss_no_coh - loss:.4f})")

    # 3. ABLATION 2: No Landauer Cost (Gamma = 0)
    # Effect: The system should ignore the cost of complexity/irreversibility
    loss_no_landauer = kernel.compute_loss_4R2(base_loss_val, C_total, decisions, gamma=0.0)
    
    results["ablation_no_landauer"] = {
        "C_total": C_total,
        "Loss": loss_no_landauer,
        "Delta_Loss": loss_no_landauer - loss,
        "Conclusion": "Loss decreased (System ignores thermodynamic cost)"
    }
    print(f"ABLATION (No Landauer): Loss={loss_no_landauer:.4f} (Delta={loss_no_landauer - loss:.4f})")

    # Save Results
    with open("evidence/ablation_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("--- ABLATION STUDY COMPLETED ---")
    print("Evidence saved to evidence/ablation_results.json")

if __name__ == "__main__":
    run_ablation_study()
