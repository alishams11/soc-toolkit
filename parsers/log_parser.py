import re
import json
import os
from datetime import datetime

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def parse_auth_log(log_file):
    """Parse SSH authentication logs (auth.log)"""
    pattern = re.compile(r'(?P<timestamp>\w{3}\s+\d+\s[\d:]+)\s.*sshd.*Failed password for (?P<user>\w+) from (?P<ip>[\d.]+)')
    results = []

    with open(log_file, "r") as f:
        for line in f:
            match = pattern.search(line)
            if match:
                results.append({
                    "timestamp": match.group("timestamp"),
                    "attack_type": "ssh_bruteforce",
                    "user": match.group("user"),
                    "source_ip": match.group("ip"),
                    "status": "failed"
                })
    return results


def parse_apache_log(log_file):
    """Parse Apache access logs"""
    pattern = re.compile(r'(?P<ip>[\d.]+) - - \[(?P<timestamp>.+?)\] "(?P<method>\w+) (?P<url>\S+)')
    results = []

    with open(log_file, "r") as f:
        for line in f:
            match = pattern.search(line)
            if match:
                results.append({
                    "timestamp": match.group("timestamp"),
                    "attack_type": "web_access",
                    "method": match.group("method"),
                    "url": match.group("url"),
                    "source_ip": match.group("ip"),
                    "status": "success"
                })
    return results


def parse_syslog(log_file):
    """Parse generic syslog entries"""
    results = []
    with open(log_file, "r") as f:
        for line in f:
            if "error" in line.lower() or "fail" in line.lower():
                results.append({
                    "timestamp": datetime.now().isoformat(),
                    "attack_type": "system_error",
                    "message": line.strip(),
                    "status": "alert"
                })
    return results


def save_results(filename, data):
    """Save parsed logs to JSON in outputs/"""
    output_path = os.path.join(OUTPUT_DIR, filename)
    with open(output_path, "w") as f:
        json.dump(data, f, indent=4)
    print(f"[+] Saved {len(data)} events to {output_path}")


if __name__ == "__main__":
    auth_logs = parse_auth_log("sample_logs/auth.log") if os.path.exists("sample_logs/auth.log") else []
    apache_logs = parse_apache_log("sample_logs/access.log") if os.path.exists("sample_logs/access.log") else []
    sys_logs = parse_syslog("sample_logs/syslog") if os.path.exists("sample_logs/syslog") else []

    all_data = auth_logs + apache_logs + sys_logs
    save_results("parsed_logs.json", all_data)
