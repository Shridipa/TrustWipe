import json, hashlib
from .signature_utils import load_public_key, verify_signature

def compute_hash(data: dict) -> str:
    raw = json.dumps(data, sort_keys=True).encode('utf-8')
    return hashlib.sha256(raw).hexdigest()

def verify_certificate(cert: dict, public_key_path: str) -> dict:
    data = cert.get("data")
    signature = cert.get("signature")

    if not data or not signature:
        return {"valid": False, "reason": "Missing data or signature"}

    hash_val = compute_hash(data)
    public_key = load_public_key(public_key_path)

    try:
        is_valid = verify_signature(public_key, bytes.fromhex(signature), hash_val.encode())
        return {
            "valid": is_valid,
            "certificate_id": data.get("certificate_id"),
            "hash": hash_val
        }
    except Exception as e:
        return {"valid": False, "reason": str(e)}