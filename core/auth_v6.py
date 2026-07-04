import hmac, hashlib, os, secrets, time
import json
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

def get_api_keys() -> dict:
    raw = os.environ.get("API_KEYS_JSON")
    if not raw:
        return {}
    try:
        return json.loads(raw)
    except Exception:
        return {}

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)) -> str:
    token = credentials.credentials
    api_keys = get_api_keys()
    if not api_keys:
        raise HTTPException(status_code=503, detail="Server misconfigured: API token not set")
    try:
        prefix, key_id, secret = token.split("_", 2)
        assert prefix == "4r2"
    except (ValueError, AssertionError):
        raise HTTPException(401, "Malformed credential")
    stored = api_keys.get(key_id)
    if stored is None:
        raise HTTPException(401, "Unknown key")
    digest = hashlib.sha256(secret.encode()).hexdigest()
    if not hmac.compare_digest(digest, stored["hash"]):        # timing-safe
        raise HTTPException(401, "Invalid credential")
    if stored.get("expires", float("inf")) < time.time():
        raise HTTPException(401, "Expired credential")
    return key_id  # identity, not secret

def mint_key(tenant: str, ttl_days: int = 90) -> tuple[str, dict]:
    """Admin tool (offline CLI, never public endpoint)."""
    key_id = secrets.token_hex(8)
    secret = secrets.token_urlsafe(32)
    record = {
        "hash": hashlib.sha256(secret.encode()).hexdigest(),
        "tenant": tenant,
        "expires": time.time() + ttl_days*86400
    }
    return f"4r2_{key_id}_{secret}", {key_id: record}
