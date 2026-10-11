"""Installed wheel consumer proof from outside the source checkout."""
import importlib
import importlib.metadata
import json
from pathlib import Path
import subprocess
import sys
import tempfile


def main():
    for name in ["bell_chsh", "damping_sweep", "qaoa_maxcut", "zne_landscape"]:
        importlib.import_module("quantum_experiments." + name)
    with tempfile.TemporaryDirectory() as directory:
        completed = subprocess.run([sys.executable, "-m", "quantum_experiments", "bell",
                                    "--shots", "75", "--out", "bell"],
                                   cwd=directory, check=True, capture_output=True, text=True)
        r = json.loads((Path(directory) / "bell/report.json").read_text())
        assert r["trials"] == 75 and r["metadata"]["mode"] == "simulation"
    Path("proof/consumer.json").write_text(json.dumps({
        "distribution": importlib.metadata.version("quantum-experiments"),
        "imported_studies": 4, "outside_checkout_cli": True, "trial_count": 75,
        "stdout_summary": json.loads(completed.stdout)}, indent=2) + "\n")


if __name__ == "__main__":
    main()
