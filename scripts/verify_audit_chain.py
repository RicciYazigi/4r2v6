#!/usr/bin/env python3
"""G6 — Verificador standalone de la cadena de auditoría 4R2.
Un tercero (auditor, comprador, regulador) lo corre sobre el log EXPORTADO,
sin acceso al sistema vivo:  python3 scripts/verify_audit_chain.py <log.jsonl>
Exit 0 = íntegra ; Exit 1 = alterada (imprime seq del punto de ruptura)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "antigravity_wings"))
from antigravity_wings.audit.hash_chain import verify_chain

def main():
    if len(sys.argv) != 2:
        print("uso: verify_audit_chain.py <ruta_log.jsonl>"); sys.exit(2)
    r = verify_chain(sys.argv[1])
    print(f"[audit-chain] ok={r['ok']} entries={r['entries']} broken_at={r['broken_at']} :: {r['reason']}")
    sys.exit(0 if r["ok"] else 1)

if __name__ == "__main__":
    main()
