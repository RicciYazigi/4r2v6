# INTEGRATION GUIDE (v7.0.0)
Three consumption modes, in order of coupling: SDK (Python, in-process),
sidecar (any language, REST), gateway pattern (fleet).
## 1. SDK (Python)
```python
from four_r2 import Guardrail
g = Guardrail(theta=0.35, weights_profile="balanced")
def guarded_completion(policy: str, user_msg: str, llm) -> str:
    draft = llm(user_msg)
    d = g.evaluate(policy=policy, request=user_msg, response=draft,
                   verifiability=compute_F(user_msg, draft))  # server-side F!
    if d.verdict == "ALLOW":
        return draft
    if d.verdict == "FLAG":
        return escalate_to_human(draft, d)      # Art. 14 human oversight band
    return refusal_message(d)                    # BLOCK (includes fail-closed)
```
Rules:
- One embedder instance shared across N/R/I (enforced by dim check).
- `evaluate()` never raises; check `d.fail_closed` for pipeline errors.
- Compute F **server-side**. Never trust caller-supplied F (THREAT_MODEL #9).
## 2. Sidecar (any language)
```bash
export FOUR_R2_API_KEY=$(openssl rand -hex 24)
uvicorn four_r2.service:app --host 0.0.0.0 --port 8472
# or: docker compose -f docker-compose.sidecar.yml up -d
```
Client contract (pseudocode, any language):
```
resp = POST http://sidecar:8472/v1/evaluate
       headers: {X-API-Key: ...}
       json: {policy, request, response, verifiability?, criticality?, domain}
if resp.status != 200 or request timed out:  verdict = BLOCK   # fail-closed end-to-end
else: verdict = resp.json.verdict
```
The sidecar returns fail-closed answers as HTTP 200 + `verdict=BLOCK` +
`fail_closed=true`. Your client MUST also map network failure to BLOCK.
## 3. LangChain-style middleware (pattern)
Wrap the model call: after generation, before returning to the user, call the
sidecar with (system_prompt → policy, user_input → request, generation →
response). On FLAG, push to your review queue with `d.breakdown` attached —
the per-layer scores are the audit artifact.
## 4. OpenAI-compatible proxy (pattern)
Terminate `/v1/chat/completions`, forward upstream, gate the upstream response
through `/v1/evaluate`, replace blocked content with a refusal payload, log
`Decision.to_dict()` to your evidence store (append-only), return.
## 5. Observability
Scrape `GET /metrics` (Prometheus):
`four_r2_decisions_total{verdict,domain}`, `four_r2_fail_closed_total`,
`four_r2_lbb_triggers_total{kind}`, `four_r2_latency_ms{quantile}`.
Alert suggestions: fail_closed rate > 1% (pipeline health), BLOCK-rate spike
per domain (attack or drift), p99 latency regression.
## 6. Calibration workflow (per embedder / domain / tenant)
```python
from four_r2 import Guardrail, calibrate_theta
rep = calibrate_theta(Guardrail(), benign_cases, grave_cases)
if rep.status == "OK":
    g = Guardrail(theta=rep.theta_star)
else:
    # OVERLAP / INSUFFICIENT_DATA: keep default theta, rely on LBB + fuses,
    # improve embedder or F signals. Do NOT invent a threshold.
    g = Guardrail()
```
Recalibrate on: embedder change, domain expansion, F-pipeline change, drift
alerts. Keep θ* per tenant and non-public (THREAT_MODEL #8).
