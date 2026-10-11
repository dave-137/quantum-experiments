# Copyright (C) Unitary Foundation
#
# This source code is licensed under the GPL license (v3) found in the
# LICENSE file in the root directory of this source tree.
# Modified 2026-10-11: selected study interfaces and validation.

"""Mitiq test_zne no-noise/two-stage tests adapted; GPL v3.
Unitary comparison follows Cirq examples_test test_example_qaoa_same_unitary.
"""
from functools import partial
import cirq
import numpy as np
from mitiq.zne import mitigate_executor
from mitiq.zne.inference import RichardsonFactory
from mitiq.zne.scaling import fold_gates_at_random
from quantum_experiments.zne_landscape import (
    variational_circuit, noiseless_executor, executor_with_noise, scaled_circuits, run, SCALE_FACTORS,
)


def test_folded_ideal_equivalence():
    circuit = variational_circuit(0.731)
    folded = scaled_circuits(circuit, 137)
    assert len(folded) == len(SCALE_FACTORS)
    for c in folded:
        assert cirq.allclose_up_to_global_phase(cirq.unitary(circuit), cirq.unitary(c), atol=1e-6)
        assert np.isclose(noiseless_executor(c), noiseless_executor(circuit), atol=1e-6)


def test_two_stage_agrees_with_mitigated_executor():
    circuit = variational_circuit(0.731)
    folded = scaled_circuits(circuit, 137)
    values = [executor_with_noise(c) for c in folded]
    high_level = mitigate_executor(executor_with_noise, factory=RichardsonFactory(SCALE_FACTORS),
                                  scale_noise=partial(fold_gates_at_random, seed=137))
    assert np.isclose(high_level(circuit), RichardsonFactory.extrapolate(SCALE_FACTORS, values), atol=1e-6)


def test_no_noise_agreement_and_full_grid():
    r = run(points=50, p=0, folding_seed=137)
    assert len(r["rows"]) == len(r["intermediate"]) == 50
    assert r["rows"][0]["gamma"] == 0
    assert r["rows"][-1]["gamma"] == 2 * np.pi
    for row, inter in zip(r["rows"], r["intermediate"]):
        assert np.isclose(row["raw"], row["ideal"], atol=1e-6)
        assert np.isclose(row["mitigated"], row["ideal"], atol=1e-6)
        assert [s["scale_factor"] for s in inter["scales"]] == SCALE_FACTORS
        assert all(np.isfinite(s["expectation"]) for s in inter["scales"])


def test_raw_reporting_keeps_errors_and_unclipped_values():
    r = run(points=5)
    for row in r["rows"]:
        assert all(np.isfinite(row[k]) for k in ["ideal", "raw", "mitigated"])
        assert row["raw_error"] == abs(row["raw"] - row["ideal"])
        assert row["mitigated_error"] == abs(row["mitigated"] - row["ideal"])
    assert r["summary"]["worsened_points"] == sum(row["mitigated_error"] > row["raw_error"] for row in r["rows"])
    assert r["summary"]["out_of_range_points"] == sum(abs(row["mitigated"]) > 1 for row in r["rows"])
