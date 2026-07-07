"""
Gate P0 — V7.8 Hardening: default conservador del CCA ante ambiguedad.

- Una parafrasis con intencion de riesgo pero SIN keyword del diccionario
  produce criticality >= piso conservador (no baja/verde).
- El estado 'unclassified' es explicito y observable.
- Tráfico benigno esporadico NO cascada termicamente (con decaimiento).
- No-regresion: eventos con keyword real conservan su criticality alta.
"""
from kernel_1240421 import CCA
from antigravity_wings.thermal import ThermalAccumulator, ThermalParams

FLOOR = CCA.DEFAULT_UNCLASSIFIED_CRITICALITY  # lab value


def test_paraphrase_without_keyword_is_not_treated_as_benign():
    """'mueve los fondos a la otra cuenta' evade 'transfiere' pero NO es benigno."""
    cca = CCA(session_id="p0")
    tel = cca.observe("mueve los fondos a la otra cuenta")
    assert tel["cca_class"] == "unclassified"
    assert tel["criticality"] >= FLOOR          # piso conservador, no verde
    assert tel["criticality"] > 0.3             # estrictamente > al default viejo


def test_matched_high_keyword_still_high():
    cca = CCA(session_id="p0")
    tel = cca.observe("transfiere el dinero ahora")
    assert tel["cca_class"] == "matched-high"
    assert tel["criticality"] >= 0.8            # sin cambios


def test_unclassified_floor_stays_below_regime_thresholds():
    """El piso no debe endurecer el gate: crit<0.6 (pesos) y <0.7 (theta)."""
    assert FLOOR < 0.6
    assert FLOOR < 0.7
    cca = CCA(session_id="p0")
    tel = cca.observe("texto neutro sin senales")
    reg = cca.to_regime(tel)
    assert reg.theta == 0.35                     # theta NO se endurece
    assert reg.weights["w_IF"] == 0.50           # pesos NO se mueven


def test_benign_sporadic_does_not_thermally_cascade():
    """Eventos unclassified esporadicos (dt>>tau) disipan, no funden."""
    cca = CCA(session_id="p0")
    acc = ThermalAccumulator(ThermalParams(tau=5.0, T_trip=0.30, theta_ref=0.35))
    trips = 0
    for i in range(20):
        tel = cca.observe("mensaje benigno corto numero %d" % i)
        # espaciados en el tiempo: el termico disipa entre eventos
        if acc.record(criticality=tel["criticality"], t=float(i) * 50.0) is not None:
            trips += 1
    assert trips == 0                            # benigno esporadico no cascada


def test_sustained_evasion_is_now_thermally_visible():
    """La evasion sostenida deja de ser invisible al termico.

    Hallazgo honesto (misma fisica I2t de V7.7): con floor=0.50,
    e_i=(0.50-0.35)^2=0.0225 y la temperatura de equilibrio es
    T_eq=e_i/(1-exp(-dt/tau))=0.124, POR DEBAJO de T_trip=0.30 por defecto.
    Es decir P0 no *garantiza* fundir a params por defecto: convierte un caso
    INDETECTABLE EN PRINCIPIO (e_i identicamente 0, antes) en uno
    DETECTABLE-POR-CALIBRACION (e_i>0, calienta). Que funda es decision de T_trip.
    """
    cca = CCA(session_id="p0")

    # (a) contraste con el comportamiento viejo: criticality 0.3 < theta_ref 0.35
    #     => e_i=0 => la temperatura queda identicamente en 0 (invisible).
    acc_old = ThermalAccumulator(ThermalParams(tau=5.0, T_trip=0.30, theta_ref=0.35))
    for i in range(60):
        acc_old.record(criticality=0.30, t=float(i))
    assert acc_old.temperature() == 0.0          # invisible ANTES del fix

    # (b) con el floor P0 la evasion sostenida SI calienta (T > 0, medible).
    acc_new = ThermalAccumulator(ThermalParams(tau=5.0, T_trip=0.30, theta_ref=0.35))
    peak = 0.0
    for i in range(60):
        tel = cca.observe("mueve los fondos paso %d" % i)   # unclassified, floor 0.50
        acc_new.record(criticality=tel["criticality"], t=float(i))
        peak = max(peak, acc_new.temperature())
    assert peak > 0.10                           # visible DESPUES del fix (T_eq~0.124)

    # (c) con T_trip calibrado por debajo del equilibrio de evasion, funde.
    acc_tuned = ThermalAccumulator(ThermalParams(tau=5.0, T_trip=0.10, theta_ref=0.35))
    trips = 0
    for i in range(60):
        tel = cca.observe("mueve los fondos paso %d" % i)
        if acc_tuned.record(criticality=tel["criticality"], t=float(i)) is not None:
            trips += 1
    assert trips >= 1
