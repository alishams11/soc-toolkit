import json
import time
import os
from pathlib import Path

try:
    from elasticsearch import Elasticsearch
except ImportError:
    Elasticsearch = None

OUT_DIR = Path(__file__).resolve().parents[1] / "outputs"
OUT_DIR.mkdir(parents=True, exist_ok=True)

def _timestamp():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

def export_to_file(document: dict, filename_prefix: str = "graylog_export"):
    ts = _timestamp().replace(":", "-")
    fname = OUT_DIR / f"{filename_prefix}_{ts}.json"
    with open(fname, "w", encoding="utf-8") as f:
        json.dump(document, f, ensure_ascii=False, indent=2)
    print(f"[+] Exported to file: {fname}")
    return str(fname)

def export_to_elasticsearch(documents: list, index: str = "soc-toolkit"):
    """
    Try to export logs to Elasticsearch, fallback to JSON if not available.
    """
    if Elasticsearch:
        try:
            es = Elasticsearch("http://localhost:9200")
            if not es.ping():
                raise Exception("Elasticsearch not reachable")
            for doc in documents:
                es.index(index=index, document=doc)
            print(f"[+] Exported {len(documents)} logs to Elasticsearch index '{index}'")
            return True
        except Exception as e:
            print(f"[!] Could not connect to Elasticsearch: {e}")
    else:
        print("[!] Elasticsearch client not installed, using fallback")
    return export_to_file(documents, filename_prefix="elk_fallback")

def export_to_graylog(input_folder="outputs", output_file="outputs/graylog_ingest.json"):
    """
    Collect all logs from outputs/ and prepare a JSON file for Graylog ingestion.
    """
    all_logs = []
    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.endswith(".json"):
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        if isinstance(data, list):
                            all_logs.extend(data)
                        else:
                            all_logs.append(data)
                except Exception as e:
                    print(f"[!] Error reading {path}: {e}")

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_logs, f, indent=2)
    print(f"[+] Graylog export complete -> {output_file}")
    return output_file
