# tests/test_api_basic.py

from fastapi.testclient import TestClient
from antigravity_wings.api.server import app

def test_root_endpoint():
    client = TestClient(app)
    resp = client.get("/")
    assert resp.status_code == 200
    data = resp.json()
    assert data["service"] == "antigravity_wings"
    assert "/cockpit" in data["endpoints"]

def test_status_endpoint_no_key():
    # En desarrollo (sin AGW_API_KEY seteada), esto debería funcionar o pedir key si está configurado por defecto
    client = TestClient(app)
    resp = client.get("/status")
    # Si settings.api_key es None, devuelve 200. Si está seteado, 401.
    assert resp.status_code in [200, 401]

def test_sessions_endpoint():
    client = TestClient(app)
    resp = client.get("/sessions")
    assert resp.status_code in [200, 401]
    if resp.status_code == 200:
        data = resp.json()
        assert "sessions" in data
