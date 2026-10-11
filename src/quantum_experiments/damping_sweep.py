# Copyright 2022 The Cirq Developers
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
"""Adapted Cirq noisy_simulation_example; same measurement/channel semantics.
Apache-2.0. Density-matrix comparison follows Cirq noisy_simulation notebook.
Changed: explicit shots/seed, sweep records and portable output instead of print.
"""
import cirq


def make_circuit():
    q = cirq.NamedQubit("q")
    return cirq.Circuit(cirq.measure(q, key="initial_state"), cirq.X(q),
                        cirq.measure(q, key="after_not_gate"))


def run(repetitions=1024, seed=137, rates=(0, 0.4, 0.5, 1)):
    circuit = make_circuit()
    rows, measurements = [], []
    for p in rates:
        channel = cirq.amplitude_damp(p)
        result = cirq.sample(program=circuit, noise=cirq.ConstantQubitNoiseModel(channel),
                             repetitions=repetitions, seed=seed)
        initial = result.histogram(key="initial_state")
        final = result.histogram(key="after_not_gate")
        q = cirq.NamedQubit("q")
        rho = cirq.DensityMatrixSimulator().simulate(
            cirq.Circuit(cirq.X(q), channel.on(q))).final_density_matrix
        rows.append({"p": p, "initial_zero": int(initial[0]), "initial_one": int(initial[1]),
                     "after_zero": int(final[0]), "after_one": int(final[1]),
                     "after_one_probability": float(final[1] / repetitions),
                     "ideal_channel_probability": float(rho[1, 1].real)})
        measurements.append({"p": p, "initial_state": result.measurements["initial_state"][:, 0].tolist(),
                             "after_not_gate": result.measurements["after_not_gate"][:, 0].tolist()})
    return {"parameters": {"repetitions": repetitions, "seed": seed, "rates": list(rates),
                           "seed_policy": "same explicit seed for each independent rate"},
            "rows": rows, "measurements": measurements, "circuit": str(circuit)}
