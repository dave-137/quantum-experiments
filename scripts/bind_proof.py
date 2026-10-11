"""Bind remote outputs to a tracked source inventory, revision and resolved lock."""
import hashlib
import json
import os
import platform
from pathlib import Path
import subprocess


def main():
    files = subprocess.check_output(["git", "ls-files", "-z"]).decode().split("\0")
    inventory = []
    for name in sorted(n for n in files if n and n != ".gitkeep"):
        p = Path(name)
        if p.is_symlink() or not p.is_file():
            raise ValueError("Proof source must be regular tracked files")
        inventory.append({"path": name, "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
                          "bytes": p.stat().st_size, "mode": ("0755" if p.stat().st_mode & 0o111 else "0644")})
    encoded = json.dumps(inventory, sort_keys=True, separators=(",", ":")).encode()
    binding = {"candidate_digest": hashlib.sha256(encoded).hexdigest(), "inventory": inventory,
               "revision": subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip(),
               "lock_sha256": hashlib.sha256(Path("requirements.lock").read_bytes()).hexdigest(),
               "python": platform.python_version(), "platform": platform.platform(),
               "job": {k: os.environ.get(k) for k in ["GITHUB_REPOSITORY", "GITHUB_RUN_ID", "GITHUB_RUN_ATTEMPT", "GITHUB_JOB"]}}
    Path("proof").mkdir(exist_ok=True)
    Path("proof/binding.json").write_text(json.dumps(binding, indent=2) + "\n")


if __name__ == "__main__":
    main()
