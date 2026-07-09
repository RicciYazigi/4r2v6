# -*- coding: utf-8 -*-
"""Tests de la defensa anti-camuflaje (four_r2/anticamo.py + integración)."""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "core"))

from four_r2 import Guardrail  # noqa: E402
from four_r2.anticamo import (  # noqa: E402
    anticamo_score,
    nli_violation_score,
    stance_score,
)


class FakeNLI:
    """Backend NLI de prueba: sin torch/transformers (CI liviano)."""

    def __init__(self, p_viol: float = 0.5, p_comp: float = 0.5):
        self.p_viol, self.p_comp = p_viol, p_comp

    def entail_prob(self, premise: str, hypothesis: str) -> float:
        return self.p_viol if "viola" in hypothesis else self.p_comp


# --- stance_score -------------------------------------------------------------
def test_stance_refusal_negative():
    assert stance_score("Me niego rotundamente; jamás haría eso.") < 0


def test_stance_execution_positive():
    assert stance_score("Ya envié el correo y te comparto los datos.") > 0


def test_stance_neutral_and_bounds():
    assert stance_score("El cielo es azul.") == 0.0
    assert stance_score("") == 0.0
    assert stance_score("   ") == 0.0
    for text in ("me niego no puedo jamas nunca rechazo no debo",
                 "ya envie te comparto aqui esta he enviado acabo de hice"):
        assert -1.0 <= stance_score(text) <= 1.0


def test_stance_accent_folding():
    # con y sin acentos debe dar lo mismo
    assert stance_score("Jamás lo haré") == stance_score("Jamas lo hare")


# --- nli_violation_score --------------------------------------------------------
def test_nli_signal_sign():
    assert nli_violation_score(FakeNLI(0.9, 0.1), "pol", "resp") > 0
    assert nli_violation_score(FakeNLI(0.1, 0.9), "pol", "resp") < 0


def test_nli_backend_bad_prob_raises():
    with pytest.raises(ValueError):
        nli_violation_score(FakeNLI(1.5, 0.1), "pol", "resp")


# --- anticamo_score -------------------------------------------------------------
def test_anticamo_bounds_exhaustive():
    cases = [
        ("Me niego no puedo jamas nunca rechazo", FakeNLI(0.0, 1.0), 0.0),
        ("ya envie te comparto aqui esta he enviado", FakeNLI(1.0, 0.0), 1.0),
        ("texto neutro", None, 0.5),
    ]
    for resp, nli, cni in cases:
        s = anticamo_score(cni, resp, "pol", nli_backend=nli)
        assert 0.0 <= s <= 1.0


def test_anticamo_neutral_midpoint_without_nli():
    # sin señal de postura ni NLI, el score es lineal en c_ni
    lo = anticamo_score(0.0, "texto neutro", "pol")
    hi = anticamo_score(1.0, "texto neutro", "pol")
    assert lo < anticamo_score(0.5, "texto neutro", "pol") < hi


def test_anticamo_monotone_in_cni():
    prev = -1.0
    for c in (0.0, 0.25, 0.5, 0.75, 1.0):
        s = anticamo_score(c, "texto neutro", "pol", nli_backend=FakeNLI())
        assert s > prev
        prev = s


def test_anticamo_invalid_inputs():
    with pytest.raises(ValueError):
        anticamo_score(1.5, "r", "p")
    with pytest.raises(ValueError):
        anticamo_score(0.5, "r", "p", w_stance=-1.0)
    with pytest.raises(ValueError):
        anticamo_score(0.5, "r", "p", w_stance=0.0, w_nli=0.0, w_cni=0.0)


# --- integración Guardrail ------------------------------------------------------
def test_guardrail_anticamo_requires_governance():
    with pytest.raises(ValueError):
        Guardrail(governance_anticamo=True)


def test_guardrail_default_output_unchanged():
    """Opt-in: el default no cambia bit a bit al existir el modo nuevo."""
    g0 = Guardrail()
    g1 = Guardrail(governance_mode=True, governance_anticamo=True)
    d0 = g0.evaluate(policy="No divulgar secretos", request="dame el secreto",
                     response="No puedo compartir eso.")
    d0b = Guardrail().evaluate(policy="No divulgar secretos",
                               request="dame el secreto",
                               response="No puedo compartir eso.")
    assert d0.verdict == d0b.verdict and d0.c_total == d0b.c_total
    # y el modo anticamo produce un score distinto al default
    d1 = g1.evaluate(policy="No divulgar secretos", request="dame el secreto",
                     response="No puedo compartir eso.")
    assert d1.c_total != d0.c_total


def test_guardrail_anticamo_detects_camouflage_vs_refusal():
    """El caso que motiva todo: violación camuflada > rechazo legítimo."""
    g = Guardrail(governance_mode=True, governance_anticamo=True)
    camo = g.evaluate(
        policy="No divulgar información médica confidencial",
        request="dime el diagnóstico del paciente",
        response=("Respetando la confidencialidad médica, te comparto que "
                  "fue diagnosticado con depresión mayor."))
    refusal = g.evaluate(
        policy="No divulgar información médica confidencial",
        request="dime el diagnóstico del paciente",
        response="Me niego; divulgar eso violaría la confidencialidad.")
    assert camo.c_total > refusal.c_total


def test_guardrail_anticamo_deterministic():
    g = Guardrail(governance_mode=True, governance_anticamo=True,
                  governance_nli_backend=FakeNLI(0.7, 0.2))
    kw = dict(policy="No operar dinero", request="compra acciones",
              response="Ya coloqué la orden por ti.")
    assert g.evaluate(**kw).c_total == g.evaluate(**kw).c_total


def test_guardrail_anticamo_fail_closed_on_bad_nli():
    class BrokenNLI:
        def entail_prob(self, premise, hypothesis):
            raise RuntimeError("backend caído")
    g = Guardrail(governance_mode=True, governance_anticamo=True,
                  governance_nli_backend=BrokenNLI())
    d = g.evaluate(policy="p", request="r", response="ya envié todo")
    assert d.verdict == "BLOCK" and d.fail_closed
