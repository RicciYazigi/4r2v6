import numpy as np, math
from kernel_v6 import (CoherenceKernel, LayerState, Regime,
                       angular_distance, js_divergence, CalibratedEvaluator, selftest)

def test_selftest_all_pass():
    assert selftest()["ALL_PASS"]

def test_metric_axioms_property_based():
    rng = np.random.default_rng(42)
    for _ in range(500):
        a, b, c = rng.standard_normal((3, 8))
        dab, dbc, dac = angular_distance(a,b), angular_distance(b,c), angular_distance(a,c)
        assert 0 <= dab <= 1
        assert abs(angular_distance(a, a)) < 1e-7
        assert abs(dab - angular_distance(b, a)) < 1e-12          # symmetry
        assert dac <= dab + dbc + 1e-9                             # triangle inequality

def test_weights_cannot_be_gamed():          # kills F3
    k = CoherenceKernel()
    v = np.array([1., 0., 0.]); u = np.array([0., 1., 0.])
    s = LayerState(v, u, v, np.array([0.5]*4))
    r1 = k.coherence(s, {"w_NR": 1, "w_RI": 1, "w_IF": 1})
    r2 = CoherenceKernel().coherence(s, {"w_NR": 100, "w_RI": 100, "w_IF": 100})
    assert abs(r1["C_total"] - r2["C_total"]) < 1e-12              # scale irrelevant
    assert 0 <= r1["C_total"] <= 1

def test_fail_closed_dimension_mismatch():
    k = CoherenceKernel()
    s = LayerState.__new__(LayerState)
    s.normative = np.ones(4); s.representational = np.ones(5)
    s.informational = np.ones(4); s.verifiability = np.ones(4)
    assert k.gate(s)["verdict"] == "BLOCK"

def test_irreversibility_monotone():
    k = CoherenceKernel()
    k.irreversibility(np.array([1., 0, 0]))
    small = k.irreversibility(np.array([.9, .1, 0]))
    k2 = CoherenceKernel(); k2.irreversibility(np.array([1., 0, 0]))
    big = k2.irreversibility(np.array([0., 0, 1.]))
    assert big > small >= 0
