# cert_generator.py
import uuid, hashlib, json
from datetime import datetime

def generate_certificate(wipe_logs, device_info, method, technician):
    cert = {
        "certificate_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat(),
        "device": device_info,
        "wipe_method": method,
        "technician": technician,
        "log_hash": hashlib.sha256(wipe_logs.encode()).hexdigest()
    }
    return cert
