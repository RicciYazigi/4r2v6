# tests/test_resilience_hardened.py

import pytest
from antigravity_wings.orchestration.session_manager import SessionManager
from antigravity_wings.resilience.circuit_breaker import CircuitBreaker, CircuitBreakerConfig, CircuitOpenError
import time

def test_session_manager_persistence(tmp_path):
    root = tmp_path / "sessions"
    sm = SessionManager(root)
    cid = "client_alpha"
    s1 = sm.create_session(cid)
    sid = s1.session_id
    
    # Simular reinicio creando otro manager sobre el mismo root
    sm2 = SessionManager(root)
    s2 = sm2.get_session(sid)
    
    assert s2 is not None
    assert s2.client_id == cid
    assert s2.base_dir == s1.base_dir
    assert s2.profile_dir.exists()

def test_circuit_breaker_logic():
    config = CircuitBreakerConfig(failure_threshold=2, recovery_timeout_sec=0.1, max_latency_sec=0.05)
    cb = CircuitBreaker("test", config)
    
    def fail_func():
        raise ValueError("f")
        
    def slow_func():
        time.sleep(0.1)
        return "ok"

    # 1. Fallo por excepción
    with pytest.raises(ValueError):
        cb.call(fail_func)
    
    # 2. Fallo por latencia
    with pytest.raises(Exception): # CircuitBreaker trata latencia alta como fallo genérico si no devuelve error específico
        cb.call(slow_func)
        
    # 3. Circuito debería estar abierto ahora (2 fallos)
    with pytest.raises(CircuitOpenError):
        cb.call(lambda: "hi")

    # 4. Esperar recuperación
    time.sleep(0.2)
    assert cb.call(lambda: "back") == "back"
    assert cb.metrics.state == "closed"

def test_session_manager_list_filter(tmp_path):
    sm = SessionManager(tmp_path)
    sm.create_session("A")
    sm.create_session("B")
    sm.create_session("A")
    
    assert len(sm.list_sessions("A")) == 2
    assert len(sm.list_sessions("B")) == 1
    assert len(sm.list_sessions()) == 3

if __name__ == "__main__":
    import sys
    sys.exit(pytest.main([__file__]))
