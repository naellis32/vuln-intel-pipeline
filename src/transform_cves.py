import csv
import json
from pathlib import Path

RAW_DIR = Path("data/raw")
CLEAN_DIR = Path("data/clean")
METRIC_VERSIONS = ["cvssMetricV40", "cvssMetricV31", "cvssMetricV30", "cvssMetricV2"]
COLUMNS = ["cve_id", "published", "status", "cvss_version", "score", "severity", "description"]


def get_severity(cve):
    metrics = cve.get("metrics", {})
    for version in METRIC_VERSIONS:
        if version in metrics:
            metric = metrics[version][0]
            cvss = metric["cvssData"]
            score = cvss.get("baseScore")
            severity = cvss.get("baseSeverity") or metric.get("baseSeverity")
            return cvss.get("version"), score, severity
    return None, None, "UNSCORED"


def get_description(cve):
    for entry in cve.get("descriptions", []):
        if entry["lang"] == "en":
            return " ".join(entry["value"].split())
    return ""


raw_file = sorted(RAW_DIR.glob("cves_*.json"))[-1]

with open(raw_file) as f:
    cves = json.load(f)

rows = []
for item in cves:
    cve = item["cve"]
    cvss_version, score, severity = get_severity(cve)

    row = {
        "cve_id": cve["id"],
        "published": cve["published"],
        "status": cve.get("vulnStatus"),
        "cvss_version": cvss_version,
        "score": score,
        "severity": severity,
        "description": get_description(cve),
    }

    rows.append(row)

CLEAN_DIR.mkdir(parents=True, exist_ok=True)
clean_file = CLEAN_DIR / raw_file.name.replace(".json", ".csv")

with open(clean_file, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=COLUMNS)
    writer.writeheader()
    writer.writerows(rows)

print("Read", len(cves), "CVEs from", raw_file)
print("Wrote", len(rows), "rows to", clean_file)