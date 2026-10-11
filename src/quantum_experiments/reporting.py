"""Portable serialization/presentation glue; numerical studies live in donor adapters."""
import csv
import hashlib
import importlib.metadata
import json
import platform
from datetime import datetime, timezone
from pathlib import Path

import matplotlib.pyplot as plt


def save_report(study, data, output, binding=None):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    versions = {name: importlib.metadata.version(name) for name in
                ["cirq-core", "mitiq", "numpy", "scipy", "networkx", "matplotlib"]}
    data = dict(data)
    data["metadata"] = {"mode": "simulation", "generated_at": datetime.now(timezone.utc).isoformat(),
                        "python": platform.python_version(), "packages": versions,
                        "binding": binding or {"status": "unbound exploratory run"}}
    if study == "bell":
        rows = [dict(zip(("a", "b", "x", "y"), v), win=w) for v, w in
                zip(zip(*(data["measurements"][k] for k in ("a", "b", "x", "y"))), data["outcomes"])]
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.bar(["Simulated game", "Quantum limit", "Classical limit"],
               [data["win_probability"], data["quantum_limit"], data["classical_limit"]],
               color=["#0072B2", "#009E73", "#D55E00"])
        ax.set(ylabel="Win probability", ylim=(0, 1), title="Four-qubit CHSH game")
        (output / "circuit.txt").write_text(data["circuit"] + "\n")
    elif study == "damping":
        rows = data["rows"]
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.plot([r["p"] for r in rows], [r["after_one_probability"] for r in rows],
                "o-", label="Sampled after X", color="#0072B2")
        ax.plot([r["p"] for r in rows], [r["ideal_channel_probability"] for r in rows],
                "--", label="Density-matrix channel prediction", color="#D55E00")
        ax.set(xlabel="Amplitude-damping probability p", ylabel="P(after_not_gate = 1)",
               ylim=(-0.03, 1.03), title="Amplitude damping after preparation")
        ax.legend()
        (output / "circuit.txt").write_text(data["circuit"] + "\n")
    elif study == "qaoa":
        rows = data["evaluations"]
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.plot([r["evaluation"] for r in rows], [r["mean_cut"] for r in rows],
                label="Sampled mean cut", color="#0072B2")
        ax.axhline(data["exact_optimum"], linestyle="--", label="Exact optimum", color="#D55E00")
        ax.set(xlabel="Objective evaluation", ylabel="Cut edges", title="Six-node Max-Cut QAOA")
        ax.legend()
        (output / "circuit.txt").write_text(data["circuit"] + "\n")
    else:
        rows = data["rows"]
        fig, axes = plt.subplots(2, 1, figsize=(8, 7), sharex=True)
        for key, label, color in [("ideal", "Ideal", "#009E73"), ("raw", "Unmitigated", "#D55E00"),
                                  ("mitigated", "Richardson ZNE", "#0072B2")]:
            axes[0].plot([r["gamma"] for r in rows], [r[key] for r in rows], label=label, color=color)
        for key, label, color in [("raw_error", "Unmitigated absolute error", "#D55E00"),
                                  ("mitigated_error", "ZNE absolute error", "#0072B2")]:
            axes[1].plot([r["gamma"] for r in rows], [r[key] for r in rows], label=label, color=color)
        axes[0].set(ylabel="ZZ expectation (dimensionless)", title="Variational energy landscape")
        axes[1].set(xlabel="Variational angle gamma (radians)", ylabel="Absolute error")
        for ax in axes:
            ax.legend()
    fig.tight_layout()
    fig.savefig(output / "plot.svg", bbox_inches="tight")
    fig.savefig(output / "plot.png", dpi=160, bbox_inches="tight")
    plt.close(fig)
    with (output / "data.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    (output / "report.json").write_text(json.dumps(data, indent=2, allow_nan=False) + "\n")
    hashes = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(output.iterdir())
              if p.is_file() and p.name != "output-hashes.json"}
    (output / "output-hashes.json").write_text(json.dumps(hashes, indent=2) + "\n")
    return data
