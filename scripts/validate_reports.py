"""Remote report consistency QA. Human plot/rendering inspection remains separate."""
import hashlib
import json
from pathlib import Path


def main():
    binding = json.loads(Path("proof/binding.json").read_text())
    image_hashes = set()
    for prefix in [Path("results"), Path("results/notebooks")]:
        for study in ["bell", "damping", "qaoa", "zne"]:
            root = prefix / study
            r = json.loads((root / "report.json").read_text())
            assert r["metadata"]["mode"] == "simulation"
            assert r["metadata"]["binding"] == binding
            hashes = json.loads((root / "output-hashes.json").read_text())
            for name, digest in hashes.items():
                assert hashlib.sha256((root / name).read_bytes()).hexdigest() == digest
            if prefix == Path("results"):
                assert hashes["plot.png"] not in image_hashes
                image_hashes.add(hashes["plot.png"])
            if study == "bell":
                assert r["trials"] == 4096 and sum(r["outcomes"]) == r["wins"]
                assert all(len(a) == 4096 for a in r["measurements"].values())
            elif study == "damping":
                assert [row["p"] for row in r["rows"]] == [0, 0.4, 0.5, 1]
                for row in r["rows"]:
                    assert row["initial_zero"] + row["initial_one"] == r["parameters"]["repetitions"]
                    assert row["after_zero"] + row["after_one"] == r["parameters"]["repetitions"]
            elif study == "qaoa":
                assert max(r["exact_values"]) == r["exact_optimum"]
                assert r["best_sampled_cut"] <= r["exact_optimum"]
                assert len(r["exact_values"]) == 64
            else:
                assert len(r["rows"]) == len(r["intermediate"]) == 50
                assert all([s["scale_factor"] for s in rec["scales"]] == [1, 3, 5]
                           for rec in r["intermediate"])
    Path("proof/report-validation.json").write_text(json.dumps({
        "status": "passed", "reports": 8, "distinct_scripted_plot_images": 4,
        "human_plot_inspection": "pending separate rendering review"}, indent=2) + "\n")


if __name__ == "__main__":
    main()
