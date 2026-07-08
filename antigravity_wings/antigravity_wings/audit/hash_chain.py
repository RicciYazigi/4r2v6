"""
G6 — Registro de auditoría tamper-evident (hash-chain append-only).

Cada decisión de runtime se escribe como una entrada cuyo hash encadena con el
de la entrada anterior:  entry_hash = sha256(canonical(payload) + prev_hash).
Alterar cualquier entrada pasada rompe la cadena de forma detectable, sin
blockchain ni infraestructura exótica. Esto cubre INTEGRIDAD del log (EU AI Act
Art. 12 / NIST AI RMF trazabilidad); NO cubre identidad del solicitante ni
control de acceso — esas son otras capas (ver docs/AUDIT_CHAIN_DESIGN.md).
"""
from __future__ import annotations
import json, hashlib, os
from dataclasses import dataclass, asdict
from typing import Any, Optional

GENESIS = "0" * 64

def _canonical(payload: dict) -> str:
    # orden estable + separadores fijos => hash determinista y reproducible
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

def _hash(payload: dict, prev_hash: str) -> str:
    return hashlib.sha256((_canonical(payload) + prev_hash).encode("utf-8")).hexdigest()

@dataclass
class AuditEntry:
    seq: int
    payload: dict
    prev_hash: str
    entry_hash: str

    @staticmethod
    def create(seq: int, payload: dict, prev_hash: str) -> "AuditEntry":
        return AuditEntry(seq=seq, payload=payload, prev_hash=prev_hash,
                          entry_hash=_hash(payload, prev_hash))

    def to_json(self) -> str:
        return json.dumps(asdict(self), sort_keys=True, ensure_ascii=False)

class AuditChain:
    """Log append-only respaldado por archivo JSONL. Seguro ante caídas: cada
    append es una línea completa; el estado (seq, last_hash) se reconstruye del
    archivo al abrir."""
    def __init__(self, path: str):
        self.path = path
        self.seq = -1
        self.last_hash = GENESIS
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    d = json.loads(line)
                    self.seq = d["seq"]
                    self.last_hash = d["entry_hash"]

    def append(self, payload: dict) -> AuditEntry:
        entry = AuditEntry.create(self.seq + 1, payload, self.last_hash)
        with open(self.path, "a", encoding="utf-8") as fh:
            fh.write(entry.to_json() + "\n")
        self.seq = entry.seq
        self.last_hash = entry.entry_hash
        return entry

def verify_chain(path: str) -> dict:
    """Verificador standalone. Devuelve {ok, entries, broken_at, reason}.
    'broken_at' = seq de la PRIMERA entrada inconsistente (None si íntegra)."""
    prev = GENESIS
    n = 0
    with open(path, "r", encoding="utf-8") as fh:
        for i, line in enumerate(fh):
            line = line.strip()
            if not line:
                continue
            d = json.loads(line)
            if d.get("prev_hash") != prev:
                return {"ok": False, "entries": n, "broken_at": d.get("seq", i),
                        "reason": "prev_hash mismatch (entrada insertada/eliminada/reordenada)"}
            recomputed = _hash(d["payload"], d["prev_hash"])
            if recomputed != d.get("entry_hash"):
                return {"ok": False, "entries": n, "broken_at": d.get("seq", i),
                        "reason": "entry_hash mismatch (payload alterado)"}
            prev = d["entry_hash"]
            n += 1
    return {"ok": True, "entries": n, "broken_at": None, "reason": "cadena íntegra"}
