# app.py
import json
from cert_generator import generate_certificate

# Sample wipe log (in real use, read from a log file)
wipe_log = "Wipe started...\nPass 1 complete\nPass 2 complete\nWipe finished."

# Device and technician info
device_info = {
    "serial_number": "SN987654321",
    "make": "Seagate",
    "model": "Barracuda 2TB",
    "storage_type": "HDD"
}

method = "NIST Clear"
technician = {
    "technician_id": "tech-007",
    "signature": "TrustWipeSystem"
}

# Generate certificate
certificate = generate_certificate(wipe_log, device_info, method, technician)

# Save to JSON file
filename = f"certificates/{certificate['certificate_id']}.json"
with open(filename, 'w') as f:
    json.dump(certificate, f, indent=4)

print(f"Certificate saved to {filename}")
