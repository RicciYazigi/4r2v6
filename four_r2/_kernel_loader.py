"""Locates and imports the canonical kernel WITHOUT duplicating it.
Replica-parity policy (CI): the kernel exists as byte-identical copies whose
SHA-256 must collapse to a single hash. This loader therefore never copies
kernel code; it puts the canonical `core/` directory on sys.path and imports
`kernel_1240421` (which itself imports `kernel_v6`, the mathematical SSOT).
Resolution order:
  1. `kernel_1240421` already importable (caller set PYTHONPATH=core).
  2. Repo layout: <this file>/../../core
  3. Installed layout: the `core` package location (pip install -e . / wheel).
Fail-closed: if the kernel cannot be located, ImportError propagates; the
Guardrail facade converts any construction/evaluation error into BLOCK.
"""
from __future__ import annotations
import importlib
import importlib.util
import pathlib
import sys
def load_kernel_module():
    try:
        return importlib.import_module("kernel_1240421")
    except ImportError:
        pass
    candidates = []
    repo_core = pathlib.Path(__file__).resolve().parent.parent / "core"
    candidates.append(repo_core)
    spec = importlib.util.find_spec("core")
    if spec is not None and spec.submodule_search_locations:
        for loc in spec.submodule_search_locations:
            candidates.append(pathlib.Path(loc))
    for cand in candidates:
        if (cand / "kernel_1240421.py").exists():
            p = str(cand)
            if p not in sys.path:
                sys.path.insert(0, p)
            return importlib.import_module("kernel_1240421")
    raise ImportError(
        "canonical kernel (core/kernel_1240421.py) not found; "
        "install with `pip install -e .` from the repo root or set PYTHONPATH=core"
    )
