#!/usr/bin/env python3

import argparse
import sys
import traceback

from parsers import log_parser
from monitors import firewall_monitor
from engine import alerts
from engine import incidents
from engine import exporter


def handle_parsing_and_alerts(log_type: str):
    """Run parser for `log_type`, check alerts for each event,
    create incidents automatically and save/display results."""
    print(f"[*] Running parser for {log_type} logs...")
    try:
        events = log_parser.run(log_type) or []
    except Exception as e:
        print(f"[!] Parser error for {log_type}: {e}")
        traceback.print_exc()
        return

    out_path = f"outputs/{log_type}_events.json"
    print(f"[+] Log saved -> {out_path}")

    all_alerts = []
    for e in events:
        try:
            alert = alerts.check_alerts(e)
        except Exception as ex:
            print(f"[!] alert-check error for event: {ex}")
            alert = None

        if alert:
            # Ensure alert is a dict
            if not isinstance(alert, dict):
                alert = {"message": str(alert)}

            # Add original event for context
            alert.setdefault("event", e)

            # Create an incident and attach the id to alert (defensive)
            try:
                inc_payload = {
                    "type": alert.get("type", alert.get("severity", "alert")),
                    "details": alert.get("message", alert.get("event", str(e)))
                }
                inc_id = incidents.create_incident(inc_payload)
                alert["incident_id"] = inc_id
                alert["incident_created"] = True
                print(f"[+] Incident created (ID: {inc_id}) for alert -> {alert.get('message')}")
            except Exception as ex_inc:
                alert["incident_created"] = False
                print(f"[!] Failed to create incident: {ex_inc}")

            all_alerts.append(alert)

    if all_alerts:
        try:
            alerts.display_alerts(all_alerts)
        except Exception:
            # best-effort display
            print("[*] Alerts (raw):")
            for a in all_alerts:
                print(a)

        try:
            alerts.save_alerts(all_alerts)
            print("[+] Alerts saved.")
        except Exception as ex:
            print(f"[!] Failed to save alerts: {ex}")


def main():
    parser = argparse.ArgumentParser(description="SOC Toolkit CLI")
    parser.add_argument("--parse", choices=["auth", "apache", "syslog"],
                        help="Parse different log types")
    parser.add_argument("--monitor", choices=["firewall"],
                        help="Monitor logs in real-time")
    parser.add_argument("--demo", choices=["brute_force"],
                        help="Run attack demos")
    parser.add_argument("--export", choices=["elk", "graylog"],
                        help="Export collected logs")
    parser.add_argument("--version", action="store_true", help="Show version and exit")
    args = parser.parse_args()

    if args.version:
        print("SOC Toolkit - version 0.1")
        sys.exit(0)

    # --- Parsers + alerts/incidents ---
    if args.parse:
        handle_parsing_and_alerts(args.parse)

    # --- Monitor ---
    if args.monitor == "firewall":
        print("[*] Starting firewall monitor...")
        try:
            # pass a sample file path or let monitor decide default
            firewall_monitor.run("monitors/sample_firewall.log")
        except Exception as e:
            print(f"[!] Firewall monitor error: {e}")
            traceback.print_exc()

    # --- Demo ---
    if args.demo == "brute_force":
        print("[*] Running brute force demo (placeholder)...")
        # TODO: hook demo implementation or import demos.brute_force.run()

    # --- Export ---
    if args.export:
        if args.export == "elk":
            print("[*] Exporting logs to Elasticsearch...")
            try:
                # Example payload; real code should collect real events
                payload = [{"msg": "example export"}]
                exporter.export_to_elasticsearch(payload, index="soc-logs")
                print("[+] Export to ELK attempted (see exporter logs).")
            except Exception as e:
                print(f"[!] Failed to export to Elasticsearch: {e}")
        elif args.export == "graylog":
            print("[*] Exporting logs for Graylog ingestion...")
            try:
                # exporter.export_to_graylog should exist; fallback to file if not
                if hasattr(exporter, "export_to_graylog"):
                    exporter.export_to_graylog()
                else:
                    # fallback: collect sample and write using exporter.export_to_file (if available)
                    if hasattr(exporter, "export_to_file"):
                        exporter.export_to_file({"sample":"graylog"}, filename_prefix="graylog_fallback")
                        print("[+] Graylog fallback export completed.")
                    else:
                        print("[!] No graylog export function available in exporter module.")
            except Exception as e:
                print(f"[!] Graylog export error: {e}")


if __name__ == "__main__":
    main()
