# Third-party notices

This project adapts examples and selected numerical-test patterns from Cirq and Mitiq. The combined source is distributed under GPL-3.0-only; retained Cirq portions carry their Apache-2.0 terms and notices. Full license texts are in [LICENSE](LICENSE) and [Apache-2.0](licenses/Apache-2.0.txt).

## Cirq

Source: quantumlib/Cirq, revision `1403830e59df5835ffc3f09e53cefedc81840a56`.

Adapted `examples/bell_inequality.py`, `examples/noisy_simulation_example.py`, `examples/qaoa.py`, selected `examples/examples_test.py` paths, `docs/simulate/noisy_simulation.ipynb`, and selected `cirq-core/cirq/sim/density_matrix_simulator_test.py` patterns. The example files contain no separate copyright notice. The noise notebook carries **Copyright 2022 The Cirq Developers**; simulator tests carry **Copyright 2019 The Cirq Developers**.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use these portions except in compliance with the License. You may obtain a copy of the License at https://www.apache.org/licenses/LICENSE-2.0. Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

Changes made 2026-10-11: parameterized seeds/shots, independent QAOA random streams, optimizer/result records, thin notebook entrypoints, serialization and presentation; selected assertions adapted to these study interfaces. Original circuit, channel, cost/mixer and exhaustive-cut mechanisms are retained.

## Mitiq

Source: unitaryfoundation/mitiq, revision `1a892a9783ddfe8c39d3d035613d6f3d168df9af`.

Adapted `docs/source/examples/simple-landscape-cirq.md`, ZNE introduction/use-case/low-level guidance and selected `mitiq/zne/tests/test_zne.py` patterns. APIs in `mitiq/zne/zne.py`, `scaling/folding.py` and `inference.py` are used from the installed library, not vendored.

Copyright (C) Unitary Foundation

This source code is licensed under the GPL license (v3) found in the LICENSE file in the root directory of this source tree.

Changes made 2026-10-11: explicit folding seed, source-defined two-stage ZNE instead of an opaque mitigated executor, ordered folded-circuit/expectation/cost records, full unclipped error reporting, CLI/notebook integration and plots. The ansatz, ZZ trace executor, noise rate and Richardson scale factors are retained.

The complete adapted source, build inputs and notebook/report scripts accompany this repository. For dependency versions, see the resolved environment artifact and the external source citations in [sources](docs/sources.md).
