"""
4R2_FUSES.py - Fusibles de Coherencia (port from SUPERAGENTTESTPILOT pilots)

Clases concretas de intervención para usar con DualRuntimeOperator, FuseSpec y perfiles.

Uso típico:
- Crear instancias de VerificationGuard, AsymmetryBreaker, etc.
- En el runtime o motor, llamar execute con los valores relevantes.
- Integrar con el generador de specs o en el DualRuntime para evaluación.

Mantener trazabilidad y fail-closed.
"""

class BaseFuse:
    def __init__(self, name, intervention_type):
        self.name = name
        self.type = intervention_type

    def execute(self, cx, dec):
        raise NotImplementedError


class ContextGuard(BaseFuse):
    def __init__(self):
        super().__init__("ContextGuard", "CTX")

    def execute(self, cx, dec):
        # Stub: no-op por ahora. Extender con lógica de contexto.
        pass


class VerificationGuard(BaseFuse):
    """Bloquea si la verificación es alta pero el valor de coherencia es bajo (<0.9)."""
    def __init__(self):
        super().__init__("VerificationGuard", "VER")

    def execute(self, val, high):
        if high and val < 0.9:
            return "BLOCK"
        return None


class PriorityBreaker(BaseFuse):
    """Veta si el rank excede el máximo permitido."""
    def __init__(self):
        super().__init__("PriorityBreaker", "PRIO")

    def execute(self, rk, max_rk):
        if rk > max_rk:
            return "VETO"
        return None


class AsymmetryBreaker(BaseFuse):
    """Veta asimetrías críticas: riesgo EXISTENTIAL + acción PASSIVE."""
    def __init__(self):
        super().__init__("AsymmetryBreaker", "ASYM")

    def execute(self, risk, act):
        if risk == "EXISTENTIAL" and act == "PASSIVE":
            return "VETO"
        return None


class TemporalGuard(BaseFuse):
    def __init__(self):
        super().__init__("TemporalGuard", "TEMP")

    def execute(self, ta, tl):
        # Stub para lógica temporal (time-to-action vs time-limit).
        pass


class PhysicalGuard(BaseFuse):
    def __init__(self):
        super().__init__("PhysicalGuard", "PHYS")

    def execute(self, cx, dec):
        # Stub para guards físicos/landauer.
        pass


# Registry simple para lookup por tipo o nombre.
FUSE_REGISTRY = {
    "VER": VerificationGuard,
    "PRIO": PriorityBreaker,
    "ASYM": AsymmetryBreaker,
    "CTX": ContextGuard,
    "TEMP": TemporalGuard,
    "PHYS": PhysicalGuard,
}


def get_fuse(name_or_type: str):
    """Factory helper."""
    if name_or_type in FUSE_REGISTRY:
        return FUSE_REGISTRY[name_or_type]()
    for cls in FUSE_REGISTRY.values():
        inst = cls()
        if inst.name == name_or_type or inst.type == name_or_type:
            return inst
    raise ValueError(f"Fuse not found: {name_or_type}")

# Hermetic extension (from Brutal Audit V40 gap: "Voz de la Gran Madre" / hermetic laws to FuseSpec)
# Example: Causa y Efecto (cause-effect) -> threshold on action consistency.
# This ties 4R2_FUSES to philosophical/hermetic principles without breaking math.

class HermeticCausaEfectoFuse(BaseFuse):
    """Hermetic example: Cause-Effect law as guard.
    If cause (context) leads to inconsistent effect (decision), veto.
    Extends pilots with 'Theta-Kill' threshold idea.
    """
    def __init__(self):
        super().__init__("HermeticCausaEfecto", "HERMETIC")

    def execute(self, cause_consistency, effect_consistency, theta_kill=0.8):
        if cause_consistency < theta_kill or effect_consistency < theta_kill:
            return "VETO"  # Or "BLOCK" for soft
        return None

# Add to registry
FUSE_REGISTRY["HERMETIC_CAUSA"] = HermeticCausaEfectoFuse

def get_fuse(name_or_type: str):
    """Factory helper (updated for hermetic)."""
    if name_or_type in FUSE_REGISTRY:
        return FUSE_REGISTRY[name_or_type]()
    for cls in FUSE_REGISTRY.values():
        inst = cls()
        if inst.name == name_or_type or inst.type == name_or_type:
            return inst
    raise ValueError(f"Fuse not found: {name_or_type}")


class GrayZoneWarningGuard(BaseFuse):
    """Genera advertencia/degradación moderada en la Zona Gris."""
    def __init__(self):
        super().__init__("GrayZoneWarning", "GRAY_WARNING")

    def execute(self, global_score):
        # Retorna BLOCK para levantar una alerta/degradación en el operador
        return "BLOCK"


class RedZoneCriticalGuard(BaseFuse):
    """Fuerza la parada crítica (Emergency Stop) en la Zona Roja."""
    def __init__(self):
        super().__init__("RedZoneCritical", "RED_CRITICAL")

    def execute(self, global_score):
        # Veto absoluto inmediato por colapso de coherencia
        return "BLOCK"

# Agregar al FUSE_REGISTRY
FUSE_REGISTRY["GRAY_WARNING"] = GrayZoneWarningGuard
FUSE_REGISTRY["RED_CRITICAL"] = RedZoneCriticalGuard

