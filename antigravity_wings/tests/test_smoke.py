"""
Smoke tests para verificar que el exoesqueleto carga y corre la demo.
Valida Mario/Luigi + pipeline completo.
"""

import importlib
from antigravity_wings.observation.observer import SystemObserver, ObservationConfig
from antigravity_wings.tomography.builder import TomographyBuilder
from antigravity_wings.dual_agents.mario import MarioAgent
from antigravity_wings.dual_agents.luigi import LuigiAgent
from antigravity_wings.scripts.demo_pipeline import main as demo_main


def test_import_package():
    m = importlib.import_module("antigravity_wings")
    assert m is not None


def test_snapshot_and_tomography():
    from antigravity_wings.observation.registry import SourceRegistry
    registry = SourceRegistry()
    observer = SystemObserver("test_client", ObservationConfig(), registry)
    snapshot = observer.build_snapshot()
    assert snapshot.client_id == "test_client"
    tomo = TomographyBuilder().build(snapshot)
    assert len(tomo.nodes) >= 2
    assert len(tomo.edges) >= 1


def test_dual_agents():
    from antigravity_wings.api.models import TomographyGraph
    graph = TomographyGraph(client_id="test", nodes=[], edges=[])
    mario = MarioAgent().analyze(graph)
    luigi = LuigiAgent().analyze(graph)
    assert mario.client_id == "test"
    assert luigi.client_id == "test"


def test_demo_pipeline_runs():
    demo_main()
