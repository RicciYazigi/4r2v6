from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from antigravity_wings.api.models import (
    ConsolidatedReport,
    NotebookSummary,
    NumericEvidence,
)
from antigravity_wings.resilience.circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerConfig,
    CircuitOpenError,
)

logger = logging.getLogger(__name__)


@dataclass
class NotebookTemplateEngine:
    """
    Motor de plantillas muy ligero para generar Markdown.

    Se diseña para ser:
    - Determinista.
    - Fácil de parsear por NotebookLM.
    - Independiente de librerías externas.
    """

    def render(
        self,
        report: ConsolidatedReport,
        numeric_evidence: Optional[NumericEvidence] = None,
    ) -> str:
        """
        Genera un documento Markdown con secciones bien delimitadas.
        """

        timestamp = datetime.utcnow().isoformat(timespec="seconds") + "Z"

        # Citas / referencias bibliográficas simples
        references = report.references or []
        ref_lines: List[str] = []
        for idx, ref in enumerate(references, start=1):
            ref_lines.append(f"[{idx}] {ref}")

        refs_block = "\n".join(ref_lines) if ref_lines else "_Sin referencias explícitas._"

        # Evidencia numérica (vista pública)
        if numeric_evidence is not None:
            fv = numeric_evidence.feature_vector
            ev_summary = (
                f"- Dimensión del vector: {len(fv)}\n"
                f"- Valores (primeros 10): {fv[:10]}\n"
                f"- Metadata: `{numeric_evidence.metadata}`\n"
            )
        else:
            ev_summary = "_No se adjuntó evidencia numérica en esta versión._\n"

        # Preparar bloques de texto para evitar backslashes en f-strings (compatibilidad <3.12)
        light_strengths = "".join(f"- {s}\n" for s in report.light.strengths) or "_Sin fortalezas reportadas._\n"
        light_redundancies = "".join(f"- {r}\n" for r in report.light.redundancies) or "_Sin redundancias explícitas._\n"
        light_safe_zones = "".join(f"- {z}\n" for z in report.light.safe_zones) or "_Sin zonas catalogadas como seguras._\n"
        light_notes = "".join(f"- {n}\n" for n in report.light.notes) or "_Sin notas adicionales._\n"

        shadow_risks = "".join(f"- {r}\n" for r in report.shadow.risks) or "_Sin riesgos explícitos._\n"
        shadow_fragile_deps = "".join(f"- {d}\n" for d in report.shadow.fragile_dependencies) or "_Sin dependencias frágiles reportadas._\n"
        shadow_no_return = "".join(f"- {p}\n" for p in report.shadow.no_return_points) or "_Sin puntos irreversibles identificados._\n"
        shadow_notes = "".join(f"- {n}\n" for n in report.shadow.notes) or "_Sin notas adicionales._\n"

        # Plantilla Markdown
        md = f"""# Informe Técnico de Coherencia — Cliente {report.client_id}

_Generado: {timestamp}_

---

## 1. Resumen Ejecutivo

{report.summary}

---

## 2. Fortalezas (Mario / Agente Luz)

**Puntos identificados por el analizador optimista ("Luz")**:

- Cliente: `{report.light.client_id}`

### 2.1 Fortalezas

{light_strengths}

### 2.2 Redundancias Positivas

{light_redundancies}

### 2.3 Zonas Seguras

{light_safe_zones}

### 2.4 Notas de Luz

{light_notes}

---

## 3. Riesgos (Luigi / Agente Sombra)

**Puntos identificados por el analizador de riesgo ("Sombra")**:

- Cliente: `{report.shadow.client_id}`

### 3.1 Riesgos

{shadow_risks}

### 3.2 Dependencias Frágiles

{shadow_fragile_deps}

### 3.3 Puntos de No-retorno

{shadow_no_return}

### 3.4 Notas de Sombra

{shadow_notes}

---

## 4. Evidencia Numérica (Vista Agnóstica)

Este bloque resume la representación numérica del sistema evaluado.
No incluye fórmulas ni lógica interna; solo una vista de forma.

{ev_summary}

---

## 5. Referencias / Citas

{refs_block}

---

## 6. Notas para NotebookLM

- Este documento se ha estructurado en secciones numeradas (1..6).
- Cada lista de puntos es independiente y puede ser referenciada
  por sección (p.ej. "ver sección 3.1 para riesgos").
- Las referencias [n] corresponden a documentos o fuentes externas
  relevantes, listadas en la sección 5.
"""

        return md



