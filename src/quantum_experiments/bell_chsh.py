"""Four-qubit CHSH game adapted from quantumlib/Cirq examples/bell_inequality.py.
Original circuit and measurement binding retained; seeded reporting adapter added.
Licensed under Apache-2.0; see THIRD_PARTY_NOTICES.md and licenses/.
"""
import cirq
import numpy as np

def make_bell_test_circuit():
    alice = cirq.GridQubit(0, 0)
    bob = cirq.GridQubit(1, 0)
    alice_referee = cirq.GridQubit(0, 1)
    bob_referee = cirq.GridQubit(1, 1)

    circuit = cirq.Circuit()

    # Prepare shared entangled state.
    circuit.append([cirq.H(alice), cirq.CNOT(alice, bob)])

    # Referees flip coins.
    circuit.append([cirq.H(alice_referee), cirq.H(bob_referee)])

    # Players do a sqrt(X) based on their referee's coin.
    circuit.append(
        [
            cirq.X(alice) ** -0.25,
            cirq.CNOT(alice_referee, alice) ** 0.5,
            cirq.CNOT(bob_referee, bob) ** 0.5,
        ]
    )

    # Then results are recorded.
    circuit.append(
        [
            cirq.measure(alice, key='a'),
            cirq.measure(bob, key='b'),
            cirq.measure(alice_referee, key='x'),
            cirq.measure(bob_referee, key='y'),
        ]
    )

    return circuit



def run(repetitions=4096, seed=137):
    circuit = make_bell_test_circuit()
    result = cirq.Simulator(seed=seed).run(program=circuit, repetitions=repetitions)
    a, b, x, y = [np.array(result.measurements[k][:, 0]) for k in ("a", "b", "x", "y")]
    outcomes = (a ^ b) == (x & y)
    return {"parameters": {"repetitions": repetitions, "seed": seed},
            "wins": int(np.count_nonzero(outcomes)), "trials": repetitions,
            "win_probability": float(np.count_nonzero(outcomes) / repetitions),
            "quantum_limit": float(np.cos(np.pi / 8) ** 2), "classical_limit": 0.75,
            "measurements": {k: result.measurements[k][:, 0].tolist() for k in ("a", "b", "x", "y")},
            "outcomes": outcomes.astype(int).tolist(), "circuit": str(circuit)}
