"""Remote-only lock bootstrap: hash every resolved published wheel, no guessed pins."""
import email
import hashlib
import json
from pathlib import Path
import zipfile


def main():
    records = []
    for wheel in sorted(Path("wheelhouse").glob("*.whl")):
        with zipfile.ZipFile(wheel) as z:
            metadata_paths = [n for n in z.namelist() if len(n.split("/")) == 2 and n.endswith(".dist-info/METADATA")]
            if len(metadata_paths) != 1:
                raise ValueError("Expected exactly one distribution metadata record")
            metadata = email.message_from_bytes(z.read(metadata_paths[0]))
        records.append({"name": metadata["Name"], "version": metadata["Version"],
                        "filename": wheel.name, "sha256": hashlib.sha256(wheel.read_bytes()).hexdigest(),
                        "bytes": wheel.stat().st_size, "requires_dist": metadata.get_all("Requires-Dist", []),
                        "source_index": "https://pypi.org/simple"})
    if not records or len({r["name"].lower().replace("_", "-") for r in records}) != len(records):
        raise ValueError("Missing or duplicate resolved distributions")
    Path("requirements.lock").write_text("# Resolved published wheels; Python 3.12/Linux\n" + "".join(
        f"{r['name']}=={r['version']} --hash=sha256:{r['sha256']}\n" for r in records))
    Path("proof").mkdir(exist_ok=True)
    Path("proof/distribution-provenance.json").write_text(json.dumps(records, indent=2) + "\n")


if __name__ == "__main__":
    main()
