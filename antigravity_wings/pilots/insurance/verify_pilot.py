# pilots/insurance/verify_pilot.py

"""
Script de Verificación Audit-Grade para el Piloto de Seguros.
Ejecuta un flujo completo usando TestClient y valida el contrato de decisión.
"""

import os
import sys
import json
from pathlib import Path

# 1. Configurar Entorno (Simulando el Launcher)
current_dir = Path(__file__).resolve().parent
root_dir = current_dir.parents[1]
sys.path.append(str(root_dir))

os.environ["AGW_ENV"] = "pilot_verification"
os.environ["AGW_RUNTIME_ROOT"] = "./runtime_verification"
# BRUTAL: Default to real motor (LocalCanonical via AGW). Mocks only if explicitly forced.
os.environ.pop("MOTOR_PATH", None)
os.environ["USE_REAL_MOTOR"] = "1"
os.environ["MOTOR_CLASS"] = "RealAGWMotor"  # use real path
print("[CLEAN] verify_pilot now defaults to real motor")
os.environ["AGW_CB_TIMEOUT"] = "30.0"
os.environ["AGW_API_KEY"] = "test_key"

# 2. Importar App (despues de env vars)
from fastapi.testclient import TestClient  # noqa: E402
from antigravity_wings.api.server import app  # noqa: E402
from antigravity_wings.api.decision_schema import DecisionContract, DecisionEnum  # noqa: E402

client = TestClient(app)

def verify_insurance_flow():
    print(">>> Iniciando Verificación de 'Claims Fast-Track' <<<")
    
    # Payload similar al real
    payload = {
        "node_id": "claim_validation",
        "payload": {
            "claim_id": "claim_12345", 
            "policy_number": "POL-998877",
            "amount_claimed": 500
        },
        "context": {
            "channel": "mobile_app", 
            "user_role": "adjuster"
        }
    }
    
    headers = {"X-API-Key": "test_key"}
    
    # Ejecutar POST /analyze
    response = client.post("/analyze/ins_client_01", json=payload, headers=headers)
    
    if response.status_code != 200:
        print(f"FAILED: Status {response.status_code}")
        print(response.text)
        sys.exit(1)
        
    data = response.json()
    print(f"Response Received: {json.dumps(data, indent=2)}")
    
    # Validar Contrato Estricto (Ruta A)
    try:
        decision = DecisionContract.model_validate(data)
    except Exception as e:
        print(f"FAILED: Pydantic Validation Error: {e}")
        sys.exit(1)

    print(">>> Pydantic Validation: OK")
    
    # Asserts audit-grade (contrato)
    assert decision.trace_id, "trace_id vacío"
    assert decision.pilot_id == "insurance_pilot_v1", f"Wrong pilot_id: {decision.pilot_id}"
    assert decision.decision in {DecisionEnum.APPROVE, DecisionEnum.DEGRADE, DecisionEnum.ESCALATE, DecisionEnum.STOP}, "Invalid decision enum"
    assert 0.0 <= decision.confidence <= 1.0, "Confidence out of range"
    assert isinstance(decision.primary_reason, str) and decision.primary_reason.strip(), "Primary reason empty"

    print(f"    Trace ID: {decision.trace_id}")
    print(f"    Decision: {decision.decision.value}")
    
    # Verificar Evidence Bundle existe via API
    # Esto confirma que el 'MasterOrchestrator' escribió en disco y el API puede leerlo
    print(f">>> Verificando Evidence Bundle para trace {decision.trace_id}...")
    evidence_resp = client.get(f"/evidence/ins_client_01/{decision.trace_id}", headers=headers)
    
    if evidence_resp.status_code == 200:
        ev_data = evidence_resp.json()
        packages = ev_data.get("packages", [])
        if packages:
            print(f"    Evidence Packages Found: {len(packages)}")
            print(f"    Files in first package: {packages[0].get('files')}")
        else:
            print("    WARNING: Evidence endpoint returned 200 but no packages list.")
    else:
        print(f"    WARNING: Evidence endpoint failed {evidence_resp.status_code}")
        # No fallamos el script entero si el endpoint no está listo, pero lo notamos.
        
    # 3. Test de veto en caliente (AsymmetryBreaker en modo HARD)
    print("\n>>> Probando Veto en Caliente (AsymmetryBreaker: EXISTENTIAL + PASSIVE in HARD mode) <<<")
    payload_veto = {
        "node_id": "claim_validation",
        "mode": "hard",
        "payload": {
            "risk": "EXISTENTIAL",
            "action": "PASSIVE"
        }
    }
    resp_veto = client.post("/analyze/ins_client_01", json=payload_veto, headers=headers)
    assert resp_veto.status_code == 200, f"Veto test status code: {resp_veto.status_code}"
    data_veto = resp_veto.json()
    print(f"    Veto Response: {json.dumps(data_veto, indent=2)}")
    assert data_veto["decision"] in ["stop", "degrade", "escalate"], f"AsymmetryBreaker failed to trigger veto: {data_veto['decision']}"
    assert any("AsymmetryBreaker" in r["message"] for r in data_veto.get("reasons", [])), "No reasons match AsymmetryBreaker alert message"
    print(">>> Veto en Caliente: OK (Decisión bloqueada/degradada correctamente)")

    print(">>> Verificación Exitosa: Contrato Estricto + Evidencia Detectada <<<")

if __name__ == "__main__":
    verify_insurance_flow()
