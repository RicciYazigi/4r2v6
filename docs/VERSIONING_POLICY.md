# VERSIONING POLICY (v7.0.0)
Two version lines, one story, machine-enforced.
## Package (release) version — `four_r2.__version__`
SemVer over the product layer: SDK, sidecar, packaging, docs, benchmarks.
- MAJOR: breaking SDK/HTTP contract change.
- MINOR: new capability, backward compatible.
- PATCH: fixes/docs.
Declared in exactly one place: `four_r2/_version.py`. `pyproject.toml` and
README must match — enforced by `scripts/check_release_coherence.py` (CI gate
+ `tests/test_release_coherence.py`).
## Kernel math version — `four_r2.KERNEL_MATH_VERSION` (currently 6.1.0)
Frozen. The math (core/kernel_v6.py + core/kernel_1240421.py) is:
1. evidence-sealed (E1/E2/E3/E4 hashes chain to this exact code), and
2. parity-protected (4 byte-identical replicas must collapse to one SHA-256 in CI).
Changing kernel math requires, in order: a new ADR + implementation →
regenerated + re-sealed evidence (all E-series) → replica sync → bump of
KERNEL_MATH_VERSION → spec update. Anything less is drift, and drift is what
this project's history (inverted polarity, blind-spot weights, doc drift)
teaches us to gate against mechanically, not by discipline alone.
## Why v7.0.0 does not bump the kernel to 7.x
Because nothing in the math changed. Pretending otherwise would invalidate
the evidence chain's meaning. v7.0.0 = product maturity release. NOTE: the
opt-in `core/frontier_v7.py` layer-decoupling defenses (H(x), JS camouflage,
Shannon OOD, hardened negation) are ADDITIVE and do not alter the frozen
kernel math; see docs/FRONTIER_REPORT.md and ADR-0008.
