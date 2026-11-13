import json

from pathlib import Path

from datetime import datetime, timedelta, timezone

import time

import requests

URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"

DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.000"

end = datetime.now(timezone.utc)
start = end - timedelta(days=7)

PAGE_SIZE = 2000

all_cves = []
start_index = 0

while True:
    params = {
        "pubStartDate": start.strftime(DATE_FORMAT),
        "pubEndDate": end.strftime(DATE_FORMAT),
        "resultsPerPage": PAGE_SIZE,
        "startIndex": start_index,
    }

    response = requests.get(URL, params=params, timeout=60)
    response.raise_for_status()
    data = response.json()

    all_cves.extend(data["vulnerabilities"])
    print("Fetched", len(all_cves), "of", data["totalResults"])

    start_index += PAGE_SIZE

    if start_index >= data["totalResults"]:
        break

    time.sleep(6)

output_dir = Path("data/raw")
output_dir.mkdir(parents=True, exist_ok=True)
output_file = output_dir / f"cves_{end.strftime('%Y-%m-%d')}.json"

with open(output_file, "w") as f:
    json.dump(all_cves, f)

print("Saved", len(all_cves), "CVEs to", output_file)