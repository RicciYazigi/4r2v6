"""4R2 sidecar service — REST enforcement point for any stack, any language.
Run:
    uvicorn four_r2.service:app --host 0.0.0.0 --port 8472
or, containerized:
    docker compose -f docker-compose.sidecar.yml up -d
Endpoints:
    GET  /health       liveness + kernel selftest invariants + versions
    POST /v1/evaluate  score one decision -> Decision JSON (HTTP 200 always
                       when authenticated; fail-closed answers are verdict
                       BLOCK with fail_closed=true, NOT HTTP 5xx — a 5xx can
                       be misread by naive clients as "no answer, proceed").
    GET  /metrics      Prometheus text exposition
Auth: if env FOUR_R2_API_KEY is set, requests must carry X-API-Key. If it is
not set, the service is open (dev mode) and /health reports auth="disabled".
Config env vars: FOUR_R2_THETA (default 0.35), FOUR_R2_WEIGHTS_PROFILE
(default "balanced"), FOUR_R2_API_KEY (optional).
"""
from __future__ import annotations
import os
from typing import List, Optional
from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, Field
from ._version import KERNEL_MATH_VERSION, __version__
from .guardrail import Guardrail
from .metrics import MetricsRegistry
class EvaluateRequest(BaseModel):
    policy: str = Field(min_length=1, description="Governing policy / system rules text")
    request: str = Field(min_length=1, description="User request text")
    response: str = Field(min_length=1, description="Candidate model output to gate")
    verifiability: Optional[List[float]] = Field(
        default=None, min_length=4, max_length=4,
        description="(f_ground, f_num, f_cite, f_exec) in [0,1]^4; omit => conservative 0.5 prior",
    )
    criticality: float = Field(default=0.0, ge=0.0, le=1.0)
    domain: str = Field(default="default", max_length=64)
def create_app(guardrail: Optional[Guardrail] = None) -> FastAPI:
    g = guardrail or Guardrail(
        theta=float(os.environ.get("FOUR_R2_THETA", "0.35")),
        weights_profile=os.environ.get("FOUR_R2_WEIGHTS_PROFILE", "balanced"),
    )
    metrics = MetricsRegistry()
    api_key = os.environ.get("FOUR_R2_API_KEY") or None
    app = FastAPI(
        title="4R2 Coherence Guardrail",
        version=__version__,
        description="Deterministic fail-closed NRIF guardrail sidecar.",
    )
    app.state.guardrail = g
    app.state.metrics = metrics
    def _auth(x_api_key: Optional[str]) -> None:
        if api_key is not None and x_api_key != api_key:
            raise HTTPException(status_code=401, detail="invalid or missing X-API-Key")
    @app.get("/health")
    def health(x_api_key: Optional[str] = Header(default=None)):
        st = g.selftest()
        ok = st.get("perfect_c") == 0.0 and st.get("loss_correct_direction") is True
        return {
            "status": "ok" if ok else "degraded",
            "package_version": __version__,
            "kernel_math_version": KERNEL_MATH_VERSION,
            "theta": g.theta,
            "weights_profile": g.weights_profile,
            "auth": "enabled" if api_key else "disabled",
            "selftest": st,
        }
    @app.post("/v1/evaluate")
    def evaluate(body: EvaluateRequest, x_api_key: Optional[str] = Header(default=None)):
        _auth(x_api_key)
        decision = g.evaluate(  # never raises: fail-closed => BLOCK
            policy=body.policy,
            request=body.request,
            response=body.response,
            verifiability=body.verifiability,
            criticality=body.criticality,
        )
        metrics.observe(decision, domain=body.domain)
        return decision.to_dict()
    @app.get("/metrics", response_class=PlainTextResponse)
    def prometheus(x_api_key: Optional[str] = Header(default=None)):
        _auth(x_api_key)
        return metrics.render_prometheus()
    return app
app = create_app()
