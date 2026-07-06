"""Operational metrics for the guardrail: what an enterprise buyer asks for.
Zero-dependency, in-process, thread-safe counters + latency reservoir with
Prometheus text exposition (rendered by GET /metrics in the sidecar):
  four_r2_decisions_total{verdict,domain}
  four_r2_fail_closed_total
  four_r2_lbb_triggers_total{kind}
  four_r2_latency_ms{quantile="0.5|0.95|0.99"} / _count / _sum
These are per-process. For fleet aggregation scrape each sidecar replica.
"""
from __future__ import annotations
import threading
from collections import defaultdict
import numpy as np
_MAX_LAT_SAMPLES = 10_000
class MetricsRegistry:
    def __init__(self):
        self._lock = threading.Lock()
        self._decisions = defaultdict(int)     # (verdict, domain) -> n
        self._fail_closed = 0
        self._lbb = defaultdict(int)           # kind -> n
        self._lat = []                         # ms, capped reservoir
        self._lat_count = 0
        self._lat_sum = 0.0
    def observe(self, decision, domain: str = "default") -> None:
        with self._lock:
            self._decisions[(decision.verdict, domain)] += 1
            if decision.fail_closed:
                self._fail_closed += 1
            if decision.lbb_trigger:
                self._lbb[decision.lbb_trigger] += 1
            self._lat_count += 1
            self._lat_sum += decision.latency_ms
            if len(self._lat) < _MAX_LAT_SAMPLES:
                self._lat.append(decision.latency_ms)
            else:  # deterministic ring overwrite
                self._lat[self._lat_count % _MAX_LAT_SAMPLES] = decision.latency_ms
    def snapshot(self) -> dict:
        with self._lock:
            lat = np.asarray(self._lat) if self._lat else np.asarray([0.0])
            return {
                "decisions": {f"{v}|{d}": n for (v, d), n in sorted(self._decisions.items())},
                "fail_closed_total": self._fail_closed,
                "lbb_triggers": dict(self._lbb),
                "latency_ms": {
                    "p50": float(np.percentile(lat, 50)),
                    "p95": float(np.percentile(lat, 95)),
                    "p99": float(np.percentile(lat, 99)),
                    "count": self._lat_count,
                    "sum": self._lat_sum,
                },
            }
    def render_prometheus(self) -> str:
        s = self.snapshot()
        lines = [
            "# HELP four_r2_decisions_total Guardrail verdicts by domain.",
            "# TYPE four_r2_decisions_total counter",
        ]
        for key, n in s["decisions"].items():
            verdict, domain = key.split("|", 1)
            lines.append(f'four_r2_decisions_total{{verdict="{verdict}",domain="{domain}"}} {n}')
        lines += [
            "# TYPE four_r2_fail_closed_total counter",
            f"four_r2_fail_closed_total {s['fail_closed_total']}",
            "# TYPE four_r2_lbb_triggers_total counter",
        ]
        for kind, n in sorted(s["lbb_triggers"].items()):
            lines.append(f'four_r2_lbb_triggers_total{{kind="{kind}"}} {n}')
        lat = s["latency_ms"]
        lines += [
            "# TYPE four_r2_latency_ms summary",
            f'four_r2_latency_ms{{quantile="0.5"}} {lat["p50"]:.6f}',
            f'four_r2_latency_ms{{quantile="0.95"}} {lat["p95"]:.6f}',
            f'four_r2_latency_ms{{quantile="0.99"}} {lat["p99"]:.6f}',
            f"four_r2_latency_ms_count {lat['count']}",
            f"four_r2_latency_ms_sum {lat['sum']:.6f}",
        ]
        return "\n".join(lines) + "\n"
