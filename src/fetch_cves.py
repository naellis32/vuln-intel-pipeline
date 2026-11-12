import requests

URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"

params = {
    "pubStartDate": "2026-11-01T00:00:00.000",
    "pubEndDate": "2026-11-08T00:00:00.000",
    "resultsPerPage": 5,
}

response = requests.get(URL, params=params, timeout=30)
response.raise_for_status()
data = response.json()

print("Total CVEs in this total range:", data["totalResults"])

for item in data["vulnerabilities"]:
    cve = item["cve"]
    description = cve["descriptions"][0]["value"]
    print(cve["id"], "|", cve["published"], "|", description)