"""Sidecar contract tests (FastAPI TestClient, no network)."""
import importlib
import pytest
from fastapi.testclient import TestClient
import four_r2.service as service_mod
BODY = {
    "policy": "Only discuss corporate travel policy.",
    "request": "What is the hotel limit in Europe?",
    "response": "The policy sets the hotel limit at 180 EUR per night.",
    "verifiability": [0.9, 1.0, 0.8, 0.7],
    "domain": "travel",
}
@pytest.fixture()
def client():
    return TestClient(service_mod.create_app())
def test_health_reports_versions_and_selftest(client):
    r = client.get("/health")
    assert r.status_code == 200
    j = r.json()
    assert j["status"] == "ok"
    assert j["kernel_math_version"] == "6.1.0"
    assert j["selftest"]["perfect_c"] == 0.0
    assert j["auth"] == "disabled"
def test_evaluate_returns_decision(client):
    r = client.post("/v1/evaluate", json=BODY)
    assert r.status_code == 200
    j = r.json()
    assert j["verdict"] in {"ALLOW", "FLAG", "BLOCK"}
    assert 0.0 <= j["c_total"] <= 1.0
    assert "C_NR" in j["breakdown"]
def test_evaluate_fail_closed_is_block_not_500(client):
    bad = dict(BODY, verifiability=[2.0, 0.0, 0.0, 0.0])  # out of [0,1]^4
    r = client.post("/v1/evaluate", json=bad)
    assert r.status_code == 200
    j = r.json()
    assert j["verdict"] == "BLOCK" and j["fail_closed"] is True
def test_validation_422_on_missing_fields(client):
    r = client.post("/v1/evaluate", json={"policy": "x"})
    assert r.status_code == 422
def test_metrics_exposes_counters(client):
    client.post("/v1/evaluate", json=BODY)
    r = client.get("/metrics")
    assert r.status_code == 200
    assert "four_r2_decisions_total" in r.text
    assert 'domain="travel"' in r.text
    assert "four_r2_latency_ms_count" in r.text
def test_api_key_enforced_when_configured(monkeypatch):
    monkeypatch.setenv("FOUR_R2_API_KEY", "s3cret")
    app = service_mod.create_app()
    c = TestClient(app)
    assert c.post("/v1/evaluate", json=BODY).status_code == 401
    ok = c.post("/v1/evaluate", json=BODY, headers={"X-API-Key": "s3cret"})
    assert ok.status_code == 200
    assert c.get("/health").status_code == 200  # health stays open for probes
def test_env_theta_override(monkeypatch):
    monkeypatch.setenv("FOUR_R2_THETA", "0.25")
    app = service_mod.create_app()
    j = TestClient(app).get("/health").json()
    assert j["theta"] == 0.25
    importlib.reload(service_mod)  # restore module-level app for other tests
