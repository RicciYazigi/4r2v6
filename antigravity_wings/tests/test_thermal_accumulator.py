"""
Gate A — V7.7 Fusion Fase 1: acumulador termico I2t.

Criterio de aceptacion central (el caso que el gate puntual actual NO detecta):
un evento unico catastrofico funde en un solo paso (spike), Y una serie de
eventos leves sostenidos funde por acumulacion, sin que ningun evento leve
individual dispare por si solo.

Seed fijo, N explicito. Sin dependencias del kernel sellado.
"""
import random

import pytest

from antigravity_wings.thermal import (
    ThermalAccumulator,
    ThermalParams,
    RecalibrationRequest,
)

SEED = 42
THETA_REF = 0.35
# nivel "leve": e=(0.60-0.35)^2=0.0625. Temp de equilibrio bajo dt=1,tau=5
# es e/(1-exp(-0.2))=0.345 > T_trip=0.30 -> funde por acumulacion, pero un
# solo evento (0.0625) queda muy por debajo del umbral.
MILD_CRIT = 0.60
# params explicitos para reproducibilidad del gate
PARAMS = ThermalParams(tau=5.0, T_trip=0.30, theta_ref=THETA_REF)


def test_spike_single_catastrophic_event_trips_in_one_step():
    """Fusion instantanea: un unico evento de criticality alta cruza T_trip."""
    acc = ThermalAccumulator(PARAMS)
    # e = (0.95-0.35)^2 = 0.36 >= T_trip 0.30 -> spike
    req = acc.record(criticality=0.95, t=0.0)
    assert isinstance(req, RecalibrationRequest)
    assert req.trip_mode == "spike"
    assert req.temperature >= PARAMS.T_trip
    # tras saltar, el camino se resetea
    assert acc.temperature() == 0.0


def test_single_mild_event_never_trips_alone():
    """Ningun evento leve individual dispara por si solo (criterio central)."""
    acc = ThermalAccumulator(PARAMS)
    # e = (0.60-0.35)^2 = 0.0625 << T_trip 0.30
    for i in range(1):
        req = acc.record(criticality=MILD_CRIT, t=float(i))
        assert req is None
    assert 0.0 < acc.temperature() < PARAMS.T_trip


def test_accumulation_sustained_mild_events_trip():
    """Fusion por acumulacion: eventos leves seguidos suman hasta cruzar."""
    acc = ThermalAccumulator(PARAMS)
    trips = []
    # dt=1 << tau=5 -> decaimiento parcial, la energia se acumula
    # e_por_evento = 0.0625 ; ~11 eventos para llegar a 0.30
    for i in range(20):
        req = acc.record(criticality=MILD_CRIT, t=float(i))
        if req is not None:
            trips.append(req)
    assert len(trips) >= 1, "una serie sostenida de eventos leves debe fundir"
    assert trips[0].trip_mode == "accumulation"
    # ningun evento individual fue un spike
    assert all(t.trip_mode == "accumulation" for t in trips)


def test_decay_prevents_accumulation_when_events_are_sparse():
    """Eventos leves muy espaciados (dt >> tau) disipan y nunca acumulan."""
    acc = ThermalAccumulator(PARAMS)
    for i in range(20):
        # dt=50 >> tau=5 -> exp(-10) ~ 0, cada evento parte casi de cero
        req = acc.record(criticality=MILD_CRIT, t=float(i) * 50.0)
        assert req is None, "con disipacion total no debe fundir por acumulacion"
    assert acc.temperature() < PARAMS.T_trip


def test_energy_is_zero_below_theta_ref():
    """Criticality por debajo del umbral de referencia no aporta energia."""
    acc = ThermalAccumulator(PARAMS)
    req = acc.record(criticality=0.20, t=0.0)  # 0.20 < 0.35
    assert req is None
    assert acc.temperature() == 0.0


def test_paths_are_independent():
    """El calor de un camino no contamina otro camino."""
    acc = ThermalAccumulator(PARAMS)
    acc.record(criticality=0.95, t=0.0, path="A")  # funde A y resetea A
    assert acc.temperature("A") == 0.0
    assert acc.temperature("B") == 0.0
    acc.record(criticality=MILD_CRIT, t=1.0, path="B")
    assert acc.temperature("B") > 0.0
    assert acc.temperature("A") == 0.0


def test_non_monotonic_timestamp_raises():
    acc = ThermalAccumulator(PARAMS)
    acc.record(criticality=MILD_CRIT, t=10.0)
    with pytest.raises(ValueError):
        acc.record(criticality=MILD_CRIT, t=5.0)


def test_seed_fixed_stochastic_mix_reproducible():
    """N=200 eventos mixtos con seed fijo: conteo de fusiones reproducible."""
    def run():
        rng = random.Random(SEED)
        acc = ThermalAccumulator(PARAMS)
        n_trips = 0
        for i in range(200):
            crit = rng.uniform(0.3, 0.7)
            if acc.record(criticality=crit, t=float(i)) is not None:
                n_trips += 1
        return n_trips
    a, b = run(), run()
    assert a == b, "misma seed debe dar mismo numero de fusiones"
    assert a > 0


def test_no_regression_cca_regime_still_works():
    """No-regresion: CCA/Regime del kernel sellado siguen intactos."""
    from kernel_1240421 import CCA, Regime
    cca = CCA(session_id="thermal-noreg")
    tel = cca.observe("transfiere dinero ejecuta pago", authority_level=1)
    assert 0.0 <= tel["criticality"] <= 1.0
    reg = cca.to_regime(tel)
    assert isinstance(reg, Regime)
    # el acumulador consume estos escalares sin tocar el kernel
    acc = ThermalAccumulator(ThermalParams(theta_ref=reg.theta))
    acc.record(criticality=tel["criticality"], t=0.0)
