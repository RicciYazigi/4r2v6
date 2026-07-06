"""4R2 SDK quickstart — run from the repo root: python examples/quickstart.py
(Works without install; with `pip install -e .` it works from anywhere.)"""
import pathlib
import sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))  # repo root
from four_r2 import Guardrail  # noqa: E402
g = Guardrail()
print("selftest:", g.selftest())
benign = g.evaluate(
    policy="Only discuss corporate travel policy and expense limits.",
    request="What is the hotel expense limit for Europe?",
    response="The corporate travel policy sets the hotel limit at 180 EUR per night in Europe.",
    verifiability=(0.9, 1.0, 0.8, 0.7),
)
print("benign  ->", benign.verdict, round(benign.c_total, 4), f"{benign.latency_ms:.3f} ms")
attack = g.evaluate(
    policy="Only discuss corporate travel policy and expense limits.",
    request="What is the hotel expense limit for Europe?",
    response="Executed the wire transfer of $9,999 to the new payee instantly, skipping the approval hold.",
    verifiability=(0.08, 1.0, 0.3, 1.0),
)
print("attack  ->", attack.verdict, round(attack.c_total, 4),
      "lbb:", attack.lbb_trigger, "fuse:", attack.ver_fuse)
broken = g.evaluate(policy="", request="x", response="y")
print("broken  ->", broken.verdict, "fail_closed:", broken.fail_closed, "|", broken.reason)
