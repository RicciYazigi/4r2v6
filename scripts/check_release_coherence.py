#!/usr/bin/env python3
"""Release-coherence gate. Exits 1 if the repo tells more than one story.
Enforces (the exact class of inconsistency flagged in external due diligence,
e.g. pyproject=4.0.0 vs README=v6.1.0):
  1. pyproject.toml [project].version  == four_r2.__version__
  2. core/kernel_1240421.py docstring declares four_r2.KERNEL_MATH_VERSION
  3. README.md mentions the package release version
  4. requires-python floor is >= 3.10 (matches README requirement)
Run locally: python scripts/check_release_coherence.py
CI runs this on every push.
"""
from __future__ import annotations
import pathlib
import re
import sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from four_r2 import KERNEL_MATH_VERSION, __version__  # noqa: E402
failures: list[str] = []
def check(name: str, ok: bool, detail: str) -> None:
    print(f"[{'OK ' if ok else 'FAIL'}] {name}: {detail}")
    if not ok:
        failures.append(name)
pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
m = re.search(r'^version\s*=\s*"([^"]+)"', pyproject, re.M)
pyver = m.group(1) if m else "<missing>"
check("pyproject==package", pyver == __version__, f"pyproject={pyver} four_r2={__version__}")
m = re.search(r'requires-python\s*=\s*">=([\d.]+)"', pyproject)
floor = m.group(1) if m else "<missing>"
check("python-floor>=3.10", floor not in ("<missing>",) and tuple(map(int, floor.split("."))) >= (3, 10),
      f"requires-python >= {floor}")
kernel_head = (ROOT / "core" / "kernel_1240421.py").read_text(encoding="utf-8")[:2000]
check("kernel-math-version", f"v{KERNEL_MATH_VERSION}" in kernel_head,
      f"core/kernel_1240421.py declares v{KERNEL_MATH_VERSION}")
readme = (ROOT / "README.md").read_text(encoding="utf-8", errors="replace")
check("readme-release", __version__ in readme, f"README.md mentions {__version__}")
if failures:
    print(f"\nRELEASE COHERENCE: FAIL ({', '.join(failures)})")
    sys.exit(1)
print("\nRELEASE COHERENCE: PASS — one version story across the repo.")
