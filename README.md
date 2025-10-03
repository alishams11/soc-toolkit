# SOC Toolkit — v1.0 🚀

A modular toolkit for **log parsing**, **firewall monitoring**, and **attack simulation demos**.  
The goal of this project is to **simulate SOC workflows**, detect anomalies, and provide hands-on practice for SOC analysts.  


## 📂 Project Structure  

```
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
```

---

## 🚀 Features  

- **Log Parsing**  
  - SSH auth logs → detect brute-force attempts  
  - Apache access logs → detect suspicious login attempts  
  - Syslog → catch errors and failed jobs  

- **Firewall Monitoring**  
  - Watch real-time logs (iptables-style)  
  - Detect suspicious scans or unusual traffic  
  - Export alerts to `outputs/alerts.json`  

- **Alerting Engine**  
  - Rule-based detection (e.g. >5 failed logins in 5 min)  
  - Color-coded CLI alerts  
  - JSON alerts for dashboards/analysis  

- **Attack Demos**  
  - Brute-force simulation (extendable)  

---

## 🎯 Why It’s Useful for SOC Analysts  

- Practice **incident triage** with real log samples  
- Learn **alert engineering** & rule-tuning  
- Understand **log → parse → alert → dashboard** pipeline  
- Use outputs for **hunting exercises** or dashboards (ELK/Grafana)  

---

## ⚡ Installation  

```bash
git clone https://github.com/alishams11/soc-toolkit.git
cd soc-toolkit
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🛠️ Usage  

### Log Parsing  
```bash
python3 main.py --parse auth --input demos/sample_auth.log --output outputs/auth.json
python3 main.py --parse apache --input demos/sample_apache.log --output outputs/apache.json
python3 main.py --parse syslog --input demos/sample_syslog.log --output outputs/syslog.json
```

### Firewall Monitoring  
```bash
python3 main.py --monitor firewall --live demos/firewall_stream.log
```

### Attack Demo  
```bash
python3 main.py --demo brute_force
```

---

## 📊 Outputs  

- Parsed logs → `outputs/*.json`  
- Alerts → `outputs/alerts.json`  

**Example alert JSON:**  
```json
{
  "timestamp": "2025-10-03T09:12:34Z",
  "rule": "ssh_bruteforce",
  "src_ip": "10.10.10.55",
  "count": 7,
  "window_minutes": 5,
  "details": "7 failed attempts on /var/log/auth.log"
}
```

---

## 📸 Screenshots  

- `screenshots/cli_auth_parsing.png` → SSH log parsing example  
- `screenshots/cli_firewall_monitor.png` → Firewall monitoring alerts  
- `screenshots/dashboard_auth_alerts.png` → Optional Grafana/Kibana visualization  

---

## 📝 License  

This project is licensed under the **MIT License**.  
