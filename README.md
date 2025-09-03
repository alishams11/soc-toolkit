# SOC Toolkit

A modular toolkit for **log parsing**, **firewall monitoring**, and **attack simulation demos**.  
The goal of this project is to simulate SOC (Security Operations Center) workflows, detect anomalies, and showcase alerting/monitoring use cases.

## 📂 Project Structure
soc-toolkit/
├── parsers/ # Log parsers (auth, apache, syslog)
├── monitors/ # Real-time log monitors (firewall)
├── demos/ # Attack simulation demos
├── engine/ # Core utils and alerting engine
├── outputs/ # Parsed logs and alerts
├── screenshots/ # Execution screenshots
├── main.py # CLI entrypoint
├── requirements.txt # Dependencies
└── LICENSE

## 🚀 Features

- **Log Parsing**
  - SSH auth logs → detect brute-force attempts
  - Apache access logs → detect suspicious login page access
  - Syslog → detect errors and failed jobs

- **Real-Time Firewall Monitoring**
  - Watch firewall logs (`iptables`-like format)
  - Raise alerts on suspicious activity
  - Save alerts in JSON format

- **Alerting Engine**
  - Simple rules (e.g., more than 5 failed logins in 5 minutes)
  - Color-coded alerts in terminal
  - Export alerts to `outputs/alerts.json`

- **Attack Demos**
  - Brute-force simulation (placeholder for now)

## ⚡ Installation

```bash
git clone https://github.com/alishams11/soc-toolkit.git
cd soc-toolkit
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

##🛠️ Usage
Log Parsing 
python3 main.py --parse auth
python3 main.py --parse apache
python3 main.py --parse syslog

Real-Time Firewall Monitoring
python3 main.py --monitor firewall

Attack Demos
python3 main.py --demo brute_force

##📊 Outputs
Parsed logs are stored in outputs/*.json
Alerts are stored in outputs/alerts.json

##📸 Examples & Screenshots
Auth Log Parsing
Apache Log Parsing
Syslog Parsing
Firewall Monitoring

##📝 License
This project is licensed under the MIT License.
