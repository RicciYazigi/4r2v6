import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

class DataSource(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def collect(self) -> List[Dict[str, Any]]:
        pass

@dataclass
class SourceRegistry:
    """Mantiene el registro de de dónde viene cada pieza de información."""
    sources: List[DataSource] = field(default_factory=list)

    def register_source(self, source: DataSource):
        self.sources.append(source)
        logger.info(f"Source registered: {source.name}")

    def all_sources(self) -> List[DataSource]:
        return self.sources
