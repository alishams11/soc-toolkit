import json
import os
from datetime import datetime

def format_log(source_ip, dest_ip, attack_type, status):
    """
    Create a standardized JSON log structure
    """
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "source_ip": source_ip,
        "destination_ip": dest_ip,
        "attack_type": attack_type,
        "status": status
    }
    return log_entry

def save_log(log_entry, filename="events.json"):
    """
    Save logs in outputs/<filename>
    """
    os.makedirs("outputs", exist_ok=True)
    filepath = os.path.join("outputs", filename)

    with open(filepath, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

    print(f"[+] Log saved -> {filepath}")
