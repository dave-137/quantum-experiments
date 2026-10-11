"""Six-node Max-Cut adaptation of Cirq examples/qaoa.py (Apache-2.0).
Cost/mixer/cut_values retained. Added independent seeds and optimizer/report records.
The default ZZ route is used; unselected BooleanHamiltonianGate alternative is omitted.
"""
import itertools
import networkx
import numpy as np
import scipy.optimize
import cirq

def rzz(rads):
    """Returns a gate with the matrix exp(-i Z⊗Z rads)."""
    return cirq.ZZPowGate(exponent=2 * rads / np.pi, global_shift=-0.5)


def qaoa_max_cut_unitary(qubits, betas, gammas, graph):
    # Selected donor use_boolean_hamiltonian_gate=False route only.
    for beta, gamma in zip(betas, gammas):
        yield (rzz(-0.5 * gamma).on(qubits[i], qubits[j]) for i, j in graph.edges)
        yield cirq.rx(2 * beta).on_each(*qubits)


def qaoa_max_cut_circuit(qubits, betas, gammas, graph):
    return cirq.Circuit(
        cirq.H.on_each(*qubits),
        qaoa_max_cut_unitary(qubits, betas, gammas, graph),
        cirq.measure(*qubits, key='m'),
    )


def cut_values(bitstrings, graph):
    mat = networkx.adjacency_matrix(graph, nodelist=sorted(graph.nodes))
    vecs = (-1) ** np.asarray(bitstrings, dtype=np.int64)
    vals = 0.5 * np.sum(vecs * (mat @ vecs.T).T, axis=-1)
    vals = 0.5 * (graph.size() - vals)
    return vals


def run(repetitions=256, maxiter=50, graph_seed=137, parameter_seed=138, simulator_seed=139):
    n, p = 6, 2
    graph = networkx.random_regular_graph(3, n, seed=graph_seed)
    qubits = cirq.LineQubit.range(n)
    rng = np.random.RandomState(parameter_seed)
    # Preserve donor parameter initialization sequence, including its example circuit.
    example_betas = rng.uniform(-np.pi, np.pi, size=p)
    example_gammas = rng.uniform(-np.pi, np.pi, size=p)
    example = qaoa_max_cut_circuit(qubits, example_betas, example_gammas, graph)
    largest_cut_found, largest_cut_value_found = None, 0
    simulator = cirq.Simulator(seed=simulator_seed)
    evaluations = []

    def f(x):
        nonlocal largest_cut_found, largest_cut_value_found
        circuit = qaoa_max_cut_circuit(qubits, x[:p], x[p:], graph)
        bitstrings = simulator.run(circuit, repetitions=repetitions).measurements["m"]
        values = cut_values(bitstrings, graph)
        max_value_index = np.argmax(values)
        max_value = values[max_value_index]
        if max_value > largest_cut_value_found:
            largest_cut_value_found = max_value
            largest_cut_found = bitstrings[max_value_index].copy()
        mean = np.mean(values)
        evaluations.append({"evaluation": len(evaluations), "mean_cut": float(mean),
                            "best_in_batch": int(max_value), "best_so_far": int(largest_cut_value_found),
                            "parameters": x.tolist()})
        return -mean

    x0 = rng.uniform(-np.pi, np.pi, size=2 * p)
    optimized = scipy.optimize.minimize(f, x0, method="Nelder-Mead", options={"maxiter": maxiter})
    all_bitstrings = np.array(list(itertools.product(range(2), repeat=n)))
    all_values = cut_values(all_bitstrings, graph)
    max_cut_value = np.max(all_values)
    final_circuit = qaoa_max_cut_circuit(qubits, optimized.x[:p], optimized.x[p:], graph)
    return {"parameters": {"n": n, "p": p, "degree": 3, "repetitions": repetitions, "maxiter": maxiter,
                           "graph_seed": graph_seed, "parameter_seed": parameter_seed,
                           "simulator_seed": simulator_seed, "use_boolean_hamiltonian_gate": False},
            "graph_edges": [list(e) for e in graph.edges], "nodelist": sorted(graph.nodes),
            "wire_order": [str(q) for q in qubits],
            "initial_parameters": x0.tolist(), "final_parameters": optimized.x.tolist(),
            "example_parameters": {"betas": example_betas.tolist(), "gammas": example_gammas.tolist()},
            "best_sampled_bitstring": largest_cut_found.tolist(), "best_sampled_cut": int(largest_cut_value_found),
            "exact_optimum": int(max_cut_value), "best_cut_ratio": float(largest_cut_value_found / max_cut_value),
            "optimizer": {"method": "Nelder-Mead", "success": bool(optimized.success),
                          "status": int(optimized.status), "message": str(optimized.message),
                          "nit": int(optimized.nit), "nfev": int(optimized.nfev),
                          "negative_mean_objective": float(optimized.fun)},
            "evaluations": evaluations,
            "exact_values": all_values.astype(int).tolist(),
            "exact_bitstrings": all_bitstrings.tolist(),
            "circuit": str(final_circuit), "example_circuit": str(example),
            "circuit_metrics": {"operations": len(list(final_circuit.all_operations())),
                                "moments": len(final_circuit)}}
