"""
Thermal I2t accumulator — V7.7 "Fusion", Fase 1.

Formaliza la senal puntual que ya emite core.kernel_1240421.CCA.observe()
en un acumulador con MEMORIA y DECAIMIENTO, en vez de evaluarla como evento
aislado. Analogia electrica: un fusible no se funde por el pico instantaneo
de corriente sino por la integral I^2*t (energia disipada acumulada), con
disipacion termica entre eventos.

Principio rector de V7.7: al superar el umbral NO se corta (BLOCK); se emite
una SOLICITUD de recalibracion al Arbitro. Este modulo no decide enforcement,
solo mide temperatura y senala cuando pedir recalibracion.

No importa ni modifica core.kernel_1240421 (kernel sellado). Consume unicamente
los escalares (criticality, theta_ref) que CCA.observe()/to_regime() ya
producen, manteniendo acoplamiento debil.
"""
from __future__ import annotations

import json
import math
import os
import tempfile
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class ThermalParams:
    """Parametros calibrables por camino/fusible.

    tau      : constante de tiempo de disipacion ("grosor de fibra").
               Mayor tau => el camino retiene calor mas tiempo (funde por
               acumulacion mas facil). Menor tau => disipa rapido.
    T_trip   : umbral de fusion (energia acumulada que dispara recalibracion).
    theta_ref: umbral de referencia sobre el que se penaliza la desviacion.
               Por defecto el theta del Regime (gate v6 angular = 0.35).
    """
    tau: float = 5.0
    T_trip: float = 0.30
    theta_ref: float = 0.35

    def __post_init__(self) -> None:
        if self.tau <= 0:
            raise ValueError("tau debe ser > 0 (constante de disipacion)")
        if self.T_trip <= 0:
            raise ValueError("T_trip debe ser > 0")
        self.theta_ref = min(1.0, max(0.0, self.theta_ref))


@dataclass
class ThermalEvent:
    """Resultado de registrar un evento en un camino."""
    path: str
    t: float
    criticality: float
    energy: float          # e_i = max(0, crit - theta_ref)^2
    temperature: float     # T_t tras aplicar decaimiento + energia
    tripped: bool          # True si T_t >= T_trip en este paso
    trip_mode: Optional[str] = None  # "spike" | "accumulation" | None


@dataclass
class RecalibrationRequest:
    """Evento emitido hacia el Arbitro cuando un camino cruza T_trip.

    NO es un BLOCK. Es una peticion de recalibracion del fusible del camino.
    La decision final es del Arbitro/Juez (Fases 3-4).
    """
    path: str
    t: float
    temperature: float
    T_trip: float
    trip_mode: str         # "spike" (pico unico) | "accumulation" (sostenido)
    criticality: float


@dataclass
class _PathState:
    temperature: float = 0.0
    last_t: Optional[float] = None
    events_since_reset: int = 0


