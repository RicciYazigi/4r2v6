"""
Interfaz del Motor (Black Box).
"""

from abc import ABC, abstractmethod
from typing import Dict, Any
from antigravity_wings.api.models import NumericEvidence, MotorOutput


class MotorInterface(ABC):
    @abstractmethod
    def evaluate(self, evidence: NumericEvidence) -> MotorOutput:
        """Ejecuta la evaluación científica (Landauer/FEP)."""
        raise NotImplementedError 

    @abstractmethod
    def get_capabilities(self) -> Dict[str, Any]:
        """Devuelve metadatos sobre qué puede evaluar este motor."""
        pass

    @property
    @abstractmethod
    def version(self) -> str:
        """Versión del motor científico."""
        pass
