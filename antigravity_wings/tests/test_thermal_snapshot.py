"""
Gate P1 — V7.8 Hardening: snapshot periodico del acumulador termico.

- "Matar" el proceso a mitad de acumulacion y reiniciar recupera el estado
  termico (con decaimiento por tiempo transcurrido) dentro de tolerancia.
- Fail-safe: snapshot ausente o corrupto -> arranca en cero sin excepcion.
- Cadencia automatica: tras M eventos el snapshot existe en disco.
"""
import json
import math
import os

import pytest

from antigravity_wings.thermal import ThermalAccumulator, ThermalParams

PARAMS = ThermalParams(tau=5.0, T_trip=0.30, theta_ref=0.35)


def test_restart_recovers_state_within_tolerance(tmp_path):
    snap = str(tmp_path / "thermal.json")
    # proceso 1: acumula y snapshot (reloj fijo en 1000)
    acc1 = ThermalAccumulator(PARAMS, snapshot_path=snap, now_fn=lambda: 1000.0)
    for i in range(10):
        acc1.record(criticality=0.60, t=float(i))     # e_i=0.0625 por evento
    acc1.save_snapshot(now=1000.0)
    saved_temp = acc1.temperature()
    assert saved_temp > 0.0

    # "kill + restart": proceso 2 carga el snapshot SIN tiempo transcurrido (now=1000)
    acc2 = ThermalAccumulator(PARAMS, snapshot_path=snap, now_fn=lambda: 1000.0)
    recovered = acc2.temperature()
    # sin Δt, el estado recuperado == guardado (dentro de redondeo)
    assert abs(recovered - saved_temp) < 1e-9

    # comparado con un acumulador que NUNCA se reinicio: identico
    acc_never = ThermalAccumulator(PARAMS)
    for i in range(10):
        acc_never.record(criticality=0.60, t=float(i))
    assert abs(recovered - acc_never.temperature()) < 1e-9


def test_reload_applies_decay_for_elapsed_time(tmp_path):
    from antigravity_wings.thermal.accumulator import _PathState
    snap = str(tmp_path / "thermal.json")
    acc1 = ThermalAccumulator(PARAMS, snapshot_path=snap, now_fn=lambda: 1000.0)
    # fijar una temperatura conocida y snapshot en t=1000
    acc1._paths["default"] = _PathState(temperature=0.20, last_t=None)
    acc1.save_snapshot(now=1000.0)

    # recargar tau segundos despues -> decae por exp(-1)
    acc2 = ThermalAccumulator(PARAMS, snapshot_path=snap, load_on_init=False,
                              now_fn=lambda: 1000.0 + PARAMS.tau)
    acc2.load_snapshot(now=1000.0 + PARAMS.tau)
    expected = 0.20 * math.exp(-1.0)
    assert abs(acc2.temperature() - expected) < 1e-6


def test_failsafe_missing_snapshot_starts_at_zero(tmp_path):
    snap = str(tmp_path / "no_existe.json")
    acc = ThermalAccumulator(PARAMS, snapshot_path=snap)   # load_on_init True
    assert acc.temperature() == 0.0                        # sin excepcion


def test_failsafe_corrupt_snapshot_starts_at_zero(tmp_path):
    snap = str(tmp_path / "corrupto.json")
    with open(snap, "w") as fh:
        fh.write("{ esto no es json valido :::")
    acc = ThermalAccumulator(PARAMS, snapshot_path=snap)
    assert acc.load_snapshot() is False
    assert acc.temperature() == 0.0                        # arranca en cero, sin lanzar


def test_auto_snapshot_by_event_cadence(tmp_path):
    snap = str(tmp_path / "auto.json")
    acc = ThermalAccumulator(PARAMS, snapshot_path=snap,
                             snapshot_every_events=5, snapshot_every_seconds=1e9)
    for i in range(5):
        acc.record(criticality=0.60, t=float(i))
    assert os.path.exists(snap)                            # se escribio por cadencia
    with open(snap) as fh:
        payload = json.load(fh)
    assert "paths" in payload and "saved_at" in payload


def test_no_snapshot_path_is_noop(tmp_path):
    acc = ThermalAccumulator(PARAMS)      # sin snapshot_path
    for i in range(100):
        acc.record(criticality=0.60, t=float(i))
    # no revienta y no persiste nada; comportamiento identico a V7.7
    assert acc.temperature() >= 0.0
