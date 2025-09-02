import json
import os
from colorama import Fore, Style
from datetime import datetime

ALERT_FILE = "outputs/alerts.json"

def check_alerts(event):
    
    log_type = event.get("log_type", "")
    message = event.get("event", "")

    if log_type == "auth" and "Failed password" in message:
        return {
            "timestamp": str(datetime.now()),
            "severity": "HIGH",
            "message": f"Multiple failed login detected: {message}"
        }

    if log_type == "syslog" and "error" in message.lower():
        return {
            "timestamp": str(datetime.now()),
            "severity": "MEDIUM",
            "message": f"Syslog error detected: {message}"
        }

    if log_type == "apache" and "login" in message.lower():
        return {
            "timestamp": str(datetime.now()),
            "severity": "LOW",
            "message": f"Apache suspicious login page access: {message}"
        }

    return None


def display_alerts(alerts):
    
    for alert in alerts:
        severity = alert["severity"]
        color = Fore.RED if severity == "HIGH" else (Fore.YELLOW if severity == "MEDIUM" else Fore.CYAN)
        print(color + f"[ALERT] {severity}: {alert['message']}" + Style.RESET_ALL)


def save_alerts(alerts):
   
    os.makedirs("outputs", exist_ok=True)
    if os.path.exists(ALERT_FILE):
        with open(ALERT_FILE, "r") as f:
            existing = json.load(f)
    else:
        existing = []

    existing.extend(alerts)

    with open(ALERT_FILE, "w") as f:
        json.dump(existing, f, indent=2)
