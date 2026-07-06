"""Single source of truth for release versioning.
RELEASE (package) version vs KERNEL MATH version are deliberately distinct:
the kernel math (core/kernel_v6.py + core/kernel_1240421.py) is frozen at
6.1.0, evidence-sealed (E1/E2/E3/E4) and parity-protected across 4 replicas.
Bumping the math version requires a new ADR + regenerated, re-sealed evidence.
The package version tracks the product layer (SDK, sidecar, packaging, docs).
scripts/check_release_coherence.py enforces that pyproject.toml, README and
this file agree. CI fails on drift.
"""
__version__ = "7.0.0"
KERNEL_MATH_VERSION = "6.1.0"
