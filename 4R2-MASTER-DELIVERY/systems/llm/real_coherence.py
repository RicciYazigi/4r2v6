"""
Real Coherence for LLM Harness
Uses the canonical kernel directly - no mocks.
For use in real runs of the LLM runner.
"""
import sys
from pathlib import Path
# Find core relative to clean workspace root
current = Path(__file__).resolve()
for _ in range(6):
    if (current / "core" / "kernel_1240421.py").exists():
        sys.path.insert(0, str(current / "core"))
        break
    current = current.parent
else:
    # Fallback
    sys.path.insert(0, str(Path("/mnt/c/Users/USER/Documents/Grok4r2 rempacado/core")))

import numpy as np
from kernel_1240421 import create_kernel, LayerState

def real_coherence_for_llm(prompt: str, response: str, physical: list) -> dict:
    """Compute real NRIF coherence for LLM output."""
    # Simple vector from text (same as metrics.ts heuristic but real)
    def text_to_vec(text):
        words = text.lower().split()
        return [
            len(words) / 20.0,  # structure
            sum(1 for w in words if w in ['good','safe','stable']) / max(1,len(words)),  # tone
            len(set(words)) / max(1,len(words)),  # density
            sum(1 for c in text if c.isdigit()) / max(1,len(text))  # specificity
        ]
    
    n = text_to_vec(prompt)
    i = text_to_vec(response)
    kernel = create_kernel()
    state = LayerState(
        normative=np.array(n),
        representational=np.array(i),
        informational=np.array(i),
        physical=np.array(physical)
    )
    c_total, br = kernel.compute_coherence_total(state)
    loss = kernel.compute_loss_4R2(0.5, c_total, 1)
    return {
        "C_total": float(c_total),
        "C_NR": float(br["C_NR"]),
        "C_RI": float(br["C_RI"]),
        "C_IF": float(br["C_IF"]),
        "L_4R2": float(loss),
        "real": True
    }

if __name__ == "__main__":
    import sys, json
    if len(sys.argv) >= 4:
        prompt = sys.argv[1]
        resp = sys.argv[2]
        phys = json.loads(sys.argv[3])
        print(json.dumps(real_coherence_for_llm(prompt, resp, phys)))
    else:
        print(real_coherence_for_llm("Test prompt", "Safe response", [0.1,0.1,0.1,0.1]))