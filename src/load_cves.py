import csv
import os
from pathlib import Path

import psycopg

CLEAN_DIR = Path("data/clean")
DATABASE_URL = os.environ.get("DATABASE_URL", "dbname=vulnintel")

UPSERT_SQL = """
INSERT INTO cves (cve_id, published, status, cvss_version, score, severity, description)
VALUES (%(cve_id)s, %(published)s, %(status)s, %(cvss_version)s, %(score)s, %(severity)s, %(description)s)
ON CONFLICT (cve_id) DO UPDATE SET
    status = EXCLUDED.status,
    cvss_version = EXCLUDED.cvss_version,
    score = EXCLUDED.score,
    severity = EXCLUDED.severity,
    description =  EXCLUDED.description,
    loaded_at = now()
"""

clean_file = sorted(CLEAN_DIR.glob("cves_*.csv"))[-1]

with open(clean_file, newline="") as f:
    rows = list(csv.DictReader(f))

for row in rows:
    for key, value in row.items():
        if value == "":
            row[key] =  None

with psycopg.connect(DATABASE_URL) as conn:
    with conn.cursor() as cur:
        cur.executemany(UPSERT_SQL, rows)
        cur.execute("SELECT count(*) FROM cves")
        total = cur.fetchone()[0]

print("Loaded", len(rows), "rows from", clean_file)
print("Table now holds", total, "CVEs")