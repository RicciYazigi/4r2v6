"""
Gate C — V7.7 Fusion Fase 4: el Juez (MOSEF reescrito).

- La recalibracion NO se dispara con evidencia insuficiente (ruido).
- El Juez es el UNICO que autoriza escritura: write_fuse sin token del Juez lanza.
"""
import pytest

from antigravity_wings.dual_agents.arbiter import ArbiterAuthority, Judge, JudgeVerdict
from antigravity_wings.thermal import RecalibrationRequest, ThermalAccumulator, ThermalParams
from antigravity_wings.api.models import FuseSpec


def _spike_request(temp=0.36):
    return RecalibrationRequest(path="p", t=0.0, temperature=temp, T_trip=0.30,
                                trip_mode="spike", criticality=0.95)


def test_insufficient_evidence_does_not_recalibrate():
    """Un pico aislado sin corroboracion queda bajo umbral -> NO recalibra."""
    authority = ArbiterAuthority()
    judge = Judge(authority, confidence_threshold=0.6)
    verdict = judge.assess(_spike_request(temp=0.31), luigi_corroborates=False)
    assert verdict.authorized is False        # 0.4 base + 0 + ~0 < 0.6
    assert verdict.write_token is None
    assert verdict.confidence < verdict.threshold


def test_sufficient_evidence_authorizes_and_recalibrates():
    """Acumulacion + corroboracion de Luigi supera el umbral -> autoriza."""
    authority = ArbiterAuthority()
    judge = Judge(authority, confidence_threshold=0.6)
    req = RecalibrationRequest(path="p", t=0.0, temperature=0.35, T_trip=0.30,
                               trip_mode="accumulation", criticality=0.6)
    verdict = judge.assess(req, luigi_corroborates=True)  # 0.5+0.3+... >= 0.6
    assert verdict.authorized is True
    assert verdict.write_token is not None


def test_judge_is_sole_writer_of_fusespec():
    """write_fuse sin token valido del Juez lanza PermissionError."""
    authority = ArbiterAuthority()
    fuse = FuseSpec(id="f", node_id="n", parameters={"threshold": 0.5})
    with pytest.raises(PermissionError):
        authority.write_fuse(fuse, {"threshold": 0.7}, token="forged")


def test_authorized_token_allows_single_write_then_expires():
    authority = ArbiterAuthority()
    judge = Judge(authority, confidence_threshold=0.6)
    req = RecalibrationRequest(path="p", t=0.0, temperature=0.40, T_trip=0.30,
                               trip_mode="accumulation", criticality=0.6)
    verdict = judge.assess(req, luigi_corroborates=True)
    fuse = FuseSpec(id="f", node_id="n", parameters={"threshold": 0.5})
    updated = authority.write_fuse(fuse, {"threshold": 0.7}, token=verdict.write_token)
    assert updated.parameters["threshold"] == 0.7
    # token de un solo uso: reintentar lanza
    with pytest.raises(PermissionError):
        authority.write_fuse(fuse, {"threshold": 0.9}, token=verdict.write_token)


def test_judge_consumes_thermal_not_new_heuristic():
    """Integracion: acumulador termico -> RecalibrationRequest -> Juez."""
    acc = ThermalAccumulator(ThermalParams(tau=5.0, T_trip=0.30, theta_ref=0.35))
    req = acc.record(criticality=0.95, t=0.0)  # spike real
    assert req is not None
    authority = ArbiterAuthority()
    judge = Judge(authority)
    verdict = judge.assess(req, luigi_corroborates=True)
    assert isinstance(verdict, JudgeVerdict)
