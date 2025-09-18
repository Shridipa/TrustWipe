def parse_log(file_path: str) -> dict:
    with open(file_path, "r") as f:
        lines = f.readlines()
    # Example: extract metadata from log
    return {
        "device_id": lines[0].strip(),
        "timestamp": lines[1].strip(),
        "status": lines[-1].strip()
    }