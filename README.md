SOC Toolkit — v1.0 🚀

A modular toolkit for log parsing, firewall monitoring, and attack-simulation demos.
This project is designed to simulate SOC workflows, detect anomalies, and provide a playground for SOC analysts to practice detection, triage, and monitoring.
🎯 Why It’s Useful for SOC Analysts (Use Cases)

Incident Triage Practice → simulate common alerts (e.g., brute-force, suspicious HTTP access, port scans).

Alert Engineering → experiment with simple detection rules and understand false positives/negatives.

Pipeline Understanding → see how logs are parsed, normalized, and transformed into alerts.

Hunting Exercises → parse outputs and practice queries for IOCs in a lab environment.

Dashboard Feeds → export alerts to ELK/Grafana for visualization.
##📂 Project Structure
soc-toolkit/
├── parsers/        # Log parsers (auth, apache, syslog)
├── monitors/       # Real-time log monitors (firewall)
├── demos/          # Attack simulation demos
├── engine/         # Core utilities & alerting engine
├── outputs/        # Parsed logs and alerts
├── screenshots/    # Execution screenshots
├── main.py         # CLI entrypoint
├── requirements.txt# Dependencies
└── LICENSE
##🚀 Features
Log Parsing
SSH auth logs → detect brute-force attempts
Apache access logs → detect suspicious login activity
Syslog → detect errors & failed jobs

Real-Time Firewall Monitoring
Watch live firewall logs (iptables-like format)
Raise alerts on suspicious scans & anomalies
Export alerts as JSON

Alerting Engine
Rules: e.g., 5 failed SSH logins in 5 minutes
Color-coded alerts in terminal
Alerts stored in outputs/alerts.json

Attack Demos
Brute-force simulation (expandable for more scenarios)

##⚡ Installation
git clone https://github.com/alishams11/soc-toolkit.git
cd soc-toolkit
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

##🛠️ Usage
1) Parse Logs
# SSH Auth log parsing
python3 main.py --parse auth --input demos/sample_auth.log --output outputs/auth.json
# Apache log parsing
python3 main.py --parse apache --input demos/sample_apache.log --output outputs/apache.json
# Syslog parsing
python3 main.py --parse syslog --input demos/sample_syslog.log --output outputs/syslog.json

2) Real-Time Firewall Monitoring
python3 main.py --monitor firewall --live demos/firewall_stream.log

3) Run Attack Demo
python3 main.py --demo brute_force

##📊 Outputs
Parsed logs → outputs/*.json
Alerts → outputs/alerts.json
Sample Alert JSON
{
  "timestamp": "2025-10-03T09:12:34Z",
  "rule": "ssh_bruteforce",
  "src_ip": "10.10.10.55",
  "count": 7,
  "window_minutes": 5,
  "details": "7 failed attempts on /var/log/auth.log"
}
##📸 Examples & Screenshots
screenshots/cli_auth_parsing.png → CLI run with SSH brute-force detection
screenshots/cli_firewall_monitor.png → Real-time firewall monitoring alerts
screenshots/dashboard_auth_alerts.png → Alerts visualized in Grafana/Kibana

##📝 License
This project is licensed under the MIT License.
