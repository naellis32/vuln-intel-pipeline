import subprocess
import sys

STEPS = [
    "src/fetch_cves.py",
    "src/transform_cves.py",
    "src/load_cves.py",
]

for step in STEPS:
    print()
    print("=== Running", step, "===")
    subprocess.run([sys.executable, step], check=True)

print()
print("Pipeline finished.")