import time
from datetime import datetime
import random

def simulate_bruteforce(target_ip="127.0.0.1", port=22, attempts=10):
    users = ["admin", "root", "test", "user"]
    passwords = ["123456", "password", "admin", "toor", "letmein"]

    log_file = "logs/brute_force.log"

    with open(log_file, "a") as f:
        for i in range(attempts):
            user = random.choice(users)
            pwd = random.choice(passwords)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            result = "Failed"

            log_line = f"[{timestamp}] SSH login attempt -> {user}:{pwd} @ {target_ip}:{port} [{result}]\n"
            print(log_line.strip())
            f.write(log_line)
            time.sleep(0.2) 
def run():
    return simulate_bruteforce()