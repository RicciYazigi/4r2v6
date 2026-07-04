"""
Configuración básica de logging para antigravity_wings.
"""
import logging


def setup_basic_logging(level=logging.INFO):
    """Configura logging básico para toda la aplicación."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(name)s | %(levelname)s | %(message)s"
    )
