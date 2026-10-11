# Modified 2026-10-11: explicit seeds and ordered intermediate records.
"""Adapted Mitiq simple-landscape-cirq example and ZNE two-stage guide.
Copyright (C) Unitary Foundation
This source code is licensed under GPL v3; see LICENSE.
Changed: deterministic folding, ordered intermediate records and portable reports.
"""
from functools import partial
import numpy as np
from cirq import Circuit, rx, CNOT, DensityMatrixSimulator, LineQubit, depolarize
from mitiq.zne import construct_circuits, combine_results
from mitiq.zne.inference import RichardsonFactory
from mitiq.zne.scaling import fold_gates_at_random

z = np.diag([1, -1])
hamiltonian = np.kron(z, z)
SCALE_FACTORS = [1, 3, 5]


def variational_circuit(gamma: float) -> Circuit:
    q0, q1 = LineQubit.range(2)
    return Circuit([rx(gamma)(q0), CNOT(q0, q1), rx(gamma)(q1), CNOT(q0, q1), rx(gamma)(q0)])


def noiseless_executor(circ: Circuit) -> float:
    rho = DensityMatrixSimulator().simulate(circ).final_density_matrix
    return float(np.real(np.trace(rho @ hamiltonian)))


def executor_with_noise(circ: Circuit, p=0.04) -> float:
    return noiseless_executor(circ.with_noise(depolarize(p)))


def scaled_circuits(circuit, folding_seed=137):
    return construct_circuits(circuit, SCALE_FACTORS,
                              scale_method=partial(fold_gates_at_random, seed=folding_seed))


def run(points=50, p=0.04, folding_seed=137):
    gammas = np.linspace(0, 2 * np.pi, points)
    rows, intermediate = [], []
    for gamma in gammas:
        circuit = variational_circuit(gamma)
        ideal = noiseless_executor(circuit)
        raw = executor_with_noise(circuit, p)
        folded = scaled_circuits(circuit, folding_seed)
        expectations = [executor_with_noise(circ, p) for circ in folded]
        mitigated = float(combine_results(SCALE_FACTORS, expectations, RichardsonFactory.extrapolate))
        rows.append({"gamma": float(gamma), "ideal": ideal, "raw": raw, "mitigated": mitigated,
                     "raw_error": abs(raw - ideal), "mitigated_error": abs(mitigated - ideal)})
        intermediate.append({"gamma": float(gamma), "scales": [
            {"scale_factor": scale, "expectation": value,
             "ideal_expectation": noiseless_executor(circ), "circuit": str(circ),
             "operations": len(list(circ.all_operations())), "moments": len(circ)}
            for scale, value, circ in zip(SCALE_FACTORS, expectations, folded)]})
    return {"parameters": {"points": points, "noise_probability": p, "folding_seed": folding_seed,
                           "scale_factors": SCALE_FACTORS, "fit": "RichardsonFactory.extrapolate",
                           "folding": "fold_gates_at_random default weighting and squash_moments",
                           "seed_policy": "same folding seed passed independently at every scale/gamma"},
            "rows": rows, "intermediate": intermediate,
            "summary": {"mean_raw_error": float(np.mean([r["raw_error"] for r in rows])),
                        "mean_mitigated_error": float(np.mean([r["mitigated_error"] for r in rows])),
                        "worsened_points": sum(r["mitigated_error"] > r["raw_error"] for r in rows),
                        "out_of_range_points": sum(abs(r["mitigated"]) > 1 for r in rows)}}
