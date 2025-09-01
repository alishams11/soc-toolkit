import time
import re
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def process_log_line(line):
    match = re.search(r"(\d+\.\d+\.\d+\.\d+).*-> (\d+\.\d+\.\d+\.\d+)", line)
    if match:
        src_ip, dst_ip = match.groups()
    else:
        src_ip, dst_ip = "unknown", "unknown"
    return {"src_ip": src_ip, "dst_ip": dst_ip, "raw": line.strip()}

class LogHandler(FileSystemEventHandler):
    def __init__(self, file_path):
        self.file_path = file_path
        self.position = 0

    def on_modified(self, event):
        if event.src_path.endswith(self.file_path):
            with open(self.file_path, "r") as f:
                f.seek(self.position)
                for line in f:
                    alert = process_log_line(line)
                    print(f"[ALERT] {alert}")
                self.position = f.tell()

def run(file_path="monitors/sample_firewall.log"):
    print("[*] Starting firewall log monitor (real-time)...")
    event_handler = LogHandler(file_path)
    observer = Observer()
    observer.schedule(event_handler, path="monitors", recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
