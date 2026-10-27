import hmac

from fastapi import Header, HTTPException
from .config import A2A_API_KEY

def require_api_key(authorization: str | None = Header(default=None)):
    # Demo authentication. Replace with OAuth2/mTLS/workload identity in production.
    if not A2A_API_KEY:
        raise HTTPException(status_code=503, detail="A2A authentication is not configured")
    expected = f"Bearer {A2A_API_KEY}"
    if not authorization or not hmac.compare_digest(authorization, expected):
        raise HTTPException(status_code=401, detail="Invalid or missing A2A credentials")
