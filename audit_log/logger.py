import json
from datetime import datetime
from jsonschema import validate, ValidationError

with open("audit_log/schema.json") as f:
    schema = json.load(f)

def log_verification(entry: dict, log_path="audit_log/verification_log.jsonl"):
    entry["timestamp"] = datetime.utcnow().isoformat()

    try:
        validate(instance=entry, schema=schema)
    except ValidationError as e:
        raise ValueError(f"Invalid log entry: {e.message}")

    with open(log_path, "a") as f:
        f.write(json.dumps(entry) + "\n")