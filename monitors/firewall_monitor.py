import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from engine import utils

LOG_FILE = "monitors/sample_firewall.log"

class FirewallHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(LOG_FILE):
            with open(LOG_FILE, "r") as f:
                for line in f.readlines()[-5:]: 
                    if "DROP" in line or "DENY" in line:
                        print(f"[ALERT] Suspicious firewall log: {line.strip()}")
                        log_entry = utils.format_log(
                            source_ip=line.split()[6],
                            dest_ip=line.split()[8],
                            attack_type="firewall_block",
                            status=line.strip()
                        )
                        utils.save_log(log_entry, "firewall_alerts.json")

def run():
    print("[*] Starting firewall log monitor (real-time)...")
    event_handler = FirewallHandler()
    observer = Observer()
    observer.schedule(event_handler, path="monitors", recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    run()
