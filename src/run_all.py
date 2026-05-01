"""
run_all.py
──────────
Runs all data preparation scripts in the correct order.
After running this, all processed CSVs are ready for Power BI.

Usage:
    python src/run_all.py
"""

import subprocess
import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent

SCRIPTS = [
    "prepare_data.py",
    "prepare_global.py",
    "prepare_viz.py",
    "prepare_demographics.py",
    "prepare_tipping_points.py",
]

print("=" * 50)
print("Climate Population Analysis — Data Pipeline")
print("=" * 50)

for script in SCRIPTS:
    path = SRC_DIR / script
    print(f"\n▶ Running {script}...")
    result = subprocess.run([sys.executable, str(path)], capture_output=False)
    if result.returncode != 0:
        print(f"❌ {script} failed — stopping pipeline.")
        sys.exit(1)

print("\n" + "=" * 50)
print("✅ All scripts completed. Processed CSVs ready.")
print("=" * 50)