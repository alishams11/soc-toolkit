import argparse
from parsers import log_parser
from monitors import firewall_monitor

def main():
    parser = argparse.ArgumentParser(description="SOC Toolkit CLI")
    parser.add_argument("--parse", choices=["auth", "apache", "syslog"], help="Parse different log types")
    parser.add_argument("--monitor", choices=["firewall"], help="Monitor logs in real-time")
    parser.add_argument("--demo", choices=["brute_force"], help="Run attack demos")
    args = parser.parse_args()

    if args.parse:
        print(f"[*] Running parser for {args.parse} logs...")
        log_parser.run(args.parse)
        print(f"[+] Log saved -> outputs/{args.parse}_events.json")

    if args.monitor == "firewall":
        print("[*] Starting firewall monitor...")
        firewall_monitor.run("monitors/sample_firewall.log")

    if args.demo == "brute_force":
        print("[*] Running brute force demo (placeholder)...")
        # TODO: Add brute force demo functionality
        print("Brute force demo would run here")

if __name__ == "__main__":
    main()