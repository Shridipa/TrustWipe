import pytest
import json
from local_verifier.verify import verify_certificate

# Sample valid certificate
valid_cert = {
    "data": {
        "certificate_id": "ABC123",
        "device_id": "DEVICE001",
        "timestamp": "2025-09-18T09:00:00Z"
    },
    "signature": "..."  # Replace with actual hex signature
}

# Sample invalid certificate (tampered data)
invalid_cert = {
    "data": {
        "certificate_id": "ABC123",
        "device_id": "DEVICE001",
        "timestamp": "2025-09-18T09:00:00Z"
    },
    "signature": "deadbeef"  # Invalid hex
}

def test_valid_certificate():
    result = verify_certificate(valid_cert, "certs/issuer_public.pem")
    assert result["valid"] is True
    assert "certificate_id" in result
    assert "hash" in result

def test_invalid_signature():
    result = verify_certificate(invalid_cert, "certs/issuer_public.pem")
    assert result["valid"] is False
    assert "reason" in result

def test_missing_fields():
    result = verify_certificate({}, "certs/issuer_public.pem")
    assert result["valid"] is False
    assert result["reason"] == "Missing data or signature"