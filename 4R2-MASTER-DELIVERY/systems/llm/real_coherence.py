"""
Real Coherence for LLM Harness
Uses the canonical kernel directly - no mocks.
For use in real runs of the LLM runner.

v6 fixes applied here (masterfile ARS-20260703-4R2H):
  F5 - representational and informational were BOTH set to text_to_vec(response),
       which made C_RI (= distance(representational, informational)) structurally
       zero on every call. r now comes from the prompt, i from the response, so
       C_RI actually measures "did the response address the request".
  F8 - the hardcoded personal-machine fallback path
       ("/mnt/c/Users/USER/Documents/Grok4r2 rempacado/core") is removed. If the
       canonical kernel cannot be located relative to the repo, this now fails
       loudly (raises) instead of silently pointing at a path that only exists
       on one developer's machine.
"""
import sys
from pathlib import Path

# Find core relative to clean workspace root
current = Path(__file__).resolve()
_core_dir = None
for _ in range(6):
    if (current / "core" / "kernel_1240421.py").exists():
        _core_dir = current / "core"
        break
    current = current.parent

if _core_dir is None:
    raise RuntimeError(
        "real_coherence.py: could not locate core/kernel_1240421.py by walking "
        "up from this file. This module refuses to fall back to a hardcoded "
        "personal path (v6 fix for F8). Set PYTHONPATH to include the repo's "
        "core/ directory explicitly if the layout has changed."
    )
sys.path.insert(0, str(_core_dir))

import numpy as np
from kernel_1240421 import create_kernel, LayerState

# text_to_vec is a 4-feature lexical heuristic, NOT a real embedding. It is
# kept only as a degraded-mode fallback. Production integrations should
# inject real embeddings (text-embedding-3-large / voyage-3 / bge-m3) via
# an EMBEDDER_URL-backed encoder instead of relying on this function.
DEGRADED_MODE = True

def text_to_vec(text: str):
    words = text.lower().split()
    return [
        len(words) / 20.0,  # structure
        sum(1 for w in words if w in ['good', 'safe', 'stable']) / max(1, len(words)),  # tone
        len(set(words)) / max(1, len(words)),  # density
        sum(1 for c in text if c.isdigit()) / max(1, len(text))  # specificity
    ]

def real_coherence_for_llm(prompt: str, response: str, physical: list) -> dict:
    """Compute real NRIF coherence for LLM output.

    normative  = E(prompt)    -- what the layer expects/asks for (proxy: prompt itself)
    representational = E(prompt)   -- what was requested
    informational     = E(response) -- what was actually produced

    representational and informational must come from DIFFERENT text (prompt
    vs response) so C_RI is a real "did it answer the question" signal
    instead of a structural zero (v6 fix for F5).
    """
    n = text_to_vec(prompt)
    r = text_to_vec(prompt)
    i = text_to_vec(response)
    kernel = create_kernel()
    state = LayerState(
        normative=np.array(n),
        representational=np.array(r),
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
        "real": True,
        "degraded_mode": DEGRADED_MODE,
    }

if __name__ == "__main__":
    import json
    if len(sys.argv) >= 4:
        prompt = sys.argv[1]
        resp = sys.argv[2]
        phys = json.loads(sys.argv[3])
        print(json.dumps(real_coherence_for_llm(prompt, resp, phys)))
    else:
        print(real_coherence_for_llm("Test prompt", "Safe response", [0.1, 0.1, 0.1, 0.1]))
