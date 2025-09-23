import argparse
from parsers import log_parser
from monitors import firewall_monitor
from engine import alerts
from engine import exporter

def main():
    parser = argparse.ArgumentParser(description="SOC Toolkit CLI")
    parser.add_argument("--parse", choices=["auth", "apache", "syslog"], help="Parse different log types")
    parser.add_argument("--monitor", choices=["firewall"], help="Monitor logs in real-time")
    parser.add_argument("--demo", choices=["brute_force"], help="Run attack demos")
    parser.add_argument("--export", choices=["elk", "graylog"], help="Export collected logs")
    args = parser.parse_args()

    # --- Parsers ---
    if args.parse:
        print(f"[*] Running parser for {args.parse} logs...")
        events = log_parser.run(args.parse)
        print(f"[+] Log saved -> outputs/{args.parse}_events.json")

        # Alert handling
        all_alerts = []
        for e in events:
            alert = alerts.check_alerts(e)
            if alert:
                all_alerts.append(alert)
        if all_alerts:
            alerts.display_alerts(all_alerts)
            alerts.save_alerts(all_alerts)

    # --- Monitor ---
    if args.monitor == "firewall":
        print("[*] Starting firewall monitor...")
        firewall_monitor.run("monitors/sample_firewall.log")

    # --- Demo ---
    if args.demo == "brute_force":
        print("[*] Running brute force demo (placeholder)...")

    # --- Export ---
    if args.export == "elk":
        print("[*] Exporting logs to Elasticsearch...")
        try:
            exporter.export_to_elasticsearch("soc-logs", [{"msg": "test export"}])
        except Exception as e:
            print(f"[!] Failed to export to Elasticsearch: {e}")

    if args.export == "graylog":
        print("[*] Exporting logs for Graylog ingestion...")
        exporter.export_to_graylog()

if __name__ == "__main__":
    main()
