# External sources

The study implementations adapt the pinned external examples below. Source revision and installed distribution version are distinct; the remote hash lock records the latter. Changes are dated 2026-10-11.

## Experiments and numerical checks

| Source | Pin | Adapted mechanisms |
|---|---|---|
| [quantumlib/Cirq/examples/bell_inequality.py](https://github.com/quantumlib/Cirq/blob/1403830e59df5835ffc3f09e53cefedc81840a56/examples/bell_inequality.py) | `1403830e59df5835ffc3f09e53cefedc81840a56` | Four-qubit CHSH circuit, register binding, XOR/AND tally, quantum/classical game limits |
| [quantumlib/Cirq/examples/noisy_simulation_example.py](https://github.com/quantumlib/Cirq/blob/1403830e59df5835ffc3f09e53cefedc81840a56/examples/noisy_simulation_example.py) | `1403830e59df5835ffc3f09e53cefedc81840a56` | Initial/X/final measurements, amplitude damping and ConstantQubitNoiseModel |
| [quantumlib/Cirq/docs/simulate/noisy_simulation.ipynb](https://github.com/quantumlib/Cirq/blob/1403830e59df5835ffc3f09e53cefedc81840a56/docs/simulate/noisy_simulation.ipynb) | `1403830e59df5835ffc3f09e53cefedc81840a56` | Amplitude-damping Kraus interpretation, density-matrix simulation, moment noise insertion |
| [quantumlib/Cirq/cirq-core/cirq/sim/density_matrix_simulator_test.py](https://github.com/quantumlib/Cirq/blob/1403830e59df5835ffc3f09e53cefedc81840a56/cirq-core/cirq/sim/density_matrix_simulator_test.py) | `1403830e59df5835ffc3f09e53cefedc81840a56` | Selected channel, measurement, repetition and seed invariants |
| [unitaryfoundation/mitiq/docs/source/guide/zne-1-intro.md](https://github.com/unitaryfoundation/mitiq/blob/1a892a9783ddfe8c39d3d035613d6f3d168df9af/docs/source/guide/zne-1-intro.md) | `1a892a9783ddfe8c39d3d035613d6f3d168df9af` | Construct/execute/combine two-stage flow and ordered results |
| [unitaryfoundation/mitiq/docs/source/guide/zne-2-use-case.md](https://github.com/unitaryfoundation/mitiq/blob/1a892a9783ddfe8c39d3d035613d6f3d168df9af/docs/source/guide/zne-2-use-case.md) | `1a892a9783ddfe8c39d3d035613d6f3d168df9af` | Extrapolation bias and limitations |
| [unitaryfoundation/mitiq/docs/source/guide/zne-4-low-level.md](https://github.com/unitaryfoundation/mitiq/blob/1a892a9783ddfe8c39d3d035613d6f3d168df9af/docs/source/guide/zne-4-low-level.md) | `1a892a9783ddfe8c39d3d035613d6f3d168df9af` | Intermediate circuits/values and factory inference |
| [unitaryfoundation/mitiq/mitiq/zne/zne.py](https://github.com/unitaryfoundation/mitiq/blob/1a892a9783ddfe8c39d3d035613d6f3d168df9af/mitiq/zne/zne.py) | `1a892a9783ddfe8c39d3d035613d6f3d168df9af` | Public construct_circuits, combine_results, mitigate_executor API verification |
| [quantumlib/Cirq/examples/examples_test.py](https://github.com/quantumlib/Cirq/blob/1403830e59df5835ffc3f09e53cefedc81840a56/examples/examples_test.py) | `1403830e59df5835ffc3f09e53cefedc81840a56` | Selected Bell/noise/QAOA smoke and global-phase unitary comparison |
| [unitaryfoundation/mitiq/docs/source/examples/simple-landscape-cirq.md](https://github.com/unitaryfoundation/mitiq/blob/1a892a9783ddfe8c39d3d035613d6f3d168df9af/docs/source/examples/simple-landscape-cirq.md) | `1a892a9783ddfe8c39d3d035613d6f3d168df9af` | Variational ansatz, ZZ trace, depolarization, 50-point sweep, Richardson [1,3,5], plots |
| [unitaryfoundation/mitiq/mitiq/zne/scaling/folding.py](https://github.com/unitaryfoundation/mitiq/blob/1a892a9783ddfe8c39d3d035613d6f3d168df9af/mitiq/zne/scaling/folding.py) | `1a892a9783ddfe8c39d3d035613d6f3d168df9af` | fold_gates_at_random seed/default weighting/default moment squashing |
| [unitaryfoundation/mitiq/mitiq/zne/inference.py](https://github.com/unitaryfoundation/mitiq/blob/1a892a9783ddfe8c39d3d035613d6f3d168df9af/mitiq/zne/inference.py) | `1a892a9783ddfe8c39d3d035613d6f3d168df9af` | RichardsonFactory.extrapolate delegates to degree-two PolyFactory |
| [quantumlib/Cirq/examples/qaoa.py](https://github.com/quantumlib/Cirq/blob/1403830e59df5835ffc3f09e53cefedc81840a56/examples/qaoa.py) | `1403830e59df5835ffc3f09e53cefedc81840a56` | rzz, Rx/ZZ QAOA, sampled negative mean, Nelder–Mead, cut_values and exhaustive enumeration |

## Adaptation boundaries

Original Bell circuit and QAOA generator functions are retained. Print-only runners become functions returning scientific arrays/records. Seeds/shots/rates are explicit; QAOA graph, parameter and simulator streams are separate. A signed-integer adapter protects the donor cut expression under NumPy 2. The unselected optional Boolean cost branch is omitted; only the false/default donor route is retained.

E4 retains the landscape example’s ansatz/executor/noise/grid/Richardson choice and uses the donor guide’s public low-level flow to expose ordered folded circuits. Each fold receives an explicit seed; no new simulator, optimizer or extrapolation algorithm is implemented.

Notebooks import the same study modules. Reporting adds only serialization, file hashes, environment binding and plots derived from executed arrays. Tests adapt selected donor invariants and checks for the new records, rather than importing upstream test suites.

## Package/license surfaces inspected

- [quantumlib/Cirq/LICENSE](https://github.com/quantumlib/Cirq/blob/1403830e59df5835ffc3f09e53cefedc81840a56/LICENSE) — external dependency/notice context.
- [quantumlib/Cirq/pyproject.toml](https://github.com/quantumlib/Cirq/blob/1403830e59df5835ffc3f09e53cefedc81840a56/pyproject.toml) — external dependency/notice context.
- [quantumlib/Cirq/cirq-core/requirements.txt](https://github.com/quantumlib/Cirq/blob/1403830e59df5835ffc3f09e53cefedc81840a56/cirq-core/requirements.txt) — external dependency/notice context.
- [unitaryfoundation/mitiq/mitiq/zne/tests/test_zne.py](https://github.com/unitaryfoundation/mitiq/blob/1a892a9783ddfe8c39d3d035613d6f3d168df9af/mitiq/zne/tests/test_zne.py) — external dependency/notice context.
- [unitaryfoundation/mitiq/pyproject.toml](https://github.com/unitaryfoundation/mitiq/blob/1a892a9783ddfe8c39d3d035613d6f3d168df9af/pyproject.toml) — external dependency/notice context.
- [unitaryfoundation/mitiq/LICENSE](https://github.com/unitaryfoundation/mitiq/blob/1a892a9783ddfe8c39d3d035613d6f3d168df9af/LICENSE) — external dependency/notice context.
- [quantumlib/Cirq/cirq-core/setup.py](https://github.com/quantumlib/Cirq/blob/1403830e59df5835ffc3f09e53cefedc81840a56/cirq-core/setup.py) — external dependency/notice context.
- [quantumlib/Cirq/cirq-core/cirq/_version.py](https://github.com/quantumlib/Cirq/blob/1403830e59df5835ffc3f09e53cefedc81840a56/cirq-core/cirq/_version.py) — external dependency/notice context.

Cirq is Apache-2.0; Mitiq is GPL v3 at the captured revision. [Third-party notices](../THIRD_PARTY_NOTICES.md) retain notices and modification descriptions, and the full license texts accompany the adapted source. Source code and build/report scripts remain inspectable in this repository.

