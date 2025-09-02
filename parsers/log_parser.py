import json
import os
from datetime import datetime

def run(log_type):
    events = []
    folder = f"outputs/{log_type}"
    os.makedirs(folder, exist_ok=True)

    if log_type == "auth":
        filename = "auth_events.json"
        with open("parsers/sample_logs/auth.log") as f:
            for line in f:
                if "Failed password" in line:
                    events.append({
                        "timestamp": str(datetime.now()),
                        "log_type": "auth",
                        "event": line.strip()
                    })

    elif log_type == "apache":
        filename = "access_events.json"
        with open("parsers/sample_logs/access.log") as f:
            for line in f:
                if "GET" in line or "POST" in line:
                    events.append({
                        "timestamp": str(datetime.now()),
                        "log_type": "apache",
                        "event": line.strip()
                    })

    elif log_type == "syslog":
        filename = "syslog_events.json"
        with open("parsers/sample_logs/syslog") as f:
            for line in f:
                if "error" in line or "failed" in line:
                    events.append({
                        "timestamp": str(datetime.now()),
                        "log_type": "syslog",
                        "event": line.strip()
                    })

    else:
        print("[!] Unknown log type")
        return 0

    with open(f"{folder}/{filename}", "w") as f:
        json.dump(events, f, indent=2)

    return events
