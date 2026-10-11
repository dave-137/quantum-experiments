# Copyright 2019 The Cirq Developers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Modified 2026-10-11: parameterized/reporting study adaptation.
"""Adapted noisy demo and density_matrix_simulator_test channel/seed invariants.
Apache-2.0; only selected single-qubit paths retained.
"""
import pytest
from quantum_experiments.damping_sweep import run


def test_endpoints_counts_and_binding():
    r = run(128, 137)
    for row, m in zip(r["rows"], r["measurements"]):
        assert row["initial_zero"] == 128 and row["initial_one"] == 0
        assert row["after_zero"] + row["after_one"] == 128
        assert len(m["initial_state"]) == len(m["after_not_gate"]) == 128
        assert sum(m["after_not_gate"]) == row["after_one"]
    assert r["rows"][0]["after_one"] == 128
    assert r["rows"][-1]["after_one"] == 0
    assert r["rows"][0]["ideal_channel_probability"] == 1
    assert r["rows"][-1]["ideal_channel_probability"] == 0


def test_channel_mixture_and_seed():
    a = run(128, 137, rates=(0.5,))
    assert a == run(128, 137, rates=(0.5,))
    assert set(a["measurements"][0]["after_not_gate"]) == {0, 1}


@pytest.mark.parametrize("p", [-0.1, 1.1])
def test_malformed_probability_uses_cirq_validation(p):
    with pytest.raises(ValueError):
        run(10, 137, rates=(p,))
