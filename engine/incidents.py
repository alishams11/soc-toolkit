import json
from pathlib import Path
from datetime import datetime

INCIDENTS_FILE = Path(__file__).resolve().parents[1] / "outputs/incidents.json"

def load_incidents():
    if INCIDENTS_FILE.exists():
        with open(INCIDENTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_incidents(incidents):
    INCIDENTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(INCIDENTS_FILE, "w", encoding="utf-8") as f:
        json.dump(incidents, f, indent=2)

def create_incident(alert: dict):
    incidents = load_incidents()
    new_incident = {
        "id": len(incidents) + 1,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "alert": alert,
        "status": "open"
    }
    incidents.append(new_incident)
    save_incidents(incidents)
    print(f"[+] Incident created (ID: {new_incident['id']})")
    return new_incident

def update_incident(incident_id: int, status: str):
    incidents = load_incidents()
    for inc in incidents:
        if inc["id"] == incident_id:
            inc["status"] = status
            save_incidents(incidents)
            print(f"[+] Incident {incident_id} updated -> {status}")
            return inc
    print(f"[!] Incident {incident_id} not found")
    return None
