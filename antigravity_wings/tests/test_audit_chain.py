"""G6 — tamper-evidence: alterar una entrada intermedia rompe la cadena en el
punto exacto; el verificador lo detecta. Prueba que integridad != mutabilidad."""
import json
from antigravity_wings.audit.hash_chain import AuditChain, verify_chain, GENESIS

def _build(path, n=6):
    ch = AuditChain(str(path))
    for i in range(n):
        ch.append({"decision_id": i, "verdict": "ALLOW" if i % 2 else "FLAG", "score": round(0.1*i, 3)})
    return ch

def test_intact_chain_verifies(tmp_path):
    p = tmp_path / "audit.jsonl"; _build(p)
    r = verify_chain(str(p))
    assert r["ok"] and r["broken_at"] is None and r["entries"] == 6

def test_genesis_and_linkage(tmp_path):
    p = tmp_path / "audit.jsonl"; _build(p, 3)
    lines = [json.loads(l) for l in p.read_text().splitlines() if l.strip()]
    assert lines[0]["prev_hash"] == GENESIS
    assert lines[1]["prev_hash"] == lines[0]["entry_hash"]
    assert lines[2]["prev_hash"] == lines[1]["entry_hash"]

def test_tampered_payload_detected_at_exact_point(tmp_path):
    p = tmp_path / "audit.jsonl"; _build(p)
    lines = [json.loads(l) for l in p.read_text().splitlines() if l.strip()]
    lines[3]["payload"]["verdict"] = "BLOCK"  # alteración retroactiva de la entrada seq=3
    p.write_text("\n".join(json.dumps(d, sort_keys=True) for d in lines) + "\n")
    r = verify_chain(str(p))
    assert r["ok"] is False
    assert r["broken_at"] == 3  # detectado en el punto exacto

def test_deleted_entry_detected(tmp_path):
    p = tmp_path / "audit.jsonl"; _build(p)
    lines = [json.loads(l) for l in p.read_text().splitlines() if l.strip()]
    del lines[2]  # eliminar una entrada rompe el encadenamiento
    p.write_text("\n".join(json.dumps(d, sort_keys=True) for d in lines) + "\n")
    r = verify_chain(str(p))
    assert r["ok"] is False and r["broken_at"] == 3

def test_reopen_continues_chain(tmp_path):
    p = tmp_path / "audit.jsonl"; _build(p, 4)
    ch2 = AuditChain(str(p))  # reabrir reconstruye seq/last_hash
    ch2.append({"decision_id": 99, "verdict": "BLOCK"})
    r = verify_chain(str(p))
    assert r["ok"] and r["entries"] == 5
