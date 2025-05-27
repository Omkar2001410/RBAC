import secrets
import time
from typing import Dict

# In-memory store (for demo; use Redis or DB in production)
otp_store: Dict[str, Dict] = {}

def generate_otp(email: str, expiry_seconds: int = 300) -> str:
    otp = str(secrets.randbelow(1000000)).zfill(6)
    otp_store[email] = {
        "otp": otp,
        "expires_at": time.time() + expiry_seconds
    }
    return otp

def verify_otp(email: str, submitted_otp: str) -> bool:
    record = otp_store.get(email)
    if not record:
        return False
    if time.time() > record["expires_at"]:
        del otp_store[email]
        return False
    if record["otp"] == submitted_otp:
        del otp_store[email]
        return True
    return False
