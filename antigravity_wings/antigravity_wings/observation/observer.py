# antigravity_wings/observation/observer.py

"""
Agente de Lectura / Observación.

Responsabilidades:
- Recibir un `SourceRegistry` con múltiples `DataSource`.
- Ejecutar la recolección de cada fuente de forma aislada (manejo de excepciones por fuente).
- Consolidar todo en un `SystemSnapshot` agnóstico al dominio.

Convención ligera (no obligatoria, pero útil):
- Cada DataSource devuelve una lista de dicts.
- El Observer:
  - añade siempre "source_name" al dict consolidado.
  - si un dict trae la clave "doc_ref" (str), se agrega a `raw_docs`.
  - todo el resto se agrega a `observed_flows`.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict, Any
import logging

from antigravity_wings.api.models import SystemSnapshot
from antigravity_wings.observation.registry import SourceRegistry

logger = logging.getLogger(__name__)


@dataclass
class ObservationConfig:
    """
    Configuración genérica de observación.
    Puede extenderse con filtros, límites, etc.
    """
    max_events: int = 10000  # límite de registros totales a incluir en el snapshot


class SystemObserver:
    """
    Observador central que orquesta la recolección desde múltiples fuentes.

    No conoce detalles de cada fuente, solo invoca `collect()` en cada `DataSource`
    registrado en el `SourceRegistry`.
    """

    def __init__(self, client_id: str, config: ObservationConfig, source_registry: SourceRegistry) -> None:
        self.client_id = client_id
        self.config = config
        self.source_registry = source_registry

    def build_snapshot(self) -> SystemSnapshot:
        """
        Ejecuta la recolección en todas las fuentes registradas y construye
        un `SystemSnapshot`.

        - Errores en una fuente NO detienen la observación de las demás.
        - Los errores se loguean con nivel WARNING.
        """

        raw_docs: List[str] = []
        observed_flows: List[Dict[str, Any]] = []

        total_records = 0

        for source in self.source_registry.all_sources():
            try:
                logger.debug("Collecting from data source '%s'", source.name)
                records = source.collect()
            except Exception as exc:  # noqa: BLE001
                logger.warning(
                    "Error collecting from data source '%s': %s",
                    source.name,
                    exc,
                    exc_info=True,
                )
                continue

            if not isinstance(records, list):
                logger.warning(
                    "Data source '%s' returned non-list result: %r",
                    source.name,
                    type(records),
                )
                continue

            for rec in records:
                if not isinstance(rec, dict):
                    logger.debug(
                        "Skipping non-dict record from '%s': %r",
                        source.name,
                        rec,
                    )
                    continue

                # Añadir metadata mínima de origen
                enriched = {"source_name": source.name, **rec}
                observed_flows.append(enriched)
                total_records += 1

                # Extraer referencias a documentos si existen
                doc_ref = rec.get("doc_ref")
                if isinstance(doc_ref, str):
                    raw_docs.append(doc_ref)

                if total_records >= self.config.max_events:
                    logger.info(
                        "Reached max_events=%d, stopping collection early",
                        self.config.max_events,
                    )
                    break

            if total_records >= self.config.max_events:
                break

        snapshot = SystemSnapshot(
            client_id=self.client_id,
            raw_docs=raw_docs,
            observed_flows=observed_flows,
        )

        logger.info(
            "Built snapshot for client_id=%s with %d flows and %d raw_docs",
            self.client_id,
            len(snapshot.observed_flows),
            len(snapshot.raw_docs),
        )

        return snapshot
