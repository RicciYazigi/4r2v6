# pilots/insurance/mocks.py

"""
Componentes Mock (simulados) para el Piloto de Seguros 'Claims Fast-Track'.
Simulan el entorno de un sistema de reclamos de autos real.
"""

from typing import List, Dict, Any
import datetime

from antigravity_wings.observation.registry import DataSource
from antigravity_wings.motor_bridge.interface import MotorInterface
from antigravity_wings.api.models import NumericEvidence, MotorOutput

# --------------------------------------------------------------------------
# 1. Mock DataSource: Simula la API de Siniestros
# --------------------------------------------------------------------------

class InsuranceClaimSource(DataSource):
    """
    Simula recibir un paquete de reclamo con:
    - ID del siniestro
    - Texto del relato (versión conductor)
    - OCR del reporte policial
    - Metadata de imágenes (URLs, fechas, EXIF simulado)
    """

    def __init__(self, claim_id: str, scenario: str = "clear_approval"):
        self._claim_id = claim_id
        self._scenario = scenario  # clear_approval, fraud_metadata, conflict_story, total_loss

    @property
    def name(self) -> str:
        return "insurance_api_v1"

    def collect(self) -> List[Dict[str, Any]]:
        # Generar datos sintéticos basados en el escenario
        base_data = {
            "claim_id": self._claim_id,
            "policy_id": "POL-998877",
            "incident_date": (datetime.datetime.now() - datetime.timedelta(days=1)).isoformat(),
            "customer_story": "I was stopped at a red light and was rear-ended by a blue sedan.",
            "images": [
                {"url": "http://img/bumper.jpg", "exif_date": (datetime.datetime.now() - datetime.timedelta(days=1)).isoformat()},
                {"url": "http://img/scene.jpg", "exif_date": (datetime.datetime.now() - datetime.timedelta(days=1)).isoformat()}
            ],
            "police_report_ocr": "V1 stopped at signal. V2 failed to stop. Rear-end collision. No injuries."
        }

        if self._scenario == "fraud_metadata":
            # EXIF date is from 2020
            base_data["images"][0]["exif_date"] = "2020-01-01T10:00:00"
            base_data["images"][1]["exif_date"] = "2020-01-01T10:05:00"
        
        elif self._scenario == "conflict_story":
            base_data["customer_story"] = "I hit a pole while parking."
            base_data["police_report_ocr"] = "Vehicle found abandoned in ditch. Suspicion of DUI."

        elif self._scenario == "total_loss":
            base_data["estimated_damage_usd"] = 25000
            base_data["vehicle_value_usd"] = 20000 

        return [base_data]

# --------------------------------------------------------------------------
# 2. Mock Motor: Simula el modelo de "Computer Vision + NLP"
# --------------------------------------------------------------------------

class ClaimsVisionMotor(MotorInterface):
    """
    Simula un motor de IA que:
    1. Analiza imágenes (daño visual)
    2. Compara texto (consistencia narrativa)
    3. Retorna un score de riesgo (0.0 = seguro, 1.0 = fraude/complejo)
    """
    
    def evaluate(self, evidence: NumericEvidence) -> MotorOutput:
        # En un caso real, el NumericEvidence tendría vectores.
        # Aquí "engañamos" un poco leyendo la metadata cruda si se pasó (esto es una simplificación del mock)
        # O asumimos que el NumericTranslator ya extrajo ciertas features.
        
        # Simulamos lógica basada en "features" (que en realidad inferimos del ID o azar para la demo)
        
        risk_score = 0.1 # Default safe
        reasons = []

        # Detectamos "corrupción" simulada en features (NaNs)
        if evidence.feature_vector and any(x == -999 for x in evidence.feature_vector):
             # Simular fallo interno si hay valores centinela
             pass 

        # Lógica simple para el Mock basada en "features" imaginarios
        # Feature 0: Metadata Consistency (1=bad, 0=good)
        # Feature 1: Narrative Consistency (1=bad, 0=good)
        # Feature 2: Damage Ratio (Cost/Value)
        
        features = evidence.feature_vector or [0, 0, 0.1]
        
        meta_score = features[0]
        narrative_score = features[1]
        damage_ratio = features[2]

        if meta_score > 0.5:
            risk_score += 0.4
            reasons.append("metadata_mismatch_detected")
        
        if narrative_score > 0.5:
            risk_score += 0.4
            reasons.append("narrative_conflict_detected")
            
        if damage_ratio > 0.8:
            risk_score += 0.3
            reasons.append("high_damage_ratio")

        return MotorOutput(
            client_id=evidence.client_id,
            scores={"risk_score": min(risk_score, 1.0)},
            ranges={"low_risk": [0, 0.3], "medium_risk": [0.3, 0.7], "high_risk": [0.7, 1.0]},
            config_blob={
                "motor_version": "v2.1-vision",
                "detected_flags": reasons
            }
        )