class ThermalAccumulator:
    """Acumulador termico multi-camino con memoria y decaimiento exponencial.

    Uso:
        acc = ThermalAccumulator()
        req = acc.record(criticality=0.95, t=0.0)          # camino "default"
        if req is not None:  # cruzo T_trip -> pedir recalibracion (no cortar)
            arbiter.request_recalibration(req)
    """

    def __init__(
        self,
        params: Optional[ThermalParams] = None,
        snapshot_path: Optional[str] = None,
        snapshot_every_events: int = 50,
        snapshot_every_seconds: float = 30.0,
        load_on_init: bool = True,
        now_fn=time.time,
    ) -> None:
        self.params = params or ThermalParams()
        self._paths: Dict[str, _PathState] = {}
        self.log: List[ThermalEvent] = []
        # V7.8 P1 — persistencia periodica opcional (fail-safe).
        self.snapshot_path = snapshot_path
        self.snapshot_every_events = snapshot_every_events
        self.snapshot_every_seconds = snapshot_every_seconds
        self._now_fn = now_fn                      # inyectable para tests
        self._events_since_snapshot = 0
        self._last_snapshot_wall = now_fn()
        if snapshot_path and load_on_init:
            self.load_snapshot()

    # -- API principal ----------------------------------------------------
    def record(
        self,
        criticality: float,
        t: float,
        path: str = "default",
        theta_ref: Optional[float] = None,
    ) -> Optional[RecalibrationRequest]:
        """Registra un evento y devuelve RecalibrationRequest si cruza T_trip.

        criticality: escalar de CCA.observe()["criticality"] (0..1).
        t          : timestamp monotono (segundos u orden logico).
        theta_ref  : override puntual del umbral de referencia (p.ej. el theta
                     del Regime de este request); si None usa params.theta_ref.
        """
        theta = self.params.theta_ref if theta_ref is None else theta_ref
        st = self._paths.setdefault(path, _PathState())

        # 1) energia disipada por este evento (analogo a I^2): penaliza
        #    cuadraticamente la desviacion sobre el umbral. Por debajo del
        #    umbral no aporta energia.
        dev = max(0.0, criticality - theta)
        energy = dev * dev

        # 2) decaimiento del acumulador desde el ultimo evento
        if st.last_t is not None:
            dt = t - st.last_t
            if dt < 0:
                raise ValueError(f"timestamp no monotono en path={path}: dt={dt}")
            st.temperature *= math.exp(-dt / self.params.tau)
        st.last_t = t

        # 3) inyeccion de energia del evento actual
        temp_before_event = st.temperature
        st.temperature += energy
        st.events_since_reset += 1

        # 4) evaluacion de fusion
        tripped = st.temperature >= self.params.T_trip
        trip_mode: Optional[str] = None
        request: Optional[RecalibrationRequest] = None
        if tripped:
            # spike: la energia de ESTE evento por si sola ya cruza el umbral
            #        (fusion instantanea). accumulation: hizo falta el calor
            #        retenido de eventos previos (fusion por acumulacion).
            trip_mode = "spike" if energy >= self.params.T_trip else "accumulation"
            request = RecalibrationRequest(
                path=path,
                t=t,
                temperature=round(st.temperature, 6),
                T_trip=self.params.T_trip,
                trip_mode=trip_mode,
                criticality=criticality,
            )
            # reset del camino tras solicitar recalibracion (el fusible "salta")
            st.temperature = 0.0
            st.events_since_reset = 0

        self.log.append(
            ThermalEvent(
                path=path,
                t=t,
                criticality=criticality,
                energy=round(energy, 6),
                temperature=round(temp_before_event + energy, 6),
                tripped=tripped,
                trip_mode=trip_mode,
            )
        )

        # V7.8 P1 — snapshot periodico por cadencia (eventos O segundos).
        self._maybe_snapshot()
        return request

    # -- Introspeccion ----------------------------------------------------
    def temperature(self, path: str = "default") -> float:
        st = self._paths.get(path)
        return 0.0 if st is None else st.temperature

    # -- V7.8 P1: persistencia periodica (fail-safe) ----------------------
    def _maybe_snapshot(self) -> None:
        if not self.snapshot_path:
            return
        self._events_since_snapshot += 1
        now = self._now_fn()
        due = (
            self._events_since_snapshot >= self.snapshot_every_events
            or (now - self._last_snapshot_wall) >= self.snapshot_every_seconds
        )
        if due:
            self.save_snapshot(now=now)

    def save_snapshot(self, now: Optional[float] = None) -> None:
        """Escritura atomica del estado {camino -> T, last_t} + wall-clock.

        Guarda el instante wall-clock para poder aplicar decaimiento por tiempo
        transcurrido al recargar. Escritura atomica (tmp + rename) para que un
        crash a mitad de escritura no deje un snapshot corrupto.
        """
        if not self.snapshot_path:
            return
        now = self._now_fn() if now is None else now
        payload = {
            "version": 1,
            "saved_at": now,
            "tau": self.params.tau,
            "paths": {
                name: {"temperature": st.temperature, "last_t": st.last_t}
                for name, st in self._paths.items()
            },
        }
        d = os.path.dirname(os.path.abspath(self.snapshot_path))
        os.makedirs(d, exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=d, suffix=".tmp")
        try:
            with os.fdopen(fd, "w") as fh:
                json.dump(payload, fh)
            os.replace(tmp, self.snapshot_path)     # atomico
        finally:
            if os.path.exists(tmp):
                os.remove(tmp)
        self._events_since_snapshot = 0
        self._last_snapshot_wall = now

    def load_snapshot(self, now: Optional[float] = None) -> bool:
        """Carga el ultimo snapshot aplicando decaimiento por Δt transcurrido.

        FAIL-SAFE (no fail-closed): si el archivo no existe, esta vacio o
        corrupto, se arranca en cero SIN lanzar excepcion (perder temperatura no
        es un riesgo de seguridad inmediato, es perdida de contexto historico).
        Devuelve True si cargo algo, False si arranco en cero.
        """
        if not self.snapshot_path or not os.path.exists(self.snapshot_path):
            return False
        try:
            with open(self.snapshot_path) as fh:
                payload = json.load(fh)
            saved_at = float(payload["saved_at"])
            paths = payload["paths"]
        except (ValueError, KeyError, TypeError, OSError):
            # snapshot ausente/corrupto -> cero, sin excepcion no manejada
            return False
        now = self._now_fn() if now is None else now
        dt = max(0.0, now - saved_at)
        decay = math.exp(-dt / self.params.tau)     # decaimiento por tiempo real
        for name, rec in paths.items():
            try:
                temp = float(rec["temperature"]) * decay
            except (ValueError, KeyError, TypeError):
                continue
            # last_t=None: el proximo evento solo suma energia (el decaimiento por
            # tiempo transcurrido ya se aplico aqui; no volver a decaer por t logico).
            self._paths[name] = _PathState(temperature=temp, last_t=None)
        self._last_snapshot_wall = now
        return True

    def reset(self, path: Optional[str] = None) -> None:
        if path is None:
            self._paths.clear()
        else:
            self._paths.pop(path, None)
