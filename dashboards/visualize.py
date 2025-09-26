import json
import matplotlib.pyplot as plt
from collections import Counter
from datetime import datetime
import plotly.express as px

def load_auth_events():
    """Load parsed auth events from outputs/auth_events.json"""
    try:
        with open("outputs/auth_events.json") as f:
            return json.load(f)
    except FileNotFoundError:
        print("[!] No auth_events.json found. Run parser first.")
        return []

def brute_force_timeline(events):
    """Plot brute-force events over time"""
    times = [datetime.fromisoformat(e["timestamp"]) for e in events]
    plt.figure(figsize=(8, 4))
    plt.hist(times, bins=10, color="red", alpha=0.7)
    plt.title("Brute-force attempts over time")
    plt.xlabel("Time")
    plt.ylabel("Attempts")
    plt.tight_layout()
    plt.savefig("screenshots/bruteforce_timeline.png")
    print("[+] Saved brute-force timeline chart -> screenshots/bruteforce_timeline.png")

def top_ips(events):
    """Plot top source IPs with Plotly"""
    ips = [e["event"].split()[-4] for e in events if "Failed password" in e["event"]]
    count = Counter(ips)
    fig = px.bar(x=list(count.keys()), y=list(count.values()), 
                 labels={"x": "Source IP", "y": "Attempts"}, 
                 title="Top Source IPs (Brute-force)")
    fig.write_image("screenshots/top_ips.png")
    print("[+] Saved top IPs chart -> screenshots/top_ips.png")

if __name__ == "__main__":
    events = load_auth_events()
    if events:
        brute_force_timeline(events)
        top_ips(events)
