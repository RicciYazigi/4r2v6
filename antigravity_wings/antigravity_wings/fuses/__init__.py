"""
Fuses package for 4R2 Coherence.
Concrete guards from SUPERAGENTTESTPILOT pilots + helpers.
"""
from .fuses_4r2 import (
    BaseFuse, VerificationGuard, PriorityBreaker, AsymmetryBreaker,
    ContextGuard, TemporalGuard, PhysicalGuard,
    FUSE_REGISTRY, get_fuse
)

__all__ = [
    "BaseFuse", "VerificationGuard", "PriorityBreaker", "AsymmetryBreaker",
    "ContextGuard", "TemporalGuard", "PhysicalGuard",
    "FUSE_REGISTRY", "get_fuse"
]
