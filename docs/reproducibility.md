# Reproducibility

## Source pins and runtime versions

The source pins identify the examples adapted, not the installed distributions. Cirq source reports a development version; Mitiq source declares 1.1.0. Published compatible packages are resolved remotely instead of assuming those source versions are released. The shared Python 3.12/Linux bootstrap bounds Cirq to 1.6.x, Mitiq to >=1.0,<1.2 and NumPy to >=2,<2.3; all transitive runtime/test/notebook dependencies are locked after resolution.

## Hash-locked bootstrap

On a clean disposable runner, from the source root:

```bash
python -m pip --isolated download --index-url https://pypi.org/simple --only-binary=:all: --dest wheelhouse -r requirements.in
python scripts/lock_wheels.py
python -m pip --isolated install --no-index --find-links wheelhouse --require-hashes -r requirements.lock
python -m pip check
python scripts/bind_proof.py
python -m pip --isolated wheel --no-deps --no-build-isolation . --wheel-dir dist
python -m pip --isolated install --no-deps --no-index dist/*.whl
python -m pytest -q --junitxml=proof/pytest.xml
quantum-experiments bell --out results/bell --binding proof/binding.json
quantum-experiments damping --out results/damping --binding proof/binding.json
quantum-experiments qaoa --out results/qaoa --binding proof/binding.json
quantum-experiments zne --out results/zne --binding proof/binding.json
python scripts/execute_notebooks.py
python scripts/consumer_smoke.py
python scripts/validate_reports.py
```

`bind_proof.py` requires a Git source checkout to record the exact revision. It hashes sorted tracked regular files (excluding the inert `.gitkeep` marker) as path/sha256/bytes/Git-mode records (0644 or 0755), encoded as canonical JSON. It also records the resolved lock hash and public job identifiers. Notebooks receive the same binding from `proof/binding.json`. Exploratory runs without that file are explicitly marked unbound.

The lock contains exact versions and hashes of the actual resolved wheels. Provenance records wheel filenames, dependency metadata, sizes, hashes and source index. The published `requirements.lock` and `results/proof/distribution-provenance.json` are the genuine resolution from run38178146290. Keep the lock and distribution-provenance artifact together; repeat the exact locked install rather than re-resolving for comparisons. Platform-specific wheel hashes target the disclosed runner environment.

## Remote proof artifact

The `Simulation proof` workflow runs on pull requests and can also be started manually after reaching the default branch. It checks out the exact feature head and uses one GitHub-hosted job, contents:read and immutable action revisions. It does not use secrets, hardware accounts or pull_request_target. The accepted run used a 13-minute job timeout within the 15-minute aggregate proof ceiling. Three jobs used 12, 58 and 102 seconds (172 seconds total; minute-rounded accounting 1 + 1 + 2 = 4 minutes). GitHub timing reported zero billable milliseconds for the latter two public-runner jobs.

The `simulation-proof` artifact contains requirements.lock, the built candidate wheel, source/environment binding, test XML, installed-consumer proof, clean-kernel notebooks, eight script/notebook simulation reports and their original output hashes. Default commands run all four full studies, including the complete 50-point ZNE sweep. A successful job does not itself replace visual inspection.

For exact-head acceptance, compare the binding inventory to the reviewed source, verify job/log IDs and lock/packages, then inspect plots and rendered notebooks for axes, legends, clipping, duplicate images and consistency with JSON/CSV arrays. Resource accounting combines the workflow’s timed proof phase with GitHub job timing. Published output and notebook commits retain the binding to the executed source revision; they do not imply those outputs were generated from their own later commit. The output-publication commit skips CI to avoid repeating an unchanged successful computational source.

## Seeds and output portability

The full defaults are recorded in [methods](methods.md). Finite-shot outputs are reproducible within the exact environment; different distribution versions may change samples or optimizer trajectories. ZNE uses density-matrix expectations rather than sampled shots. Report generation timestamps and image metadata can change hashes between reruns while numerical arrays remain reproducible. Output hashes bind each individual run; they are not cross-run equality claims.
