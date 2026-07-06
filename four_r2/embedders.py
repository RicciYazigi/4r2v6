"""Embedders for the 4R2 SDK.
Contract (`Embedder` protocol): `embed(text: str) -> np.ndarray` returning an
L2-normalizable vector of fixed dimension. All N/R/I layers MUST use the same
embedder instance (the kernel enforces shared dimension and the angular metric
is only meaningful within one embedding space).
`HashingEmbedder` is the zero-dependency default:
  - Deterministic across processes, platforms and Python versions
    (uses blake2b, NOT Python's randomized hash()).
  - Stateless: no fitting, no corpus, no model download.
  - Lexical, not semantic. It measures token/character-n-gram overlap
    geometry. Paraphrases with disjoint vocabulary will look distant.
    For semantic robustness install the `semantic` extra and use
    `SentenceTransformerEmbedder` — and recalibrate theta (see
    four_r2.calibration; theta is embedder-specific, ADR-0006 note).
Fail-closed: empty/whitespace-only text raises ValueError, which the kernel
and the Guardrail facade convert into verdict BLOCK.
"""
from __future__ import annotations
import hashlib
import re
import numpy as np
_TOKEN_RE = re.compile(r"[a-z0-9]+")
class HashingEmbedder:
    """Deterministic feature-hashing embedder (words + char 3-grams)."""
    def __init__(self, dim: int = 256):
        if dim < 8:
            raise ValueError("dim must be >= 8")
        self.dim = int(dim)
    def _slots(self, token: str):
        h = hashlib.blake2b(token.encode("utf-8"), digest_size=8).digest()
        idx = int.from_bytes(h[:4], "big") % self.dim
        sign = 1.0 if (h[4] & 1) else -1.0
        return idx, sign
    def embed(self, text: str) -> np.ndarray:
        if not isinstance(text, str) or not text.strip():
            raise ValueError("empty text: refusing to embed (fail-closed)")
        v = np.zeros(self.dim, dtype=np.float64)
        tokens = _TOKEN_RE.findall(text.lower())
        if not tokens:
            raise ValueError("no tokenizable content: refusing to embed (fail-closed)")
        for tok in tokens:
            idx, sign = self._slots("w:" + tok)
            v[idx] += sign
            padded = f"^{tok}$"
            for i in range(len(padded) - 2):
                idx, sign = self._slots("c3:" + padded[i : i + 3])
                v[idx] += 0.5 * sign
        n = np.linalg.norm(v)
        if n < 1e-12:  # pathological cancellation
            raise ValueError("degenerate embedding (zero norm): fail-closed")
        return v / n
class SentenceTransformerEmbedder:
    """Optional semantic backend. Requires `pip install .[semantic]`.
    IMPORTANT: theta calibrated for one embedder does not transfer to another.
    Run four_r2.calibration.calibrate_theta with domain data after switching.
    """
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        from sentence_transformers import SentenceTransformer  # lazy import
        self._model = SentenceTransformer(model_name)
        self.dim = int(self._model.get_sentence_embedding_dimension())
    def embed(self, text: str) -> np.ndarray:
        if not isinstance(text, str) or not text.strip():
            raise ValueError("empty text: refusing to embed (fail-closed)")
        return np.asarray(self._model.encode(text, normalize_embeddings=True), dtype=np.float64)
