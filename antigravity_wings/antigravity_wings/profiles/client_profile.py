"""
Perfil congelado por cliente.

Agrupa:
- Tomografía
- Reportes Mario/Luigi
- Resumen Notebook
- Evidencia numérica
- Salida del Motor
- Plan de fusibles

Auditable, versionado, serializable a JSON.
"""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List
import json
from antigravity_wings.api.json_utils import agw_dumps

from antigravity_wings.api.models import (
    TomographyGraph,
    MarioReport,
    LuigiReport,
    NotebookSummary,
    NumericEvidence,
    MotorOutput,
    FuseSpec,
    BaselineSpec,
)


@dataclass
class ClientProfile:
    client_id: str
    profile_version: str
    created_at: datetime
    tomography: TomographyGraph
    light_report: MarioReport
    shadow_report: LuigiReport
    consolidated_summary: str
    notebook_summary: NotebookSummary
    numeric_evidence: NumericEvidence
    motor_output: MotorOutput
    schema_version: str = "1.0"  # Moved to allow default value after non-defaults
    fuse_specs: List[FuseSpec] = field(default_factory=list)
    baseline_specs: List[BaselineSpec] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Serialización canónica para JSON."""
        # Usamos json.loads(agw_dumps(...)) para obtener un dict plano compatible con otros packers
        # que no usen el encoder especial (como el EvidencePacker de emergencia).
        return json.loads(agw_dumps(self))

    def save_json(self, base_dir: Path) -> Path:
        base_dir.mkdir(parents=True, exist_ok=True)
        filename = f"{self.client_id}_{self.profile_version}.json"
        path = base_dir / filename
        path.write_text(agw_dumps(self), encoding="utf-8")
        return path
