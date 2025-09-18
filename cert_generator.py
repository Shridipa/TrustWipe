import uuid
import hashlib
import json
from datetime import datetime

def normalize_device_type(device_type_raw):
    """Normalize device type input to standard labels."""
    device_type = device_type_raw.strip().lower()
    if device_type in ["hdd", "hard disk drive", "hard drive"]:
        return "HDD"
    elif device_type in ["ssd", "solid state drive"]:
        return "SSD"
    else:
        return "Unknown"

def select_wipe_method(device_type):
    """Choose appropriate wipe method based on device type."""
    if device_type == "HDD":
        return "NIST Clear"
    elif device_type == "SSD":
        return "NIST Purge"
    else:
        return "Standard Wipe"

def generate_certificate(wipe_logs, device_info, technician):
    # Normalize device type
    raw_type = device_info.get("storage_type", "")
    device_type = normalize_device_type(raw_type)

    # Select appropriate wipe method
    method = select_wipe_method(device_type)

    # Build certificate dictionary
    cert = {
        "certificate_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat(),
        "device": {
            "make": device_info.get("make", "Unknown"),
            "model": device_info.get("model", "Unknown"),
            "serial_number": device_info.get("serial_number", "Unknown"),
            "storage_type": device_type
        },
        "wipe_method": method,
        "technician": technician,
        "log_hash": hashlib.sha256(wipe_logs.encode()).hexdigest()
    }

    return cert
