import socket
from datetime import datetime

def simulate_port_scan(target_ip="127.0.0.1", ports=range(20, 30)):
    log_file = "logs/port_scan.log"

    with open(log_file, "a") as f:
        for port in ports:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.5)
                result = s.connect_ex((target_ip, port))
                s.close()

                status = "OPEN" if result == 0 else "CLOSED"
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_line = f"[{timestamp}] Port {port} on {target_ip} -> {status}\n"

                print(log_line.strip())
                f.write(log_line)

            except Exception as e:
                print(f"[!] Error scanning port {port}: {e}")
def run():
    return simulate_port_scan()