import hashlib
import logging
from pathlib import Path
from datetime import datetime
from typing import Any, Dict

from antigravity_wings.api.json_utils import agw_dumps

logger = logging.getLogger(__name__)

class EvidencePacker:
    """
    Se encarga de persistir los artefactos de una corrida y generar el sellado criptográfico.
    """
    def __init__(self, session_dir: str):
        self.dir = Path(session_dir)
        self.dir.mkdir(parents=True, exist_ok=True)

    def pack(self, artifact_name: str, content: Any) -> str:
        """Guarda un artefacto y devuelve su hash SHA-256."""
        ext = "json" if not isinstance(content, str) else "txt"
        file_path = self.dir / f"{artifact_name}.{ext}"
        
        data = agw_dumps(content) if ext == "json" else content
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(data)
            
        file_hash = hashlib.sha256(data.encode("utf-8")).hexdigest()
        
        # Guardar el hash individualmente para auditoría rápida
        with open(file_path.with_suffix(".hash"), "w") as f:
            f.write(file_hash)
            
        logger.info(f"Artifact {artifact_name} packed. Hash: {file_hash[:8]}...")
        return file_hash

    def finalize_manifest(self, artifacts: Dict[str, str]):
        """Crea el manifiesto de la sesión con todos los hashes."""
        manifest = {
            "version": "1.0",
            "timestamp": datetime.utcnow().isoformat(),
            "artifacts": artifacts
        }
        manifest_path = self.dir / "manifest.json"
        
        with open(manifest_path, "w", encoding="utf-8") as f:
            f.write(agw_dumps(manifest))
            
        logger.info(f"Session manifest finalized at {manifest_path}")
