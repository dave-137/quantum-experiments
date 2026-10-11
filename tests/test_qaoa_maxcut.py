"""Cirq qaoa cut_values/exhaustive baseline and examples_test smoke adapted.
Apache-2.0. Independent XOR edge check uses donor Boolean cost expression.
"""
import cirq
import networkx
import numpy as np
from quantum_experiments.qaoa_maxcut import run, cut_values


def test_sampled_best_and_exact_ordering():
    r = run(repetitions=32, maxiter=5)
    graph = networkx.Graph()
    graph.add_nodes_from(r["nodelist"])
    graph.add_edges_from(r["graph_edges"])
    assert r["nodelist"] == list(range(6))
    assert r["wire_order"] == [str(q) for q in cirq.LineQubit.range(6)]
    assert all(d == 3 for _, d in graph.degree())
    best = np.array(r["best_sampled_bitstring"])
    assert int(cut_values(best[None, :], graph)[0]) == r["best_sampled_cut"]
    assert sum(int(best[i] ^ best[j]) for i, j in graph.edges) == r["best_sampled_cut"]
    values = cut_values(np.array(r["exact_bitstrings"]), graph)
    assert len(values) == 64
    assert values.astype(int).tolist() == r["exact_values"]
    assert int(max(values)) == r["exact_optimum"]
    assert 0 <= r["best_sampled_cut"] <= r["exact_optimum"]
    assert r["best_cut_ratio"] == r["best_sampled_cut"] / r["exact_optimum"]
    assert all(e["best_in_batch"] <= r["exact_optimum"] for e in r["evaluations"])
    assert r["optimizer"]["nfev"] == len(r["evaluations"])
    assert r["optimizer"]["message"]
    assert np.isfinite(r["optimizer"]["negative_mean_objective"])


def test_three_seed_reproducibility():
    assert run(16, 3, 137, 138, 139) == run(16, 3, 137, 138, 139)
