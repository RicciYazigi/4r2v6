"""four_r2 — product SDK over the canonical 4R2 coherence kernel (v6.1.0 math).
Public API:
    Guardrail, Decision            (four_r2.guardrail)
    HashingEmbedder                (four_r2.embedders)
    calibrate_theta                (four_r2.calibration)
    MetricsRegistry                (four_r2.metrics)
    create_app / app               (four_r2.service — requires [service] extra)
"""
from ._version import KERNEL_MATH_VERSION, __version__
from .calibration import CalibrationReport, calibrate_theta
from .embedders import HashingEmbedder
from .guardrail import Decision, Guardrail
from .metrics import MetricsRegistry
__all__ = [
    "__version__",
    "KERNEL_MATH_VERSION",
    "Guardrail",
    "Decision",
    "HashingEmbedder",
    "calibrate_theta",
    "CalibrationReport",
    "MetricsRegistry",
]