class NotebookClient:
    """
    Cliente de alto nivel para construir artefactos para NotebookLM.
    Integración opcional con Agencia API para resúmenes reales.
    """

    def __init__(
        self, 
        notebook_id: str, 
        api_key: Optional[str] = None,
        use_real_llm: bool = False,
        agency_url: str = "http://localhost:3000/api/v1/agency/summarize",
        circuit_config: Optional[CircuitBreakerConfig] = None
    ) -> None:
        self.notebook_id = notebook_id
        self.api_key = api_key
        self.use_real_llm = use_real_llm
        self.agency_url = agency_url
        self._engine = NotebookTemplateEngine()
        
        config = circuit_config or CircuitBreakerConfig(
            failure_threshold=3,
            recovery_timeout_sec=60.0,
            max_latency_sec=10.0
        )
        self._cb = CircuitBreaker(name=f"notebook_{notebook_id}", config=config)

    @property
    def circuit_metrics(self):
        return self._cb.metrics

    def build_markdown(
        self,
        report: ConsolidatedReport,
        numeric_evidence: Optional[NumericEvidence] = None,
    ) -> str:
        try:
            return self._cb.call(self._engine.render, report, numeric_evidence)
        except (CircuitOpenError, Exception) as exc:
            logger.error("Notebook markdown generation failed (CB): %s", exc)
            return f"# Informe Técnico (FALLBACK) — {report.client_id}\n\nError: {exc}"

    def summarize(self, report: ConsolidatedReport) -> NotebookSummary:
        """
        Genera un resumen sintético. Usa Agencia API si está configurado.
        """
        try:
            if self.use_real_llm:
                return self._cb.call(self._summarize_via_agency, report)
            return self._cb.call(self._summarize_internal, report)
        except (CircuitOpenError, Exception) as exc:
            logger.error("Notebook summarization failed (CB): %s", exc)
            return NotebookSummary(
                client_id=report.client_id,
                condensed_summary=f"fallback: {exc}",
                key_points=["Error de resiliencia en la capa de Notebook / Agencia"],
                source_refs=report.references,
            )

    def _summarize_via_agency(self, report: ConsolidatedReport) -> NotebookSummary:
        """Llamada real a la Agencia API de Antigravity (LLM)."""
        import httpx
        payload = {
            "client_id": report.client_id,
            "context": report.summary,
            "mario_input": [s for s in report.light.strengths],
            "luigi_input": [r for r in report.shadow.risks]
        }
        
        with httpx.Client(timeout=15.0) as client:
            response = client.post(self.agency_url, json=payload)
            response.raise_for_status()
            data = response.json()
            
            return NotebookSummary(
                client_id=report.client_id,
                condensed_summary=data.get("summary", "No summary provided by Agency"),
                key_points=data.get("insights", ["Analysis delivered by Real LLM"]),
                source_refs=report.references
            )

    def _summarize_internal(self, report: ConsolidatedReport) -> NotebookSummary:
        condensed = f"[NB-MOCK:{self.notebook_id}] Summary for {report.client_id}"
        key_points: List[str] = [
            f"Luz: {len(report.light.strengths)} fortalezas",
            f"Sombra: {len(report.shadow.risks)} riesgos",
        ]
        return NotebookSummary(
            client_id=report.client_id,
            condensed_summary=condensed,
            key_points=key_points,
            source_refs=report.references,
        )
