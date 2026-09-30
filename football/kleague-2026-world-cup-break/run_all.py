"""Run all four stages in order, using separate Python processes."""
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parent
for script in sorted((root / "scripts").glob("v[1-4]_*.py")):
    print(f"Running {script.name}", flush=True)
    subprocess.run([sys.executable, str(script)], cwd=root, check=True)
print("Completed all stages. Results are in outputs/ unless KLEAGUE_OUTPUT_DIR was set.")
