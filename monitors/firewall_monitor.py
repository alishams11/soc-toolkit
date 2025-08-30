import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import re

ALERT_LOG = "outputs/alerts.log"
FIREWALL_LOG = "monitors/sample_firewall.log" 

class LogHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith("sample_firewall.log"):
            with open(FIREWALL_LOG, "r") as f:
                lines = f.readlines()
                last_line = lines[-1].strip()

                if "DROP" in last_line or "DENY" in last_line:
                    alert = f"[ALERT] Suspicious firewall log detected: {last_line}"
                    print(alert)
                    with open(ALERT_LOG, "a") as log_file:
                        log_file.write(alert + "\n")

def start_monitor():
    print("[*] Starting firewall log monitor (real-time)...")
    event_handler = LogHandler()
    observer = Observer()
    observer.schedule(event_handler, path="monitors/", recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    start_monitor()
