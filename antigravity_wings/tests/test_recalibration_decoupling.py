"""
Gate C — V7.7 Fusion Fase 5: desacople logico del hot path.

El hot path solo ENCOLA (O(1)) sin correr el arbitraje; el procesamiento ocurre
fuera de linea via drain(). Se verifica que encolar NO ejecuta el handler y que
el hot path (encolar) es mucho mas barato que la arbitracion completa.

NOTA DE ALCANCE (decision abierta -> v8): no se usan hilos/procesos ni cola
distribuida. La infraestructura async real queda como semilla de v8; aqui se
prueba el desacople sin arriesgar el hot path sincrono actual.
"""
import time

from antigravity_wings.dual_agents.arbiter import RecalibrationQueue
from antigravity_wings.thermal import ThermalAccumulator, ThermalParams


def test_enqueue_does_not_run_handler():
    q = RecalibrationQueue()
    ran = {"count": 0}

    def handler(req):
        ran["count"] += 1
        return "processed"

    acc = ThermalAccumulator(ThermalParams(tau=5.0, T_trip=0.30, theta_ref=0.35))
    req = acc.record(criticality=0.95, t=0.0)
    q.enqueue(req)
    assert len(q) == 1
    assert ran["count"] == 0            # encolar NO corre el arbitraje

    results = q.drain(handler)          # procesamiento fuera del hot path
    assert ran["count"] == 1
    assert results == ["processed"]
    assert len(q) == 0


def test_hot_path_enqueue_is_cheaper_than_full_processing():
    """El coste de encolar (hot path) << coste del handler pesado (background)."""
    q = RecalibrationQueue()

    def heavy_handler(req):
        time.sleep(0.01)                # simula arbitraje/Juez fuera de linea
        return True

    acc = ThermalAccumulator(ThermalParams(tau=5.0, T_trip=0.30, theta_ref=0.35))
    req = acc.record(criticality=0.95, t=0.0)

    t0 = time.perf_counter()
    q.enqueue(req)
    enqueue_dt = time.perf_counter() - t0

    t1 = time.perf_counter()
    q.drain(heavy_handler)
    drain_dt = time.perf_counter() - t1

    # el hot path no paga el coste del arbitraje
    assert enqueue_dt < drain_dt
    assert enqueue_dt < 0.005
