"""Cirq bell_inequality main tally and examples_test smoke adapted (Apache-2.0)."""
import numpy as np
from quantum_experiments.bell_chsh import make_bell_test_circuit, run


def test_donor_game_measurement_binding_and_theory():
    r = run(4096, 137)
    arrays = [np.array(r["measurements"][k]) for k in ["a", "b", "x", "y"]]
    assert all(a.shape == (4096,) for a in arrays)
    a, b, x, y = arrays
    wins = (a ^ b) == (x & y)
    assert np.count_nonzero(wins) == r["wins"]
    assert r["outcomes"] == wins.astype(int).tolist()
    assert r["wins"] <= r["trials"] == 4096
    assert r["win_probability"] == r["wins"] / r["trials"]
    assert r["classical_limit"] == 0.75
    # A broad finite-shot guard, not a confidence interval or identical-count demand.
    assert abs(r["win_probability"] - r["quantum_limit"]) < 0.04
    assert len(make_bell_test_circuit().all_qubits()) == 4


def test_explicit_seed_reproducibility():
    assert run(75, 137) == run(75, 137)
