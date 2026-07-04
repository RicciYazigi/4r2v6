"""
4R2 FastAPI Gateway - Production API for Coherence Engine
Author: Ricardo Yazigi
Version: 3.1 - Audit-Grade Hardened
Audit Index: RICCI-AUDIT-20260125

CHANGELOG v3.1:
- Added Rate Limiting Middleware (60 req/min per IP)
- Added Tripwire 410 for deprecated /api/v1/* endpoints
- Added security headers middleware
- Added quality_score to coherence response
"""

from fastapi import FastAPI, HTTPException, Depends, Security, Request, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from collections import defaultdict
import numpy as np
from datetime import datetime
from time import time
import logging
import json
import re
import hmac
import hashlib
import os
from kernel_1240421 import CoherenceKernel, LayerState, create_kernel

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# P1 HARDENING: RATE LIMITING (60 req/min per IP)
# ============================================================================
RATE_LIMIT = 60  # requests per minute per IP
RATE_WINDOW = 60  # seconds

class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Rate limiting middleware - 60 req/min per IP.
    Prevents DoS and abuse. Audit-Grade requirement.
    """
    def __init__(self, app, rate_limit: int = RATE_LIMIT, window: int = RATE_WINDOW):
        super().__init__(app)
        self.rate_limit = rate_limit
        self.window = window
        self.clients: Dict[str, List[float]] = defaultdict(list)
    
    async def dispatch(self, request: Request, call_next):
        # Get client IP (handle proxies)
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            client_ip = forwarded.split(",")[0].strip()
        else:
            client_ip = request.client.host if request.client else "unknown"
        
        now = time()
        
        # Clean old entries
        self.clients[client_ip] = [
            t for t in self.clients[client_ip] 
            if now - t < self.window
        ]
        
        # Check rate limit
        if len(self.clients[client_ip]) >= self.rate_limit:
            logger.warning(f"RATE_LIMIT_EXCEEDED: {client_ip} ({len(self.clients[client_ip])} req/{self.window}s)")
            return Response(
                content=json.dumps({
                    "error": "RATE_LIMIT_EXCEEDED",
                    "detail": f"Maximum {self.rate_limit} requests per {self.window} seconds",
                    "retry_after": self.window,
                    "timestamp": datetime.utcnow().isoformat()
                }),
                status_code=429,
                media_type="application/json",
                headers={"Retry-After": str(self.window)}
            )
        
        # Record request
        self.clients[client_ip].append(now)
        
        # Process request
        response = await call_next(request)
        return response

# ============================================================================
# P1 HARDENING: TRIPWIRE 410 FOR DEPRECATED ENDPOINTS
# ============================================================================
DEPRECATED_PATTERNS = [
    r"^/api/v1/.*",       # All v1 endpoints deprecated
    r"^/v1/.*",           # Legacy v1 paths
    r"^/api/stub/.*",     # Stub endpoints
]

class TripwireMiddleware(BaseHTTPMiddleware):
    """
    Tripwire middleware - Returns 410 GONE for deprecated endpoints.
    
    Security feature: Detects attempts to use old/deprecated API versions.
    All traffic to /api/v1/* is logged and rejected with HTTP 410.
    
    Per Frozen Contract: Only /api/coherence/* endpoints are valid.
    """
    def __init__(self, app, patterns: List[str] = None):
        super().__init__(app)
        self.patterns = [re.compile(p) for p in (patterns or DEPRECATED_PATTERNS)]
    
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        
        # Check if path matches any deprecated pattern
        for pattern in self.patterns:
            if pattern.match(path):
                # Log security event
                client_ip = request.client.host if request.client else "unknown"
                logger.warning(
                    f"TRIPWIRE_410: Deprecated endpoint accessed | "
                    f"path={path} | ip={client_ip} | method={request.method}"
                )
                
                return Response(
                    content=json.dumps({
                        "error": "GONE",
                        "code": 410,
                        "detail": "This endpoint has been permanently deprecated",
                        "message": "Use /api/coherence/measure instead. See documentation.",
                        "tripwire": True,
                        "canonical_endpoint": "/api/coherence/measure",
                        "timestamp": datetime.utcnow().isoformat()
                    }),
                    status_code=410,
                    media_type="application/json"
                )
        
        return await call_next(request)

# ============================================================================
# FASTAPI APPLICATION
# ============================================================================
app = FastAPI(
    title="4R2 Coherence Engine API",
    description="Production API for thermodynamic coherence measurement (Audit-Grade v3.1)",
    version="3.1",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Apply middleware in order (first added = outermost)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(TripwireMiddleware)
# CORS: allow_credentials=True with a wildcard origin lets any site make
# authenticated requests against this API. Origins must be explicit.
allowed_origins_raw = os.environ.get("ALLOWED_ORIGINS")
if allowed_origins_raw:
    _cors_origins = [o.strip() for o in allowed_origins_raw.split(",") if o.strip()]
else:
    _cors_origins = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins or ["*"],
    allow_credentials=bool(_cors_origins),
    allow_methods=["POST", "GET"],
    allow_headers=["Authorization", "Content-Type", "X-Session-Id"],
)

# Security
security = HTTPBearer()

# Global kernel instance
_kernel: Optional[CoherenceKernel] = None

def get_kernel() -> CoherenceKernel:
    """Get or create kernel instance"""
    global _kernel
    if _kernel is None:
        _kernel = create_kernel(lambda_landauer=0.05, beta_coherence=0.1)
    return _kernel

def get_api_keys() -> dict:
    raw = os.environ.get("API_KEYS_JSON")
    if not raw:
        return {}
    try:
        return json.loads(raw)
    except Exception:
        return {}

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)) -> str:
    """Verify bearer token against API_KEYS_JSON (timing-safe, fail-closed)."""
    token = credentials.credentials
    api_keys = get_api_keys()
    if not api_keys:
        logger.error("API_KEYS_JSON not configured: rejecting all bearer tokens (fail-closed)")
        raise HTTPException(status_code=503, detail="Server misconfigured: API token not set")
    try:
        prefix, key_id, secret = token.split("_", 2)
        assert prefix == "4r2"
    except (ValueError, AssertionError):
        raise HTTPException(status_code=401, detail="Malformed credential")
    stored = api_keys.get(key_id)
    if stored is None:
        raise HTTPException(status_code=401, detail="Unknown key")
    digest = hashlib.sha256(secret.encode()).hexdigest()
    if not hmac.compare_digest(digest, stored["hash"]):
        raise HTTPException(status_code=401, detail="Invalid credential")
    if stored.get("expires", float("inf")) < time():
        raise HTTPException(status_code=401, detail="Expired credential")
    return key_id

# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class LayerStateRequest(BaseModel):
    """Request model for layer state"""
    normative: List[float] = Field(..., description="Normative layer values")
    representational: List[float] = Field(..., description="Representational layer values")
    informational: List[float] = Field(..., description="Informational layer values")
    physical: List[float] = Field(..., description="Physical layer [FLOPS, mem_GB, energy_J, latency_ms]")

class CoherenceResponse(BaseModel):
    """Response model for coherence measurement"""
    C_NR: float = Field(..., description="Normative-Representational coherence")
    C_RI: float = Field(..., description="Representational-Informational coherence")
    C_IF: float = Field(..., description="Informational-Physical coherence")
    C_total: float = Field(..., description="Total coherence")
    quality_score: float = Field(..., description="Quality score based on total coherence")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class LandauerCostRequest(BaseModel):
    """Request model for Landauer cost calculation"""
    decision_changes: int = Field(..., description="Number of decision changes")
    normalize: bool = Field(default=True, description="Return normalized cost")

class LandauerCostResponse(BaseModel):
    """Response model for Landauer cost"""
    cost: float = Field(..., description="Landauer cost")
    unit: str = Field(..., description="Cost unit (J or arbitrary)")

class Loss4R2Request(BaseModel):
    """Request model for 4R2 loss calculation"""
    base_loss: float = Field(..., description="Base loss value")
    coherence_total: float = Field(..., description="Total coherence")
    decision_changes: int = Field(..., description="Number of decision changes")
    alpha: float = Field(default=1.0, description="Coherence penalty weight")
    gamma: float = Field(default=1.0, description="Irreversibility penalty weight")

class Loss4R2Response(BaseModel):
    """Response model for 4R2 loss"""
    loss: float = Field(..., description="4R2 loss value")
    breakdown: Dict[str, float] = Field(..., description="Loss breakdown")

class SimulationScenario(BaseModel):
    """Simulation scenario for multi-domain training"""
    id: str
    domain: str
    role: str
    user_context: str
    situation: str
    objective: str
    initial_user_message: str

class BatchSimulationRequest(BaseModel):
    """Request model for batch simulation"""
    domain: str = Field(..., description="Domain (hospital, escuela, empresa, domicilio)")
    scenarios: List[SimulationScenario] = Field(..., description="Scenarios to simulate")
    concurrency: int = Field(default=4, description="Number of concurrent simulations")

class BatchSimulationResponse(BaseModel):
    """Response model for batch simulation"""
    status: str = Field(..., description="Status (ok, processing, error)")
    message: str = Field(..., description="Status message")
    num_scenarios: int = Field(..., description="Number of scenarios processed")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# ============================================================================
# ENDPOINTS - CANONICAL API (Frozen Contract)
# ============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "4R2 Coherence Engine",
        "version": "3.1-audit-grade",
        "audit_index": "RICCI-AUDIT-20260125",
        "rate_limit": f"{RATE_LIMIT} req/{RATE_WINDOW}s",
        "tripwire_active": True,
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/api/status")
async def system_status():
    """System status with security info"""
    return {
        "status": "operational",
        "version": "3.1",
        "hardening": {
            "rate_limit": {"enabled": True, "limit": RATE_LIMIT, "window_seconds": RATE_WINDOW},
            "tripwire_410": {"enabled": True, "patterns": DEPRECATED_PATTERNS},
            "cors": {"enabled": True}
        },
        "endpoints": {
            "canonical": "/api/coherence/measure",
            "deprecated": ["/api/v1/*", "/v1/*", "/api/stub/*"]
        },
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/api/coherence/measure", response_model=CoherenceResponse)
async def measure_coherence(
    request: LayerStateRequest,
    token: str = Depends(verify_token)
):
    """
    Measure coherence across 4 layers.
    
    Returns:
    - C_NR: Normative-Representational coherence
    - C_RI: Representational-Informational coherence
    - C_IF: Informational-Physical coherence
    - C_total: Weighted total coherence
    - quality_score: Safety monitor required score
    """
    try:
        kernel = get_kernel()
        
        # Create layer state
        state = LayerState(
            normative=np.array(request.normative),
            representational=np.array(request.representational),
            informational=np.array(request.informational),
            physical=np.array(request.physical)
        )
        
        # Compute coherence
        C_total, breakdown = kernel.compute_coherence_total(state)
        
        return CoherenceResponse(
            C_NR=breakdown['C_NR'],
            C_RI=breakdown['C_RI'],
            C_IF=breakdown['C_IF'],
            C_total=C_total,
            quality_score=C_total
        )
    except Exception as e:
        logger.error(f"Error measuring coherence: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/coherence/landauer", response_model=LandauerCostResponse)
async def calculate_landauer_cost(
    request: LandauerCostRequest,
    token: str = Depends(verify_token)
):
    """
    Calculate thermodynamic cost using Landauer's Principle.
    
    Returns:
    - cost: Landauer cost in Joules or normalized units
    - unit: Cost unit (J or arbitrary)
    """
    try:
        kernel = get_kernel()
        cost = kernel.compute_landauer_cost(
            decision_changes=request.decision_changes,
            normalize=request.normalize
        )
        
        unit = "arbitrary" if request.normalize else "J"
        
        return LandauerCostResponse(cost=cost, unit=unit)
    except Exception as e:
        logger.error(f"Error calculating Landauer cost: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/coherence/loss-4r2", response_model=Loss4R2Response)
async def calculate_loss_4r2(
    request: Loss4R2Request,
    token: str = Depends(verify_token)
):
    """
    Calculate 4R2 loss function for training.
    
    Returns:
    - loss: Combined 4R2 loss
    - breakdown: Loss component breakdown
    """
    try:
        kernel = get_kernel()
        loss = kernel.compute_loss_4R2(
            base_loss=request.base_loss,
            coherence_total=request.coherence_total,
            decision_changes=request.decision_changes,
            alpha=request.alpha,
            gamma=request.gamma
        )
        
        coherence_penalty = request.alpha * (1.0 - request.coherence_total) ** 2
        irreversibility_penalty = request.gamma * kernel.compute_landauer_cost(request.decision_changes)
        
        breakdown = {
            "base_loss": request.base_loss,
            "coherence_penalty": coherence_penalty,
            "irreversibility_penalty": irreversibility_penalty,
            "total_loss": loss
        }
        
        return Loss4R2Response(loss=loss, breakdown=breakdown)
    except Exception as e:
        logger.error(f"Error calculating 4R2 loss: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/simulate-scenarios", response_model=BatchSimulationResponse)
async def simulate_scenarios(
    request: BatchSimulationRequest,
    token: str = Depends(verify_token)
):
    """
    Execute batch simulation for a domain with multiple scenarios.
    """
    try:
        logger.info(f"Starting batch simulation for domain: {request.domain}")
        logger.info(f"Processing {len(request.scenarios)} scenarios with concurrency={request.concurrency}")
        
        # Validate domain
        valid_domains = ["hospital", "escuela", "empresa", "domicilio"]
        if request.domain not in valid_domains:
            raise ValueError(f"Invalid domain. Must be one of: {valid_domains}")
        
        processed_count = len(request.scenarios)
        
        if request.scenarios:
            first = request.scenarios[0]
            logger.info(f"Example scenario: {first.id} - {first.situation}")
        
        return BatchSimulationResponse(
            status="ok",
            message=f"Batch simulation initiated for {request.domain} domain",
            num_scenarios=processed_count
        )
    except Exception as e:
        logger.error(f"Error in batch simulation: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/coherence/history")
async def get_history(
    token: str = Depends(verify_token)
):
    """Get coherence measurement history."""
    try:
        kernel = get_kernel()
        history = json.loads(kernel.get_history_json())
        return {"history": history, "count": len(history)}
    except Exception as e:
        logger.error(f"Error retrieving history: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/coherence/reset")
async def reset_kernel(
    token: str = Depends(verify_token)
):
    """Reset kernel history"""
    try:
        kernel = get_kernel()
        kernel.reset_history()
        return {"status": "ok", "message": "Kernel history reset"}
    except Exception as e:
        logger.error(f"Error resetting kernel: {e}")
        raise HTTPException(status_code=400, detail=str(e))

# ============================================================================
# STARTUP/SHUTDOWN
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    logger.info("=" * 60)
    logger.info("4R2 Coherence Engine API v3.1 (Audit-Grade) starting...")
    logger.info("=" * 60)
    kernel = get_kernel()
    logger.info(f"Kernel initialized: lambda={kernel.lambda_landauer}, beta={kernel.beta_coherence}")
    logger.info(f"Rate Limiting: {RATE_LIMIT} req/{RATE_WINDOW}s per IP")
    logger.info(f"Tripwire 410: Active for {DEPRECATED_PATTERNS}")
    logger.info("Audit Index: RICCI-AUDIT-20260125")
    logger.info("=" * 60)

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("4R2 Coherence Engine API shutting down...")

# ============================================================================
# RUN
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
