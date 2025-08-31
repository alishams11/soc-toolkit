import re
import os
from engine import utils

LOG_DIR = "parsers/sample_logs"

def parse_auth_log():
    filepath = os.path.join(LOG_DIR, "auth.log")
    if not os.path.exists(filepath):
        return

    with open(filepath, "r") as f:
        for line in f:
            match = re.search(r"Failed password for (\w+) from ([\d\.]+)", line)
            if match:
                user, ip = match.groups()
                log_entry = utils.format_log(
                    source_ip=ip,
                    dest_ip="localhost",
                    attack_type="ssh_bruteforce",
                    status=f"failed login for {user}"
                )
                utils.save_log(log_entry, "auth_events.json")

def parse_access_log():
    filepath = os.path.join(LOG_DIR, "access.log")
    if not os.path.exists(filepath):
        return

    with open(filepath, "r") as f:
        for line in f:
            match = re.search(r'([\d\.]+).*"GET (.*?) HTTP', line)
            if match:
                ip, path = match.groups()
                log_entry = utils.format_log(
                    source_ip=ip,
                    dest_ip="localhost",
                    attack_type="web_access",
                    status=f"GET {path}"
                )
                utils.save_log(log_entry, "access_events.json")

def parse_syslog():
    filepath = os.path.join(LOG_DIR, "syslog")
    if not os.path.exists(filepath):
        return

    with open(filepath, "r") as f:
        for line in f:
            if "error" in line.lower():
                log_entry = utils.format_log(
                    source_ip="localhost",
                    dest_ip="localhost",
                    attack_type="system_error",
                    status=line.strip()
                )
                utils.save_log(log_entry, "syslog_events.json")

def run():
    print("[*] Parsing logs...")
    parse_auth_log()
    parse_access_log()
    parse_syslog()
    print("[+] Parsing finished.")

if __name__ == "__main__":
    run()
