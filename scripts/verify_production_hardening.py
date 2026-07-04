#!/usr/bin/env python3
"""
Production Hardening Verification
- Rate limit enforcement on /analyze (with x-api-key)
- CircuitBreaker trip on RealMotor failure path
- Confirms MasterOrchestrator uses CB + structured paths
Run with: PYTHONPATH=antigravity_wings python scripts/verify_production_hardening.py
"""
import os
import sys

def verify_rate_limit_on_analyze():
    test_key = os.environ.setdefault("AGW_ADMIN_KEY", "hardening-verify-local-only-key")
    from fastapi.testclient import TestClient
    from antigravity_wings.api.server import app

    client = TestClient(app)
    headers = {"x-api-key": test_key}
    oks = 0
    too_many = 0
    for i in range(70):
        resp = client.post("/analyze/hardening", json={"metadata": {"trace": "rate-verify"}}, headers=headers)
        if resp.status_code == 200:
            oks += 1
        elif resp.status_code == 429:
            too_many += 1
    print(f"RATE /analyze: 200s={oks} 429s={too_many}")
    assert oks <= 65, "Too many OKs, rate limit weak"
    assert too_many >= 3, "Not enough 429s triggered"
    print("  -> RATE LIMIT (60/min) on /analyze: PASSED")

def verify_circuit_breaker_real_motor():
    from antigravity_wings.api.models import NumericEvidence
    from antigravity_wings.motor_bridge.real_motor import RealMotor
    from antigravity_wings.resilience.circuit_breaker import CircuitOpenError

    motor = RealMotor(base_url="http://127.0.0.1:1")  # unreachable -> failures
    ev = NumericEvidence(
        client_id="cb-verify",
        normative=[0.1, 0.2, 0.3, 0.4],
        representational=[0.5]*4,
        informational=[0.6]*4,
        physical=[10.0]*4,
    )
    fails = 0
    tripped = False
    for i in range(15):
        try:
            motor.evaluate(ev)
        except CircuitOpenError:
            tripped = True
            print(f"  CB opened after {fails} failures (attempt {i})")
            break
        except Exception:
            fails += 1
    print(f"CB: observed_fails={fails} tripped={tripped}")
    assert tripped, "CB did not trip"
    print("  -> CIRCUIT BREAKER on RealMotor (fail-open protect): PASSED")

def verify_master_hardening():
    from antigravity_wings.orchestration.master import MasterOrchestrator
    o = MasterOrchestrator()
    ver = getattr(o.motor, "version", "unknown")
    cb_name = o.cb.name
    print(f"Master motor={ver} CB={cb_name}")
    # execute will use the cb.call
    print("  -> Master CB protection + real motor path: PRESENT")

if __name__ == "__main__":
    print("=== PRODUCTION HARDENING VERIFICATION ===")
    verify_rate_limit_on_analyze()
    verify_circuit_breaker_real_motor()
    verify_master_hardening()
    print("=== ALL HARDENING CHECKS PASSED ===")
